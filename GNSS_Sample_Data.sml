(* ============================================ *)
(* GNSS Train Positioning System *)
(* Sample GNSS Signal Data for Simulation *)
(* ============================================ *)

(* Sample satellite data for epoch 1 *)
val sampleSat1 = {
    id = 1,
    psr = 20156234.567,
    psr_rate = -234.5,
    x = 15234567.89,
    y = 21456789.12,
    z = 18765432.10,
    vx = 1234.56,
    vy = -876.54,
    vz = 543.21,
    clk = 0.000123,
    azimuth = 45.6,
    elevation = 62.3,
    Rate_clock = 0.0000001
};

val sampleSat2 = {
    id = 2,
    psr = 22345678.90,
    psr_rate = -189.3,
    x = 18234567.89,
    y = 15456789.12,
    z = 21765432.10,
    vx = -987.65,
    vy = 1234.56,
    vz = -654.32,
    clk = 0.000098,
    azimuth = 120.4,
    elevation = 58.7,
    Rate_clock = 0.0000002
};

val sampleSat3 = {
    id = 3,
    psr = 21567890.12,
    psr_rate = -210.7,
    x = 12345678.90,
    y = 18765432.10,
    z = 22456789.12,
    vx = 876.54,
    vy = -543.21,
    vz = 1098.76,
    clk = 0.000145,
    azimuth = 230.1,
    elevation = 55.2,
    Rate_clock = 0.0000003
};

val sampleSat4 = {
    id = 4,
    psr = 23456789.01,
    psr_rate = -245.8,
    x = 19876543.21,
    y = 12345678.90,
    z = 20123456.78,
    vx = -654.32,
    vy = 987.65,
    vz = -765.43,
    clk = 0.000167,
    azimuth = 310.5,
    elevation = 48.9,
    Rate_clock = 0.0000004
};

val sampleSat5 = {
    id = 5,
    psr = 20987654.32,
    psr_rate = -198.6,
    x = 16543210.98,
    y = 20876543.21,
    z = 19234567.89,
    vx = 765.43,
    vy = -1098.76,
    vz = 876.54,
    clk = 0.000134,
    azimuth = 75.8,
    elevation = 70.1,
    Rate_clock = 0.0000005
};

val sampleSat6 = {
    id = 6,
    psr = 22876543.21,
    psr_rate = -223.4,
    x = 14567890.12,
    y = 22345678.90,
    z = 17876543.21,
    vx = 543.21,
    vy = -765.43,
    vz = 654.32,
    clk = 0.000156,
    azimuth = 165.3,
    elevation = 52.4,
    Rate_clock = 0.0000006
};

val sampleSat7 = {
    id = 7,
    psr = 21234567.89,
    psr_rate = -205.9,
    x = 17654321.09,
    y = 19234567.89,
    z = 21098765.43,
    vx = -1234.56,
    vy = 654.32,
    vz = -987.65,
    clk = 0.000189,
    azimuth = 280.7,
    elevation = 44.6,
    Rate_clock = 0.0000007
};

(* Create signal list for epoch 1 *)
val signalList1 = [sampleSat1, sampleSat2, sampleSat3, sampleSat4, sampleSat5, sampleSat6, sampleSat7];

(* SIGNALLIST format: (epoch, timestamp, signal_list) *)
val epoch1Data = (1, 1, signalList1);

(* Sample reference positions (ground truth) - UTM coordinates *)
(* Segment from Jing-Shen high-speed railway *)
val refPos1 = (1, (500234.567, 4456789.123, 85.5));
val refPos2 = (2, (500267.891, 4456812.456, 85.7));
val refPos3 = (3, (500301.234, 4456835.789, 85.9));
val refPos4 = (4, (500334.567, 4456859.012, 86.1));
val refPos5 = (5, (500367.890, 4456882.345, 86.3));

(* Mountain parameters for testing *)
val mountainTest1 = (100.0, 500.0);  (* Height: 100m, Distance: 500m *)
val mountainTest2 = (150.0, 300.0);  (* Height: 150m, Distance: 300m *)
val mountainTest3 = (200.0, 600.0);  (* Height: 200m, Distance: 600m *)

(* Test configurations for different scenarios *)

(* Configuration 1: Open Area - No Interference *)
val config_open_normal = {
    scenario = OpenArea,
    interference = Normal,
    bAM = false,
    bFM = false,
    bPulse = false
};

(* Configuration 2: Open Area - AM Interference *)
val config_open_am = {
    scenario = OpenArea,
    interference = AM,
    bAM = true,
    bFM = false,
    bPulse = false
};

(* Configuration 3: Open Area - FM Interference *)
val config_open_fm = {
    scenario = OpenArea,
    interference = FM,
    bAM = false,
    bFM = true,
    bPulse = false
};

(* Configuration 4: Open Area - Pulse Interference *)
val config_open_pulse = {
    scenario = OpenArea,
    interference = Pulse,
    bAM = false,
    bFM = false,
    bPulse = true
};

(* Configuration 5: Mountain Scenario *)
val config_mountain = {
    scenario = Mountain,
    interference = Normal,
    mountain = mountainTest1
};

(* Configuration 6: Tunnel Scenario *)
val config_tunnel = {
    scenario = Tunnel,
    tunnelState = InTunnel
};

(* Helper function to generate satellite data for multiple epochs *)
fun generateEpochData (startEpoch: int) (numEpochs: int) : SIGNALLIST list =
    let
        fun genSingleEpoch epoch =
            let
                val timeOffset = Real.fromInt epoch
                (* Simulate satellite movement and clock drift *)
                fun updateSat (sat: SIGNAL) =
                    {id = #id sat,
                     psr = #psr sat + #psr_rate sat * timeOffset,
                     psr_rate = #psr_rate sat,
                     x = #x sat + #vx sat * timeOffset,
                     y = #y sat + #vy sat * timeOffset,
                     z = #z sat + #vz sat * timeOffset,
                     vx = #vx sat,
                     vy = #vy sat,
                     vz = #vz sat,
                     clk = #clk sat + #Rate_clock sat * timeOffset,
                     azimuth = #azimuth sat,
                     elevation = #elevation sat,
                     Rate_clock = #Rate_clock sat}
                val updatedList = List.map updateSat signalList1
            in
                (epoch, epoch, updatedList)
            end
    in
        List.tabulate(numEpochs, fn i => genSingleEpoch (startEpoch + i))
    end;

(* Generate reference trajectory *)
fun generateReferenceTrajectory (startEpoch: int) (numEpochs: int) : COORDINATE list =
    let
        (* Initial position *)
        val (initEpoch, (initX, initY, initZ)) = refPos1
        (* Train velocity (approximately 300 km/h = 83.33 m/s) *)
        val velocity = 83.33
        (* Direction vector (normalized) - moving northeast *)
        val dirX = 0.6
        val dirY = 0.8
        val dirZ = 0.002  (* slight upward slope *)
        
        fun genPosition epoch =
            let
                val t = Real.fromInt (epoch - startEpoch)
                val newX = initX + dirX * velocity * t
                val newY = initY + dirY * velocity * t
                val newZ = initZ + dirZ * velocity * t
            in
                (epoch, (newX, newY, newZ))
            end
    in
        List.tabulate(numEpochs, fn i => genPosition (startEpoch + i))
    end;

(* Example: Generate 600 epochs of data (10 minutes) *)
val fullSimulationData = generateEpochData 1 600;
val fullReferenceTrajectory = generateReferenceTrajectory 1 600;

(* Test data for verification *)
val testData_10epochs = generateEpochData 1 10;
val testRef_10epochs = generateReferenceTrajectory 1 10;

(* Monitor function to check simulation progress *)
fun monitorProgress (epoch: int) (error: REAL) : unit =
    if epoch mod 60 = 0 then
        print ("Epoch " ^ Int.toString epoch ^ " - Error: " ^ Real.toString error ^ " m\n")
    else
        ();

(* Statistics calculation functions *)
fun calculateMean (values: REAL list) : REAL =
    let
        val sum = List.foldl op+ 0.0 values
        val count = Real.fromInt (List.length values)
    in
        sum / count
    end;

fun calculateStdDev (values: REAL list) : REAL =
    let
        val mean = calculateMean values
        val sqDiffs = List.map (fn v => (v - mean) * (v - mean)) values
        val variance = calculateMean sqDiffs
    in
        Math.sqrt variance
    end;

(* Result analysis structure *)
datatype SimulationResult = Result of {
    scenario: SCENARIO,
    interference: STATEINFE,
    meanError: REAL,
    stdDev: REAL,
    maxError: REAL,
    minError: REAL
};

(* Function to analyze simulation results *)
fun analyzeResults (errors: REAL list) (scenario: SCENARIO) (interference: STATEINFE) : SimulationResult =
    let
        val meanErr = calculateMean errors
        val stdErr = calculateStdDev errors
        val maxErr = List.foldl Real.max (List.hd errors) errors
        val minErr = List.foldl Real.min (List.hd errors) errors
    in
        Result {
            scenario = scenario,
            interference = interference,
            meanError = meanErr,
            stdDev = stdErr,
            maxError = maxErr,
            minError = minErr
        }
    end;

(* Export function for results *)
fun exportResults (result: SimulationResult) : string =
    case result of
        Result {scenario, interference, meanError, stdDev, maxError, minError} =>
            "Scenario: " ^ (case scenario of OpenArea => "Open Area" | Mountain => "Mountain" | Tunnel => "Tunnel") ^
            "\nInterference: " ^ (case interference of AM => "AM" | FM => "FM" | Pulse => "Pulse" | Normal => "Normal") ^
            "\nMean Error: " ^ Real.toString meanError ^ " m" ^
            "\nStd Deviation: " ^ Real.toString stdDev ^ " m" ^
            "\nMax Error: " ^ Real.toString maxError ^ " m" ^
            "\nMin Error: " ^ Real.toString minError ^ " m\n";
