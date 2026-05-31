import traci
import pandas as pd

sumoCmd = [
    "sumo-gui",
    "-c",
    "config/simulation.sumocfg"
]

traci.start(sumoCmd)

runtime_data = []

step = 0

while traci.simulation.getMinExpectedNumber() > 0:

    traci.simulationStep()

    vehicles = traci.vehicle.getIDList()

    total_speed = 0
    total_waiting = 0

    for veh in vehicles:
        total_speed += traci.vehicle.getSpeed(veh)
        total_waiting += traci.vehicle.getWaitingTime(veh)

    avg_speed = 0
    avg_waiting = 0

    if len(vehicles) > 0:
        avg_speed = total_speed / len(vehicles)
        avg_waiting = total_waiting / len(vehicles)

    runtime_data.append({
        "step": step,
        "vehicles": len(vehicles),
        "avg_speed": avg_speed,
        "avg_waiting": avg_waiting
    })

    print(
        f"Step={step} "
        f"Vehicles={len(vehicles)} "
        f"AvgSpeed={avg_speed:.2f} "
        f"AvgWait={avg_waiting:.2f}"
    )

    step += 1

traci.close()

df = pd.DataFrame(runtime_data)
df.to_csv("outputs/runtime_stats.csv", index=False)

print("Simulation completed!")