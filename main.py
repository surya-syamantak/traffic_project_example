import os

print("===================================")
print("TRAFFIC SIMULATION PROJECT STARTED")
print("===================================")

# Step 1: Generate Routes
print("\nGenerating vehicle routes...")

route_result = os.system(
    'python "C:/Program Files (x86)/Eclipse/Sumo/tools/randomTrips.py" '
    '-n maps/city.net.xml '
    '-o routes/vehicles.trips.xml '
    '-r routes/vehicles.rou.xml '
    '-e 360'
)

if route_result != 0:
    print("Route generation failed!")
    exit()

# Step 2: Run Simulation
print("\nRunning SUMO simulation...")

simulation_result = os.system(
    "python backend/run_simulation.py"
)

if simulation_result != 0:
    print("Simulation failed!")
    exit()

# Step 3: Generate Statistics
print("\nGenerating statistics...")

stats_result = os.system(
    "python backend/statistics.py"
)

if stats_result != 0:
    print("Statistics generation failed!")
    exit()

print("\n===================================")
print("PROJECT COMPLETED SUCCESSFULLY")
print("===================================")