import simpy
import random
import config

class Car:
    def __init__(self, car_id, env):
        self.id = car_id
        self.env = env
        self.arrival_time = env.now
        self.start_times = {}
        self.end_times = {}

class PaintShop:
    def __init__(self, env, monitor):
        self.env = env
        self.monitor = monitor
        
        # Resources for each station
        self.cleaning_station = simpy.Resource(env, capacity=config.CLEANING_MACHINES)
        self.primer_station = simpy.Resource(env, capacity=config.PRIMER_MACHINES)
        self.painting_station = simpy.Resource(env, capacity=config.PAINTING_MACHINES)

    def process_car(self, car):
        """Pipeline process: Cleaning -> Primer -> Painting"""
        self.monitor.log(f"Car {car.id} arrived.")
        
        # 1. Cleaning Station
        yield from self._run_station(car, "Cleaning", self.cleaning_station, 
                                     config.CLEANING_TIME_MIN, config.CLEANING_TIME_MAX)

        # 2. Primer Station
        yield from self._run_station(car, "Primer", self.primer_station, 
                                     config.PRIMER_TIME_MIN, config.PRIMER_TIME_MAX)

        # 3. Painting Station
        yield from self._run_station(car, "Painting", self.painting_station, 
                                     config.PAINTING_TIME_MIN, config.PAINTING_TIME_MAX)

        # Exit System
        total_time = self.env.now - car.arrival_time
        self.monitor.log(f"Car {car.id} finished. Total time: {total_time:.2f}")
        self.monitor.record_car_finished(total_time)

    def _run_station(self, car, name, resource, min_time, max_time):
        """Generic function to handle processing at a station."""
        queue_len = len(resource.queue)
        self.monitor.update_queue_stats(name, queue_len) # Log queue before request

        request_time = self.env.now
        with resource.request() as req:
            yield req  # Wait for machine
            
            wait_time = self.env.now - request_time
            self.monitor.record_wait_time(name, wait_time)
            
            # Update queue stats again as we leave the queue
            self.monitor.update_queue_stats(name, len(resource.queue))

            start_time = self.env.now
            process_time = random.uniform(min_time, max_time)
            
            self.monitor.log(f"Car {car.id} starts {name} (Waited: {wait_time:.2f}).")
            yield self.env.timeout(process_time)
            self.monitor.log(f"Car {car.id} finishes {name}.")
            
            self.monitor.record_busy_time(name, process_time)

def car_generator(env, shop):
    """Generates cars coming into the system."""
    car_id = 1
    while True:
        # Stop generating cars if strictly passing 480 (optional check, 
        # but problem says 'Cars already in process at 480 must complete')
        # We can just let the simulation time limit handle the stop of NEW events,
        # but main.py will need to handle running until all finished.
        # Here we just generate indefinitely, main loop controls duration.
        if env.now >= config.SIM_TIME:
            break

        yield env.timeout(random.uniform(config.ARRIVAL_MIN, config.ARRIVAL_MAX))
        car = Car(car_id, env)
        env.process(shop.process_car(car))
        car_id += 1
