# Simulation Configuration

# Simulation Duration
SIM_TIME = 480  # minutes (8 hours)

# Car Arrival
ARRIVAL_MEAN = 10  # minutes (Average of 8-12)
ARRIVAL_MIN = 8
ARRIVAL_MAX = 12

# Station 1: Cleaning
CLEANING_MACHINES = 1
CLEANING_TIME_MIN = 15
CLEANING_TIME_MAX = 20

# Station 2: Primer
PRIMER_MACHINES = 2
PRIMER_TIME_MIN = 25
PRIMER_TIME_MAX = 35

# Station 3: Painting
PAINTING_MACHINES = 1
PAINTING_TIME_MIN = 30
PAINTING_TIME_MAX = 40

# Bottleneck Alert Threshold (Queue Length)
QUEUE_ALERT_THRESHOLD = 3
