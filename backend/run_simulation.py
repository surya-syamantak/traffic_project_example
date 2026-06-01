import traci
import pandas as pd

# ==========================================
# SUMO Configuration
# ==========================================

sumoCmd = [
    "sumo-gui",
    "-c",
    "config/simulation.sumocfg"
]

traci.start(sumoCmd)

# ==========================================
# Check Traffic Lights
# ==========================================

traffic_lights = traci.trafficlight.getIDList()

if len(traffic_lights) == 0:
    print("No traffic lights found in the network!")
    traci.close()
    exit()

signal_id = traffic_lights[0]

print(f"Using Traffic Signal: {signal_id}")

# ==========================================
# Display Available Phases
# ==========================================

logic = traci.trafficlight.getAllProgramLogics(signal_id)

for program in logic:
    print(f"Number of Phases: {len(program.phases)}")

# ==========================================
# Fixed-Time Parameters
# ==========================================

GREEN_NS = 30
YELLOW_NS = 5
GREEN_EW = 30
YELLOW_EW = 5

CYCLE_LENGTH = (
    GREEN_NS +
    YELLOW_NS +
    GREEN_EW +
    YELLOW_EW
)

# ==========================================
# Runtime Data Storage
# ==========================================

runtime_data = []

step = 0

# ==========================================
# Simulation Loop
# ==========================================

while traci.simulation.getMinExpectedNumber() > 0:

    sim_time = traci.simulation.getTime()

    cycle = sim_time % CYCLE_LENGTH

    # --------------------------------------
    # Fixed-Time Signal Algorithm
    # --------------------------------------

    if cycle < GREEN_NS:
        desired_phase = 0

    elif cycle < GREEN_NS + YELLOW_NS:
        desired_phase = 1

    elif cycle < GREEN_NS + YELLOW_NS + GREEN_EW:
        desired_phase = 2

    else:
        desired_phase = 3

    current_phase = traci.trafficlight.getPhase(signal_id)

    if current_phase != desired_phase:
        traci.trafficlight.setPhase(
            signal_id,
            desired_phase
        )

    # --------------------------------------
    # Advance Simulation
    # --------------------------------------

    traci.simulationStep()

    vehicles = traci.vehicle.getIDList()

    total_speed = 0
    total_waiting = 0
    queue_length = 0

    for veh in vehicles:

        speed = traci.vehicle.getSpeed(veh)

        total_speed += speed

        waiting_time = traci.vehicle.getWaitingTime(veh)

        total_waiting += waiting_time

        # Queue Detection
        if speed <= 0.1:
            queue_length += 1

    # --------------------------------------
    # Calculate Statistics
    # --------------------------------------

    if len(vehicles) > 0:

        avg_speed = total_speed / len(vehicles)

        avg_waiting = total_waiting / len(vehicles)

    else:

        avg_speed = 0

        avg_waiting = 0

    # --------------------------------------
    # Store Data
    # --------------------------------------

    runtime_data.append({
        "step": step,
        "vehicles": len(vehicles),
        "avg_speed": avg_speed,
        "avg_waiting": avg_waiting,
        "queue_length": queue_length,
        "signal_phase": current_phase
    })

    # --------------------------------------
    # Console Output
    # --------------------------------------

    print(
        f"Step={step} | "
        f"Vehicles={len(vehicles)} | "
        f"AvgSpeed={avg_speed:.2f} m/s | "
        f"AvgWait={avg_waiting:.2f} s | "
        f"Queue={queue_length} | "
        f"Phase={current_phase}"
    )

    step += 1

# ==========================================
# End Simulation
# ==========================================

traci.close()

# ==========================================
# Save Results
# ==========================================

df = pd.DataFrame(runtime_data)

df.to_csv(
    "outputs/runtime_stats.csv",
    index=False
)

print("\nSimulation completed successfully!")
print("Results saved to outputs/runtime_stats.csv")