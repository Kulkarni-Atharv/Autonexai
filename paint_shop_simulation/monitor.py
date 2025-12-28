import config

class Monitor:
    def __init__(self, env):
        self.env = env
        self.cars_finished = 0
        self.total_time_in_system = 0
        
        # Tracking metrics per station
        self.stations = ["Cleaning", "Primer", "Painting"]
        self.queue_stats = {s: {"max_len": 0, "total_wait": 0, "total_arrivals": 0} for s in self.stations}
        self.busy_time = {s: 0 for s in self.stations}
        self.total_alerts = 0

    def log(self, message):
        print(f"[{self.env.now:.2f}] {message}")

    def check_bottleneck(self, station_name, queue_len):
        """Check if queue length exceeds threshold and alert."""
        if queue_len > config.QUEUE_ALERT_THRESHOLD:
            self.total_alerts += 1
            self.log(f"ALERT: Queue at {station_name} has {queue_len} cars waiting!")

    def update_queue_stats(self, station_name, queue_len):
        if queue_len > self.queue_stats[station_name]["max_len"]:
            self.queue_stats[station_name]["max_len"] = queue_len
        self.check_bottleneck(station_name, queue_len)

    def record_wait_time(self, station_name, wait_time):
        self.queue_stats[station_name]["total_wait"] += wait_time
        self.queue_stats[station_name]["total_arrivals"] += 1

    def record_busy_time(self, station_name, duration):
        self.busy_time[station_name] += duration

    def record_car_finished(self, time_in_system):
        self.cars_finished += 1
        self.total_time_in_system += time_in_system
