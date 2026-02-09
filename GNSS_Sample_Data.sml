(* ====================================================== *)
(* GNSS Sample Data for Train Positioning Simulation     *)
(* ====================================================== *)

(* Sample GNSS signals with realistic parameters *)
val sampleSignal1 = {id=1, frequency=1575.42, amplitude=1.0, phase=0.0, snr=45.0};
val sampleSignal2 = {id=2, frequency=1575.42, amplitude=0.9, phase=0.5, snr=43.0};
val sampleSignal3 = {id=3, frequency=1575.42, amplitude=0.95, phase=1.0, snr=44.0};
val sampleSignal4 = {id=4, frequency=1575.42, amplitude=0.85, phase=1.5, snr=42.0};

(* Sample signal list *)
val sampleSignals = [sampleSignal1, sampleSignal2, sampleSignal3, sampleSignal4];

(* Sample coordinates representing train positions *)
val coord1 = {x=0.0, y=0.0, z=100.0, timestamp=0};
val coord2 = {x=100.0, y=80.0, z=100.0, timestamp=1};
val coord3 = {x=200.0, y=160.0, z=100.0, timestamp=2};
val coord4 = {x=300.0, y=240.0, z=100.0, timestamp=3};

(* Sample scenarios *)
val urbanScenario = {
  scenarioId=1,
  scenarioType="Urban",
  interferenceLevel=0.3,
  tunnelLength=0.0,
  mountainHeight=0.0
};

val tunnelScenario = {
  scenarioId=2,
  scenarioType="Tunnel",
  interferenceLevel=0.5,
  tunnelLength=500.0,
  mountainHeight=0.0
};

val mountainScenario = {
  scenarioId=3,
  scenarioType="Mountain",
  interferenceLevel=0.4,
  tunnelLength=0.0,
  mountainHeight=1500.0
};

val combinedScenario = {
  scenarioId=4,
  scenarioType="Combined",
  interferenceLevel=0.6,
  tunnelLength=300.0,
  mountainHeight=800.0
};

(* Sample initial state *)
val initialState = {
  position={x=0.0, y=0.0, z=100.0, timestamp=0},
  velocity=20.0,
  acceleration=0.5,
  covariance=1.0
};

(* Test data for validation *)
val testPositions = [
  {estimated={x=0.5, y=0.4, z=100.2, timestamp=0}, 
   actual={x=0.0, y=0.0, z=100.0, timestamp=0}, 
   error=0.64, timestamp=0},
  {estimated={x=100.3, y=80.2, z=100.1, timestamp=1}, 
   actual={x=100.0, y=80.0, z=100.0, timestamp=1}, 
   error=0.36, timestamp=1},
  {estimated={x=200.2, y=160.1, z=100.15, timestamp=2}, 
   actual={x=200.0, y=160.0, z=100.0, timestamp=2}, 
   error=0.25, timestamp=2}
];

(* Expected evaluation results according to paper *)
(* These values should be verified against Petrii.PDF *)
val expectedUrbanEvaluation = {
  scenario="Urban",
  meanError=2.5,
  maxError=5.0,
  rmsError=3.2,
  successRate=0.95
};

val expectedTunnelEvaluation = {
  scenario="Tunnel",
  meanError=8.5,
  maxError=15.0,
  rmsError=10.2,
  successRate=0.75
};

val expectedMountainEvaluation = {
  scenario="Mountain",
  meanError=6.0,
  maxError=12.0,
  rmsError=7.5,
  successRate=0.82
};

(* Helper function to print evaluation results *)
fun printEvaluation(eval: EVALUATION) =
  let
    val () = print("Scenario: " ^ #scenario eval ^ "\n")
    val () = print("Mean Error: " ^ Real.toString(#meanError eval) ^ " m\n")
    val () = print("Max Error: " ^ Real.toString(#maxError eval) ^ " m\n")
    val () = print("RMS Error: " ^ Real.toString(#rmsError eval) ^ " m\n")
    val () = print("Success Rate: " ^ Real.toString(#successRate eval) ^ "\n")
  in
    ()
  end;

(* Notes for validation:
   - Urban scenario: Low interference, good accuracy
   - Tunnel scenario: High signal loss, reduced accuracy
   - Mountain scenario: Moderate shadowing effects
   - Combined scenario: Multiple error sources
   
   Expected performance according to paper:
   - Urban: Mean error < 3m, Success rate > 90%
   - Tunnel: Mean error < 10m, Success rate > 70%
   - Mountain: Mean error < 8m, Success rate > 80%
*)
