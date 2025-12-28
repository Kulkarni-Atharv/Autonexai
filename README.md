# Paint Shop Simulation

A SimPy-based simulation of an automotive paint shop conveyor system to analyze throughput, identify bottlenecks, and optimize the process.

## Overview
This project simulates a paint shop with three sequential stations:
1.  **Cleaning Station**: 1 machine
2.  **Primer Station**: 2 machines
3.  **Painting Station**: 1 machine

Cars flow through these stations in order (Cleaning -> Primer -> Painting). The simulation runs for a 480-minute shift to measure performance metrics.

## Features
-   **Sequential Process Flow**: Enforces the order of operations.
-   **Resource Contention**: Models finite capacity of machines at each station.
-   **Bottleneck Detection**: Automatically alerts when a queue exceeds 3 cars.
-   **Metrics Collection**: Calculates:
    -   Total throughput (cars produced)
    -   Average time in system
    -   Station utilization
    -   Average wait times and maximum queue lengths

## Project Structure
-   `paint_shop_simulation/`:
    -   `main.py`: Entry point for the simulation.
    -   `config.py`: Configuration parameters (times, capacities).
    -   `monitor.py`: Logging and statistics tracking.
    -   `paint_shop.py`: Core simulation logic (Car and Station classes).
    -   `presentation.md`: Analysis of results and recommendations.

## Requirements
-   Python 3.x
-   `simpy`

## Installation
1.  Clone the repository:
    ```bash
    git clone https://github.com/Kulkarni-Atharv/Autonexai.git
    cd Autonexai
    ```
2.  Install dependencies:
    ```bash
    pip install simpy
    ```

## Usage
Run the simulation:
```bash
python paint_shop_simulation/main.py
```

## Example Output
```text
--- Starting Simulation for 480 minutes ---
...
[703.23] ALERT: Queue at Painting has 18 cars waiting!
...
--- Final Metrics ---
Total Cars Completed: 48
Alerts triggered: 4 times
Average Time in System: 651.24 minutes

--- Station Statistics ---
Station: Painting
  Max Queue Length: 23
  Avg Wait Time: 399.82 minutes
  Utilization: 96.93%
```

## Findings
The simulation consistently identifies the **Painting Station** as the primary bottleneck, with high utilization and long wait times. Adding a second painting machine is recommended to balance the line.
