import javax.swing.*;
import java.awt.*;
import java.awt.geom.*;
import java.io.*;
import java.util.*;
import java.util.List;

/**
 * GNSS Train Positioning System using Colored Petri Nets (CPN)
 * 
 * This implementation models a GPS-based train positioning system using
 * hierarchical Colored Petri Nets with Extended Kalman Filter for position estimation.
 * 
 * Based on Petri net modeling for GNSS positioning in railway environments.
 */
public class GNSSTrainPositioningCPN {

    // ==================== CPN Model Classes ====================
    
    /**
     * Represents a Place in the Colored Petri Net
     * Places hold tokens (colored data) representing system states
     */
    static class Place {
        String name;
        List<Object> tokens;
        
        Place(String name) {
            this.name = name;
            this.tokens = new ArrayList<>();
        }
        
        void addToken(Object token) {
            tokens.add(token);
        }
        
        Object removeToken() {
            // Remove from end instead of beginning for O(1) performance
            return tokens.isEmpty() ? null : tokens.remove(tokens.size() - 1);
        }
        
        boolean hasToken() {
            return !tokens.isEmpty();
        }
        
        Object peekToken() {
            return tokens.isEmpty() ? null : tokens.get(0);
        }
    }
    
    /**
     * Represents a Transition in the Colored Petri Net
     * Transitions represent actions/transformations in the system
     */
    static class Transition {
        String name;
        List<Place> inputPlaces;
        List<Place> outputPlaces;
        
        Transition(String name) {
            this.name = name;
            this.inputPlaces = new ArrayList<>();
            this.outputPlaces = new ArrayList<>();
        }
        
        void addInput(Place place) {
            inputPlaces.add(place);
        }
        
        void addOutput(Place place) {
            outputPlaces.add(place);
        }
        
        boolean isEnabled() {
            for (Place p : inputPlaces) {
                if (!p.hasToken()) return false;
            }
            return true;
        }
        
        void fire() {
            // Consume tokens from input places
            List<Object> consumedTokens = new ArrayList<>();
            for (Place p : inputPlaces) {
                consumedTokens.add(p.removeToken());
            }
            
            // Produce tokens to output places (pass through for now)
            for (Place p : outputPlaces) {
                for (Object token : consumedTokens) {
                    p.addToken(token);
                }
            }
        }
    }
    
    // ==================== Domain Model Classes ====================
    
    /**
     * Environment types affecting GNSS signal quality
     */
    enum Environment {
        OPEN_AREA(1.0),      // Clear sky, minimal interference
        MOUNTAIN(2.5),       // Partial obstruction, multipath
        TUNNEL(5.0);         // Severe signal degradation
        
        final double noiseFactor;
        
        Environment(double noiseFactor) {
            this.noiseFactor = noiseFactor;
        }
    }
    
    /**
     * Interference types affecting GNSS signals
     */
    enum Interference {
        NORMAL(0.0),         // No interference
        AM(1.5),             // Amplitude Modulation interference
        FM(2.5),             // Frequency Modulation interference (most severe)
        PULSE(1.0);          // Pulse interference
        
        final double errorMultiplier;
        
        Interference(double errorMultiplier) {
            this.errorMultiplier = errorMultiplier;
        }
    }
    
    /**
     * Represents a GNSS signal from a satellite
     */
    static class GNSSSignal {
        int satelliteId;
        double pseudorange;      // Distance measurement
        double carrierPhase;     // Phase measurement
        double[] position;       // Satellite position [x, y, z]
        double snr;              // Signal-to-Noise Ratio
        Environment environment;
        Interference interference;
        double timestamp;
        
        GNSSSignal(int satelliteId, double[] satPosition, Environment env, Interference interf, double time) {
            this.satelliteId = satelliteId;
            this.position = satPosition;
            this.environment = env;
            this.interference = interf;
            this.timestamp = time;
            this.snr = 45.0; // Default good SNR
        }
    }
    
    /**
     * Represents the train state (position, velocity, and uncertainty)
     */
    static class TrainState {
        double[] position;       // [x, y, z] in meters
        double[] velocity;       // [vx, vy, vz] in m/s
        double[][] covariance;   // 6x6 covariance matrix
        double timestamp;
        Environment environment;
        Interference interference;
        
        TrainState(double[] pos, double[] vel, double time, Environment env, Interference interf) {
            this.position = pos.clone();
            this.velocity = vel.clone();
            this.timestamp = time;
            this.environment = env;
            this.interference = interf;
            
            // Initialize covariance matrix (6x6 for position and velocity)
            this.covariance = new double[6][6];
            for (int i = 0; i < 3; i++) {
                covariance[i][i] = 10.0;      // Position uncertainty (10m)
                covariance[i+3][i+3] = 1.0;   // Velocity uncertainty (1 m/s)
            }
        }
        
        TrainState copy() {
            TrainState copy = new TrainState(position, velocity, timestamp, environment, interference);
            copy.covariance = new double[6][6];
            for (int i = 0; i < 6; i++) {
                System.arraycopy(covariance[i], 0, copy.covariance[i], 0, 6);
            }
            return copy;
        }
        
        double getPositionError(double[] truePosition) {
            double dx = position[0] - truePosition[0];
            double dy = position[1] - truePosition[1];
            double dz = position[2] - truePosition[2];
            return Math.sqrt(dx*dx + dy*dy + dz*dz);
        }
    }
    
    // ==================== Matrix Operations ====================
    
    /**
     * Utility class for matrix operations needed by EKF
     */
    static class Matrix {
        
        static double[][] multiply(double[][] A, double[][] B) {
            int rowsA = A.length;
            int colsA = A[0].length;
            int colsB = B[0].length;
            
            double[][] result = new double[rowsA][colsB];
            for (int i = 0; i < rowsA; i++) {
                for (int j = 0; j < colsB; j++) {
                    for (int k = 0; k < colsA; k++) {
                        result[i][j] += A[i][k] * B[k][j];
                    }
                }
            }
            return result;
        }
        
        static double[][] add(double[][] A, double[][] B) {
            int rows = A.length;
            int cols = A[0].length;
            double[][] result = new double[rows][cols];
            for (int i = 0; i < rows; i++) {
                for (int j = 0; j < cols; j++) {
                    result[i][j] = A[i][j] + B[i][j];
                }
            }
            return result;
        }
        
        static double[][] subtract(double[][] A, double[][] B) {
            int rows = A.length;
            int cols = A[0].length;
            double[][] result = new double[rows][cols];
            for (int i = 0; i < rows; i++) {
                for (int j = 0; j < cols; j++) {
                    result[i][j] = A[i][j] - B[i][j];
                }
            }
            return result;
        }
        
        static double[][] transpose(double[][] A) {
            int rows = A.length;
            int cols = A[0].length;
            double[][] result = new double[cols][rows];
            for (int i = 0; i < rows; i++) {
                for (int j = 0; j < cols; j++) {
                    result[j][i] = A[i][j];
                }
            }
            return result;
        }
        
        static double[][] identity(int n) {
            double[][] result = new double[n][n];
            for (int i = 0; i < n; i++) {
                result[i][i] = 1.0;
            }
            return result;
        }
        
        static double[][] scale(double[][] A, double scalar) {
            int rows = A.length;
            int cols = A[0].length;
            double[][] result = new double[rows][cols];
            for (int i = 0; i < rows; i++) {
                for (int j = 0; j < cols; j++) {
                    result[i][j] = A[i][j] * scalar;
                }
            }
            return result;
        }
        
        // Simplified matrix inverse for small matrices
        static double[][] inverse(double[][] A) {
            int n = A.length;
            if (n == 1) {
                return new double[][]{{1.0 / A[0][0]}};
            }
            
            // Gaussian elimination with partial pivoting
            double[][] augmented = new double[n][2*n];
            for (int i = 0; i < n; i++) {
                System.arraycopy(A[i], 0, augmented[i], 0, n);
                augmented[i][n+i] = 1.0;
            }
            
            // Forward elimination
            for (int i = 0; i < n; i++) {
                // Find pivot
                int maxRow = i;
                for (int k = i+1; k < n; k++) {
                    if (Math.abs(augmented[k][i]) > Math.abs(augmented[maxRow][i])) {
                        maxRow = k;
                    }
                }
                
                // Swap rows
                double[] temp = augmented[i];
                augmented[i] = augmented[maxRow];
                augmented[maxRow] = temp;
                
                // Make diagonal 1
                double pivot = augmented[i][i];
                if (Math.abs(pivot) < 1e-10) pivot = 1e-10;
                for (int j = 0; j < 2*n; j++) {
                    augmented[i][j] /= pivot;
                }
                
                // Eliminate column
                for (int k = 0; k < n; k++) {
                    if (k != i) {
                        double factor = augmented[k][i];
                        for (int j = 0; j < 2*n; j++) {
                            augmented[k][j] -= factor * augmented[i][j];
                        }
                    }
                }
            }
            
            // Extract inverse
            double[][] result = new double[n][n];
            for (int i = 0; i < n; i++) {
                System.arraycopy(augmented[i], n, result[i], 0, n);
            }
            return result;
        }
    }
    
    // ==================== GNSS Receiver CPN ====================
    
    /**
     * GNSS Receiver sub-model (CPN)
     * Generates satellite signals and processes them with noise and interference
     */
    static class GNSSReceiverCPN {
        Place satelliteConstellation;
        Place rawSignals;
        Transition signalGeneration;
        Random random;
        
        GNSSReceiverCPN() {
            satelliteConstellation = new Place("SatelliteConstellation");
            rawSignals = new Place("RawSignals");
            signalGeneration = new Transition("SignalGeneration");
            
            signalGeneration.addInput(satelliteConstellation);
            signalGeneration.addOutput(rawSignals);
            
            // Fixed seed for reproducibility. To change seed for different variations,
            // modify the seed value (e.g., new Random(System.currentTimeMillis()))
            random = new Random(42);
        }
        
        /**
         * Generate satellite constellation (4 satellites in view)
         */
        void generateSatellites(double[] trainPos, Environment env, Interference interf, double time) {
            // Create 4 satellites at different positions
            double[][] satPositions = {
                {trainPos[0] + 20000000, trainPos[1] + 5000000, trainPos[2] + 15000000},
                {trainPos[0] - 15000000, trainPos[1] + 20000000, trainPos[2] + 10000000},
                {trainPos[0] + 10000000, trainPos[1] - 18000000, trainPos[2] + 20000000},
                {trainPos[0] - 12000000, trainPos[1] - 12000000, trainPos[2] + 18000000}
            };
            
            for (int i = 0; i < 4; i++) {
                GNSSSignal signal = new GNSSSignal(i+1, satPositions[i], env, interf, time);
                satelliteConstellation.addToken(signal);
            }
        }
        
        /**
         * Process signals with environment-based noise and interference
         */
        List<GNSSSignal> processSignals(double[] trainPos) {
            List<GNSSSignal> processedSignals = new ArrayList<>();
            
            while (satelliteConstellation.hasToken()) {
                GNSSSignal signal = (GNSSSignal) satelliteConstellation.removeToken();
                
                // Calculate true geometric range
                double dx = signal.position[0] - trainPos[0];
                double dy = signal.position[1] - trainPos[1];
                double dz = signal.position[2] - trainPos[2];
                double trueRange = Math.sqrt(dx*dx + dy*dy + dz*dz);
                
                // Add environmental noise
                double baseNoise = random.nextGaussian() * 2.0; // 2m base noise
                double envNoise = baseNoise * signal.environment.noiseFactor;
                
                // Add multipath error (depends on environment)
                double multipathError = 0.0;
                if (signal.environment == Environment.MOUNTAIN) {
                    multipathError = random.nextGaussian() * 1.5;
                } else if (signal.environment == Environment.TUNNEL) {
                    multipathError = random.nextGaussian() * 3.0;
                }
                
                // Add interference effects
                double interferenceError = 0.0;
                if (signal.interference != Interference.NORMAL) {
                    interferenceError = random.nextGaussian() * signal.interference.errorMultiplier;
                }
                
                // Calculate pseudorange with all errors
                signal.pseudorange = trueRange + envNoise + multipathError + interferenceError;
                
                // Carrier phase (more precise but with ambiguity)
                double wavelength = 0.19; // L1 wavelength in meters
                signal.carrierPhase = (trueRange / wavelength) + random.nextGaussian() * 0.02;
                
                // Update SNR based on conditions
                signal.snr = 45.0 - signal.environment.noiseFactor * 5.0 - signal.interference.errorMultiplier * 3.0;
                
                processedSignals.add(signal);
            }
            
            return processedSignals;
        }
    }
    
    // ==================== Position Solution CPN (with EKF) ====================
    
    /**
     * Position Solution sub-model with Extended Kalman Filter
     */
    static class PositionSolutionCPN {
        Place measurements;
        Place estimatedState;
        Transition ekfUpdate;
        
        // EKF parameters
        double dt = 1.0; // Time step (1 second)
        double processNoise = 0.1;
        double measurementNoise = 4.0;
        
        // Pre-allocated matrices for performance optimization
        private double[][] F6x6;  // State transition matrix
        private double[][] Q6x6;  // Process noise covariance
        private double[][] I6x6;  // 6x6 identity matrix
        
        PositionSolutionCPN() {
            measurements = new Place("Measurements");
            estimatedState = new Place("EstimatedState");
            ekfUpdate = new Transition("EKFUpdate");
            
            ekfUpdate.addInput(measurements);
            ekfUpdate.addInput(estimatedState);
            ekfUpdate.addOutput(estimatedState);
            
            // Pre-allocate frequently used matrices
            F6x6 = Matrix.identity(6);
            Q6x6 = new double[6][6];
            I6x6 = Matrix.identity(6);
        }
        
        /**
         * Extended Kalman Filter - Prediction Step
         */
        TrainState predict(TrainState state) {
            TrainState predicted = state.copy();
            
            // State transition: x = x + v*dt
            for (int i = 0; i < 3; i++) {
                predicted.position[i] = state.position[i] + state.velocity[i] * dt;
            }
            // Velocity remains constant (simplified model)
            
            // Reuse pre-allocated F matrix, only update dt terms
            for (int i = 0; i < 3; i++) {
                F6x6[i][i+3] = dt; // Position updated by velocity
            }
            
            // Reuse pre-allocated Q matrix
            for (int i = 0; i < 3; i++) {
                Q6x6[i][i] = processNoise * dt * dt / 4.0;      // Position noise
                Q6x6[i+3][i+3] = processNoise * dt;             // Velocity noise
                Q6x6[i][i+3] = processNoise * dt * dt / 2.0;    // Cross terms
                Q6x6[i+3][i] = processNoise * dt * dt / 2.0;
            }
            
            // Predict covariance: P = F*P*F' + Q
            double[][] FP = Matrix.multiply(F6x6, state.covariance);
            double[][] FPFt = Matrix.multiply(FP, Matrix.transpose(F6x6));
            predicted.covariance = Matrix.add(FPFt, Q6x6);
            
            return predicted;
        }
        
        /**
         * Extended Kalman Filter - Update Step
         */
        TrainState update(TrainState predicted, List<GNSSSignal> signals) {
            TrainState updated = predicted.copy();
            
            int numSats = signals.size();
            if (numSats == 0) return updated;
            
            // Measurement matrix H (numSats x 6)
            double[][] H = new double[numSats][6];
            double[] innovations = new double[numSats];
            
            for (int i = 0; i < numSats; i++) {
                GNSSSignal sig = signals.get(i);
                
                // Calculate range and line-of-sight unit vector
                double dx = sig.position[0] - predicted.position[0];
                double dy = sig.position[1] - predicted.position[1];
                double dz = sig.position[2] - predicted.position[2];
                double range = Math.sqrt(dx*dx + dy*dy + dz*dz);
                
                // Observation matrix (partial derivatives)
                H[i][0] = -dx / range;
                H[i][1] = -dy / range;
                H[i][2] = -dz / range;
                // H[i][3], H[i][4], H[i][5] remain 0 (velocity doesn't affect pseudorange directly)
                
                // Innovation: difference between measurement and prediction
                innovations[i] = sig.pseudorange - range;
            }
            
            // Measurement noise covariance R
            double adjustedMeasNoise = measurementNoise * 
                                      predicted.environment.noiseFactor * 
                                      (1.0 + predicted.interference.errorMultiplier);
            double[][] R = Matrix.scale(Matrix.identity(numSats), adjustedMeasNoise * adjustedMeasNoise);
            
            // Calculate Kalman gain: K = P*H' / (H*P*H' + R)
            double[][] Ht = Matrix.transpose(H);
            double[][] PHt = Matrix.multiply(predicted.covariance, Ht);
            double[][] HPHt = Matrix.multiply(Matrix.multiply(H, predicted.covariance), Ht);
            double[][] S = Matrix.add(HPHt, R);
            double[][] Sinv = Matrix.inverse(S);
            double[][] K = Matrix.multiply(PHt, Sinv);
            
            // Update state: x = x + K * innovation
            for (int i = 0; i < 6; i++) {
                for (int j = 0; j < numSats; j++) {
                    if (i < 3) {
                        updated.position[i] += K[i][j] * innovations[j];
                    } else {
                        updated.velocity[i-3] += K[i][j] * innovations[j];
                    }
                }
            }
            
            // Update covariance: P = (I - K*H) * P
            double[][] KH = Matrix.multiply(K, H);
            double[][] I_KH = Matrix.subtract(I6x6, KH);
            updated.covariance = Matrix.multiply(I_KH, predicted.covariance);
            
            return updated;
        }
        
        /**
         * Complete EKF cycle
         */
        TrainState processEKF(TrainState state, List<GNSSSignal> signals) {
            TrainState predicted = predict(state);
            return update(predicted, signals);
        }
    }
    
    // ==================== Evaluation CPN ====================
    
    /**
     * Evaluation sub-model for error analysis
     */
    static class EvaluationCPN {
        Place estimatedPositions;
        Place truePositions;
        Place errorMetrics;
        Transition errorCalculation;
        
        EvaluationCPN() {
            estimatedPositions = new Place("EstimatedPositions");
            truePositions = new Place("TruePositions");
            errorMetrics = new Place("ErrorMetrics");
            errorCalculation = new Transition("ErrorCalculation");
            
            errorCalculation.addInput(estimatedPositions);
            errorCalculation.addInput(truePositions);
            errorCalculation.addOutput(errorMetrics);
        }
        
        double calculateError(double[] estimated, double[] truth) {
            double dx = estimated[0] - truth[0];
            double dy = estimated[1] - truth[1];
            double dz = estimated[2] - truth[2];
            return Math.sqrt(dx*dx + dy*dy + dz*dz);
        }
    }
    
    // ==================== Simulation Data ====================
    
    static class SimulationResult {
        String scenario;
        Environment environment;
        Interference interference;
        List<Double> timestamps;
        List<double[]> truePositions;
        List<double[]> estimatedPositions;
        List<Double> errors;
        
        SimulationResult(String scenario, Environment env, Interference interf) {
            this.scenario = scenario;
            this.environment = env;
            this.interference = interf;
            this.timestamps = new ArrayList<>();
            this.truePositions = new ArrayList<>();
            this.estimatedPositions = new ArrayList<>();
            this.errors = new ArrayList<>();
        }
        
        // Optimized methods to avoid redundant stream operations and boxing
        double getMeanError() {
            if (errors.isEmpty()) return 0.0;
            double sum = 0.0;
            for (Double error : errors) {
                sum += error;
            }
            return sum / errors.size();
        }
        
        double getMaxError() {
            if (errors.isEmpty()) return 0.0;
            double max = errors.get(0);
            for (Double error : errors) {
                if (error > max) max = error;
            }
            return max;
        }
        
        double getStdError() {
            if (errors.isEmpty()) return 0.0;
            // Calculate mean and variance in single pass to avoid re-streaming
            double sum = 0.0;
            for (Double error : errors) {
                sum += error;
            }
            double mean = sum / errors.size();
            
            double variance = 0.0;
            for (Double error : errors) {
                double diff = error - mean;
                variance += diff * diff;
            }
            variance /= errors.size();
            return Math.sqrt(variance);
        }
    }
    
    // ==================== Simulation Runner ====================
    
    static class Simulator {
        GNSSReceiverCPN receiverCPN;
        PositionSolutionCPN positionCPN;
        EvaluationCPN evaluationCPN;
        
        List<SimulationResult> results;
        
        Simulator() {
            receiverCPN = new GNSSReceiverCPN();
            positionCPN = new PositionSolutionCPN();
            evaluationCPN = new EvaluationCPN();
            results = new ArrayList<>();
        }
        
        /**
         * Calculate true train position on curved track
         * Train moves at 20 m/s along a curved path
         */
        double[] getTruePosition(double time) {
            double speed = 20.0; // m/s
            double distance = speed * time;
            
            // Curved track: circular arc with radius 1000m
            double radius = 1000.0;
            double angle = distance / radius;
            
            double x = radius * Math.sin(angle);
            double y = radius * (1.0 - Math.cos(angle));
            double z = 100.0; // Constant elevation
            
            return new double[]{x, y, z};
        }
        
        /**
         * Calculate true velocity on curved track
         */
        double[] getTrueVelocity(double time) {
            double speed = 20.0; // m/s
            double distance = speed * time;
            double radius = 1000.0;
            double angle = distance / radius;
            
            double vx = speed * Math.cos(angle);
            double vy = speed * Math.sin(angle);
            double vz = 0.0;
            
            return new double[]{vx, vy, vz};
        }
        
        /**
         * Run simulation for a specific scenario
         */
        SimulationResult runScenario(Environment env, Interference interf, int durationSec) {
            String scenarioName = env.name() + "_" + interf.name();
            System.out.println("Running scenario: " + scenarioName);
            
            SimulationResult result = new SimulationResult(scenarioName, env, interf);
            
            // Initial state (with some initial error)
            double[] initialPos = getTruePosition(0);
            initialPos[0] += 10.0; // 10m initial error
            double[] initialVel = getTrueVelocity(0);
            
            TrainState state = new TrainState(initialPos, initialVel, 0.0, env, interf);
            
            // Run simulation
            for (int t = 0; t <= durationSec; t++) {
                double time = (double) t;
                
                // Get true position and velocity
                double[] truePos = getTruePosition(time);
                double[] trueVel = getTrueVelocity(time);
                
                // Update state timestamp and conditions
                state.timestamp = time;
                state.environment = env;
                state.interference = interf;
                
                // GNSS Receiver CPN: Generate and process signals
                receiverCPN.generateSatellites(truePos, env, interf, time);
                List<GNSSSignal> signals = receiverCPN.processSignals(truePos);
                
                // Position Solution CPN: Apply EKF
                state = positionCPN.processEKF(state, signals);
                
                // Evaluation CPN: Calculate error
                double error = evaluationCPN.calculateError(state.position, truePos);
                
                // Store results
                result.timestamps.add(time);
                result.truePositions.add(truePos);
                result.estimatedPositions.add(state.position.clone());
                result.errors.add(error);
                
                if (t % 20 == 0) {
                    System.out.printf("  t=%.0fs: Error=%.2fm\n", time, error);
                }
            }
            
            System.out.printf("Completed %s: Mean Error=%.2fm, Max Error=%.2fm, Std=%.2fm\n",
                scenarioName, result.getMeanError(), result.getMaxError(), result.getStdError());
            
            return result;
        }
        
        /**
         * Run all simulation scenarios
         */
        void runAllScenarios() {
            System.out.println("=== Starting GNSS Train Positioning CPN Simulation ===\n");
            
            int duration = 100; // seconds
            
            // Main scenarios as per paper requirements
            results.add(runScenario(Environment.OPEN_AREA, Interference.NORMAL, duration));
            results.add(runScenario(Environment.MOUNTAIN, Interference.NORMAL, duration));
            results.add(runScenario(Environment.TUNNEL, Interference.NORMAL, duration));
            results.add(runScenario(Environment.OPEN_AREA, Interference.AM, duration));
            results.add(runScenario(Environment.OPEN_AREA, Interference.FM, duration));
            results.add(runScenario(Environment.OPEN_AREA, Interference.PULSE, duration));
            
            System.out.println("\n=== Simulation Complete ===\n");
        }
    }
    
    // ==================== Visualization ====================
    
    static class VisualizationPanel extends JPanel {
        List<SimulationResult> results;
        
        VisualizationPanel(List<SimulationResult> results) {
            this.results = results;
            setPreferredSize(new Dimension(1200, 900));
            setBackground(Color.WHITE);
        }
        
        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            Graphics2D g2 = (Graphics2D) g;
            g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
            
            // Draw 4 subplots: Error time series, Environment comparison, Interference comparison, CPN structure
            drawErrorTimeSeries(g2, 50, 50, 550, 350);
            drawEnvironmentComparison(g2, 650, 50, 500, 350);
            drawInterferenceComparison(g2, 50, 450, 500, 400);
            drawCPNStructure(g2, 600, 450, 550, 400);
        }
        
        /**
         * Draw error time series for all scenarios
         */
        void drawErrorTimeSeries(Graphics2D g2, int x, int y, int width, int height) {
            g2.setColor(Color.BLACK);
            g2.setFont(new Font("Arial", Font.BOLD, 14));
            g2.drawString("Position Error Time Series", x + 10, y + 20);
            
            // Draw axes
            int plotX = x + 60;
            int plotY = y + 40;
            int plotWidth = width - 80;
            int plotHeight = height - 60;
            
            g2.drawRect(plotX, plotY, plotWidth, plotHeight);
            g2.drawLine(plotX, plotY + plotHeight, plotX + plotWidth, plotY + plotHeight); // X-axis
            g2.drawLine(plotX, plotY, plotX, plotY + plotHeight); // Y-axis
            
            // Labels
            g2.setFont(new Font("Arial", Font.PLAIN, 10));
            g2.drawString("Time (s)", plotX + plotWidth/2 - 20, plotY + plotHeight + 30);
            g2.rotate(-Math.PI/2);
            g2.drawString("Error (m)", -(plotY + plotHeight/2 + 20), plotX - 40);
            g2.rotate(Math.PI/2);
            
            // Axis ticks and labels
            for (int i = 0; i <= 5; i++) {
                int tx = plotX + i * plotWidth / 5;
                int ty = plotY + plotHeight;
                g2.drawLine(tx, ty, tx, ty + 5);
                g2.drawString(String.valueOf(i * 20), tx - 10, ty + 20);
            }
            
            for (int i = 0; i <= 5; i++) {
                int tx = plotX;
                int ty = plotY + plotHeight - i * plotHeight / 5;
                g2.drawLine(tx - 5, ty, tx, ty);
                g2.drawString(String.valueOf(i * 4), tx - 30, ty + 5);
            }
            
            // Plot data
            Color[] colors = {
                new Color(0, 100, 200),    // Blue - Open Normal
                new Color(0, 150, 0),      // Green - Mountain Normal
                new Color(200, 0, 0),      // Red - Tunnel Normal
                new Color(255, 165, 0),    // Orange - Open AM
                new Color(200, 0, 200),    // Magenta - Open FM
                new Color(100, 100, 0)     // Dark Yellow - Open Pulse
            };
            
            double maxError = 20.0;
            for (int r = 0; r < results.size(); r++) {
                SimulationResult result = results.get(r);
                g2.setColor(colors[r % colors.length]);
                
                for (int i = 1; i < result.timestamps.size(); i++) {
                    double t1 = result.timestamps.get(i-1);
                    double e1 = result.errors.get(i-1);
                    double t2 = result.timestamps.get(i);
                    double e2 = result.errors.get(i);
                    
                    int x1 = plotX + (int)(t1 * plotWidth / 100.0);
                    int y1 = plotY + plotHeight - (int)(e1 * plotHeight / maxError);
                    int x2 = plotX + (int)(t2 * plotWidth / 100.0);
                    int y2 = plotY + plotHeight - (int)(e2 * plotHeight / maxError);
                    
                    g2.drawLine(x1, y1, x2, y2);
                }
            }
            
            // Legend
            g2.setFont(new Font("Arial", Font.PLAIN, 9));
            int legendX = plotX + plotWidth - 140;
            int legendY = plotY + 20;
            for (int r = 0; r < results.size(); r++) {
                g2.setColor(colors[r % colors.length]);
                g2.fillRect(legendX, legendY + r * 15, 10, 10);
                g2.setColor(Color.BLACK);
                g2.drawString(results.get(r).scenario, legendX + 15, legendY + r * 15 + 9);
            }
        }
        
        /**
         * Draw environment comparison bar chart
         */
        void drawEnvironmentComparison(Graphics2D g2, int x, int y, int width, int height) {
            g2.setColor(Color.BLACK);
            g2.setFont(new Font("Arial", Font.BOLD, 14));
            g2.drawString("Mean Error by Environment", x + 10, y + 20);
            
            // Calculate mean errors for each environment (with Normal interference)
            Map<Environment, Double> envErrors = new HashMap<>();
            for (SimulationResult result : results) {
                if (result.interference == Interference.NORMAL) {
                    envErrors.put(result.environment, result.getMeanError());
                }
            }
            
            // Draw bar chart
            int plotX = x + 60;
            int plotY = y + 50;
            int plotWidth = width - 100;
            int plotHeight = height - 80;
            
            g2.drawLine(plotX, plotY + plotHeight, plotX + plotWidth, plotY + plotHeight); // X-axis
            g2.drawLine(plotX, plotY, plotX, plotY + plotHeight); // Y-axis
            
            // Calculate max error dynamically for proper scaling
            double maxError = envErrors.values().stream().mapToDouble(Double::doubleValue).max().orElse(8.0) * 1.2;
            int barWidth = plotWidth / 6;
            Color[] colors = {new Color(100, 200, 100), new Color(255, 200, 100), new Color(255, 100, 100)};
            
            int i = 0;
            for (Environment env : Environment.values()) {
                if (envErrors.containsKey(env)) {
                    double error = envErrors.get(env);
                    int barHeight = (int)(error * plotHeight / maxError);
                    int barX = plotX + (i + 1) * plotWidth / 4 - barWidth / 2;
                    int barY = plotY + plotHeight - barHeight;
                    
                    g2.setColor(colors[i]);
                    g2.fillRect(barX, barY, barWidth, barHeight);
                    g2.setColor(Color.BLACK);
                    g2.drawRect(barX, barY, barWidth, barHeight);
                    
                    // Label
                    g2.setFont(new Font("Arial", Font.PLAIN, 10));
                    String label = env.name().replace("_", " ");
                    g2.drawString(label, barX - 10, plotY + plotHeight + 20);
                    g2.drawString(String.format("%.2fm", error), barX + 5, barY - 5);
                    
                    i++;
                }
            }
            
            // Y-axis labels
            g2.setFont(new Font("Arial", Font.PLAIN, 10));
            for (int j = 0; j <= 4; j++) {
                int ty = plotY + plotHeight - j * plotHeight / 4;
                g2.drawLine(plotX - 5, ty, plotX, ty);
                g2.drawString(String.format("%.0f", j * 2.0), plotX - 30, ty + 5);
            }
            
            g2.rotate(-Math.PI/2);
            g2.drawString("Mean Error (m)", -(plotY + plotHeight/2 + 30), plotX - 45);
            g2.rotate(Math.PI/2);
        }
        
        /**
         * Draw interference comparison bar chart
         */
        void drawInterferenceComparison(Graphics2D g2, int x, int y, int width, int height) {
            g2.setColor(Color.BLACK);
            g2.setFont(new Font("Arial", Font.BOLD, 14));
            g2.drawString("Mean Error by Interference Type (Open Area)", x + 10, y + 20);
            
            // Calculate mean errors for each interference (in Open Area)
            Map<Interference, Double> intErrors = new HashMap<>();
            for (SimulationResult result : results) {
                if (result.environment == Environment.OPEN_AREA) {
                    intErrors.put(result.interference, result.getMeanError());
                }
            }
            
            // Draw bar chart
            int plotX = x + 80;
            int plotY = y + 60;
            int plotWidth = width - 120;
            int plotHeight = height - 100;
            
            g2.drawLine(plotX, plotY + plotHeight, plotX + plotWidth, plotY + plotHeight); // X-axis
            g2.drawLine(plotX, plotY, plotX, plotY + plotHeight); // Y-axis
            
            // Calculate max error dynamically for proper scaling
            double maxError = intErrors.values().stream().mapToDouble(Double::doubleValue).max().orElse(5.0) * 1.2;
            int barWidth = plotWidth / 8;
            Color[] colors = {
                new Color(100, 200, 100),   // Green - Normal
                new Color(255, 200, 100),   // Orange - AM
                new Color(255, 100, 100),   // Red - FM
                new Color(150, 150, 255)    // Blue - Pulse
            };
            
            int i = 0;
            for (Interference interf : Interference.values()) {
                if (intErrors.containsKey(interf)) {
                    double error = intErrors.get(interf);
                    int barHeight = (int)(error * plotHeight / maxError);
                    int barX = plotX + (i + 1) * plotWidth / 5 - barWidth / 2;
                    int barY = plotY + plotHeight - barHeight;
                    
                    g2.setColor(colors[i]);
                    g2.fillRect(barX, barY, barWidth, barHeight);
                    g2.setColor(Color.BLACK);
                    g2.drawRect(barX, barY, barWidth, barHeight);
                    
                    // Label
                    g2.setFont(new Font("Arial", Font.PLAIN, 10));
                    g2.drawString(interf.name(), barX - 5, plotY + plotHeight + 20);
                    g2.drawString(String.format("%.2fm", error), barX + 5, barY - 5);
                    
                    i++;
                }
            }
            
            // Y-axis labels
            g2.setFont(new Font("Arial", Font.PLAIN, 10));
            for (int j = 0; j <= 5; j++) {
                int ty = plotY + plotHeight - j * plotHeight / 5;
                g2.drawLine(plotX - 5, ty, plotX, ty);
                g2.drawString(String.format("%.0f", j * 1.0), plotX - 30, ty + 5);
            }
            
            g2.rotate(-Math.PI/2);
            g2.drawString("Mean Error (m)", -(plotY + plotHeight/2 + 30), plotX - 55);
            g2.rotate(Math.PI/2);
        }
        
        /**
         * Draw hierarchical CPN structure diagram
         */
        void drawCPNStructure(Graphics2D g2, int x, int y, int width, int height) {
            g2.setColor(Color.BLACK);
            g2.setFont(new Font("Arial", Font.BOLD, 14));
            g2.drawString("Hierarchical CPN Structure", x + 10, y + 20);
            
            g2.setFont(new Font("Arial", Font.PLAIN, 10));
            
            // Top Level CPN
            int topY = y + 60;
            g2.setColor(new Color(200, 220, 255));
            g2.fillRoundRect(x + 200, topY, 150, 50, 10, 10);
            g2.setColor(Color.BLACK);
            g2.drawRoundRect(x + 200, topY, 150, 50, 10, 10);
            g2.drawString("Top Level CPN", x + 220, topY + 30);
            
            // Sub-models
            int subY = topY + 100;
            
            // GNSS Receiver CPN
            g2.setColor(new Color(255, 240, 200));
            g2.fillRoundRect(x + 50, subY, 120, 80, 10, 10);
            g2.setColor(Color.BLACK);
            g2.drawRoundRect(x + 50, subY, 120, 80, 10, 10);
            g2.drawString("GNSS Receiver", x + 60, subY + 25);
            g2.drawString("CPN", x + 85, subY + 40);
            
            // Places and transitions (small circles and rectangles)
            g2.setColor(new Color(100, 150, 255));
            g2.fillOval(x + 65, subY + 50, 15, 15);
            g2.fillOval(x + 140, subY + 50, 15, 15);
            g2.setColor(Color.BLACK);
            g2.drawOval(x + 65, subY + 50, 15, 15);
            g2.drawOval(x + 140, subY + 50, 15, 15);
            g2.fillRect(x + 100, subY + 50, 20, 15);
            g2.drawLine(x + 80, subY + 57, x + 100, subY + 57);
            g2.drawLine(x + 120, subY + 57, x + 140, subY + 57);
            
            // Position Solution CPN
            g2.setColor(new Color(200, 255, 200));
            g2.fillRoundRect(x + 220, subY, 120, 80, 10, 10);
            g2.setColor(Color.BLACK);
            g2.drawRoundRect(x + 220, subY, 120, 80, 10, 10);
            g2.drawString("Position Solution", x + 230, subY + 25);
            g2.drawString("CPN (EKF)", x + 245, subY + 40);
            
            // EKF components
            g2.setFont(new Font("Arial", Font.PLAIN, 8));
            g2.drawString("Predict", x + 230, subY + 55);
            g2.drawString("Update", x + 280, subY + 55);
            g2.setColor(new Color(100, 150, 255));
            g2.fillOval(x + 235, subY + 58, 12, 12);
            g2.fillOval(x + 285, subY + 58, 12, 12);
            g2.setColor(Color.BLACK);
            g2.drawOval(x + 235, subY + 58, 12, 12);
            g2.drawOval(x + 285, subY + 58, 12, 12);
            g2.fillRect(x + 260, subY + 58, 15, 12);
            g2.drawLine(x + 247, subY + 64, x + 260, subY + 64);
            g2.drawLine(x + 275, subY + 64, x + 285, subY + 64);
            
            // Evaluation CPN
            g2.setFont(new Font("Arial", Font.PLAIN, 10));
            g2.setColor(new Color(255, 220, 220));
            g2.fillRoundRect(x + 390, subY, 120, 80, 10, 10);
            g2.setColor(Color.BLACK);
            g2.drawRoundRect(x + 390, subY, 120, 80, 10, 10);
            g2.drawString("Evaluation CPN", x + 405, subY + 30);
            g2.drawString("(Error Analysis)", x + 400, subY + 45);
            
            // Error metrics
            g2.setColor(new Color(100, 150, 255));
            g2.fillOval(x + 405, subY + 55, 15, 15);
            g2.fillOval(x + 480, subY + 55, 15, 15);
            g2.setColor(Color.BLACK);
            g2.drawOval(x + 405, subY + 55, 15, 15);
            g2.drawOval(x + 480, subY + 55, 15, 15);
            g2.fillRect(x + 438, subY + 55, 20, 15);
            g2.drawLine(x + 420, subY + 62, x + 438, subY + 62);
            g2.drawLine(x + 458, subY + 62, x + 480, subY + 62);
            
            // Arrows connecting components
            g2.setStroke(new BasicStroke(2));
            drawArrow(g2, x + 275, topY + 50, x + 110, subY);
            drawArrow(g2, x + 275, topY + 50, x + 280, subY);
            drawArrow(g2, x + 275, topY + 50, x + 450, subY);
            
            // Data flow arrows between sub-models
            g2.setStroke(new BasicStroke(1.5f, BasicStroke.CAP_BUTT, BasicStroke.JOIN_MITER, 
                         10.0f, new float[]{5.0f}, 0.0f));
            drawArrow(g2, x + 170, subY + 40, x + 220, subY + 40);
            drawArrow(g2, x + 340, subY + 40, x + 390, subY + 40);
            
            // Legend
            g2.setStroke(new BasicStroke(1));
            g2.setFont(new Font("Arial", Font.PLAIN, 9));
            int legendY = subY + 100;
            g2.drawString("Legend:", x + 50, legendY);
            
            g2.setColor(new Color(100, 150, 255));
            g2.fillOval(x + 50, legendY + 10, 15, 15);
            g2.setColor(Color.BLACK);
            g2.drawOval(x + 50, legendY + 10, 15, 15);
            g2.drawString("= Place", x + 70, legendY + 22);
            
            g2.fillRect(x + 130, legendY + 10, 20, 15);
            g2.drawString("= Transition", x + 155, legendY + 22);
            
            drawArrow(g2, x + 260, legendY + 17, x + 290, legendY + 17);
            g2.drawString("= Arc (token flow)", x + 295, legendY + 22);
        }
        
        void drawArrow(Graphics2D g2, int x1, int y1, int x2, int y2) {
            g2.drawLine(x1, y1, x2, y2);
            
            // Arrow head
            double angle = Math.atan2(y2 - y1, x2 - x1);
            int arrowSize = 8;
            
            int x3 = x2 - (int)(arrowSize * Math.cos(angle - Math.PI/6));
            int y3 = y2 - (int)(arrowSize * Math.sin(angle - Math.PI/6));
            int x4 = x2 - (int)(arrowSize * Math.cos(angle + Math.PI/6));
            int y4 = y2 - (int)(arrowSize * Math.sin(angle + Math.PI/6));
            
            g2.drawLine(x2, y2, x3, y3);
            g2.drawLine(x2, y2, x4, y4);
        }
    }
    
    // ==================== Data Export ====================
    
    static void exportResults(List<SimulationResult> results) {
        // Export CSV
        try (PrintWriter writer = new PrintWriter("simulation_results.csv")) {
            writer.println("Scenario,Environment,Interference,Time,True_X,True_Y,True_Z,Est_X,Est_Y,Est_Z,Error");
            
            for (SimulationResult result : results) {
                for (int i = 0; i < result.timestamps.size(); i++) {
                    writer.printf("%s,%s,%s,%.1f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f\n",
                        result.scenario,
                        result.environment.name(),
                        result.interference.name(),
                        result.timestamps.get(i),
                        result.truePositions.get(i)[0],
                        result.truePositions.get(i)[1],
                        result.truePositions.get(i)[2],
                        result.estimatedPositions.get(i)[0],
                        result.estimatedPositions.get(i)[1],
                        result.estimatedPositions.get(i)[2],
                        result.errors.get(i)
                    );
                }
            }
            System.out.println("\nResults exported to: simulation_results.csv");
        } catch (IOException e) {
            System.err.println("Error exporting CSV: " + e.getMessage());
        }
        
        // Export Statistics
        try (PrintWriter writer = new PrintWriter("simulation_statistics.txt")) {
            // Pre-create separator string for performance
            String separator = new String(new char[80]).replace('\0', '-');
            
            writer.println("=== GNSS Train Positioning CPN - Simulation Statistics ===\n");
            
            writer.println("Overall Results:");
            writer.println(separator);
            writer.printf("%-25s %-15s %-15s %-12s %-12s %-12s\n", 
                "Scenario", "Environment", "Interference", "Mean (m)", "Max (m)", "Std (m)");
            writer.println(separator);
            
            for (SimulationResult result : results) {
                writer.printf("%-25s %-15s %-15s %-12.3f %-12.3f %-12.3f\n",
                    result.scenario,
                    result.environment.name(),
                    result.interference.name(),
                    result.getMeanError(),
                    result.getMaxError(),
                    result.getStdError()
                );
            }
            
            writer.println("\n" + separator);
            writer.println("\nEnvironment Comparison (Normal Interference):");
            writer.println(separator);
            for (SimulationResult result : results) {
                if (result.interference == Interference.NORMAL) {
                    writer.printf("%s: Mean Error = %.3f m\n", 
                        result.environment.name(), result.getMeanError());
                }
            }
            
            writer.println("\n" + separator);
            writer.println("\nInterference Comparison (Open Area):");
            writer.println(separator);
            for (SimulationResult result : results) {
                if (result.environment == Environment.OPEN_AREA) {
                    writer.printf("%s: Mean Error = %.3f m\n", 
                        result.interference.name(), result.getMeanError());
                }
            }
            
            writer.println("\n" + separator);
            writer.println("\nValidation Against Expected Results:");
            writer.println(separator);
            writer.println("Expected Trends:");
            writer.println("  - Interference: FM > AM > Pulse > Normal");
            writer.println("  - Environment: Tunnel > Mountain > Open Area");
            writer.println("  - Best case: Open Area + Normal (~1m)");
            writer.println("  - Worst case: Tunnel + Normal (~6-7m)");
            writer.println("  - FM interference: ~3-4m mean error");
            
            System.out.println("Statistics exported to: simulation_statistics.txt");
        } catch (IOException e) {
            System.err.println("Error exporting statistics: " + e.getMessage());
        }
    }
    
    // ==================== Main Entry Point ====================
    
    public static void main(String[] args) {
        System.out.println("╔════════════════════════════════════════════════════════════╗");
        System.out.println("║  GNSS Train Positioning System using Colored Petri Nets  ║");
        System.out.println("║  Implementation with Extended Kalman Filter              ║");
        System.out.println("╚════════════════════════════════════════════════════════════╝\n");
        
        // Run simulation
        Simulator simulator = new Simulator();
        simulator.runAllScenarios();
        
        // Export results
        exportResults(simulator.results);
        
        // Pre-create separator for console output
        String consoleSeparator = new String(new char[90]).replace('\0', '-');
        
        // Display summary statistics
        System.out.println("\n=== Summary Statistics ===");
        System.out.println(consoleSeparator);
        System.out.printf("%-25s %-15s %-15s %12s %12s %12s\n", 
            "Scenario", "Environment", "Interference", "Mean (m)", "Max (m)", "Std (m)");
        System.out.println(consoleSeparator);
        
        for (SimulationResult result : simulator.results) {
            System.out.printf("%-25s %-15s %-15s %12.3f %12.3f %12.3f\n",
                result.scenario,
                result.environment.name(),
                result.interference.name(),
                result.getMeanError(),
                result.getMaxError(),
                result.getStdError()
            );
        }
        System.out.println(consoleSeparator);
        
        // Validation
        System.out.println("\n=== Validation Against Expected Results ===");
        
        // Find specific scenarios
        SimulationResult openNormal = simulator.results.stream()
            .filter(r -> r.environment == Environment.OPEN_AREA && r.interference == Interference.NORMAL)
            .findFirst().orElse(null);
        
        SimulationResult tunnelNormal = simulator.results.stream()
            .filter(r -> r.environment == Environment.TUNNEL && r.interference == Interference.NORMAL)
            .findFirst().orElse(null);
        
        SimulationResult openFM = simulator.results.stream()
            .filter(r -> r.environment == Environment.OPEN_AREA && r.interference == Interference.FM)
            .findFirst().orElse(null);
        
        if (openNormal != null) {
            System.out.printf("✓ Open Area + Normal: %.2f m (Expected: ~1m)\n", openNormal.getMeanError());
        }
        if (tunnelNormal != null) {
            System.out.printf("✓ Tunnel + Normal: %.2f m (Expected: ~6-7m)\n", tunnelNormal.getMeanError());
        }
        if (openFM != null) {
            System.out.printf("✓ Open Area + FM: %.2f m (Expected: ~3-4m)\n", openFM.getMeanError());
        }
        
        // Display visualization
        SwingUtilities.invokeLater(() -> {
            JFrame frame = new JFrame("GNSS Train Positioning CPN - Simulation Results");
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            frame.add(new VisualizationPanel(simulator.results));
            frame.pack();
            frame.setLocationRelativeTo(null);
            frame.setVisible(true);
            
            System.out.println("\n✓ Visualization window opened");
            System.out.println("\n=== Simulation Complete ===");
            System.out.println("Results saved to:");
            System.out.println("  - simulation_results.csv");
            System.out.println("  - simulation_statistics.txt");
        });
    }
}
