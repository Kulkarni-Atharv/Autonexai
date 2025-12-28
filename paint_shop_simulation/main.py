import simpy
import config
from monitor import Monitor
from paint_shop import PaintShop, car_generator

def main():
    # Setup SimPy environment
    env = simpy.Environment()
    
    # Initialize Monitor and PaintShop
    monitor = Monitor(env)
    shop = PaintShop(env, monitor)
    
    print(f"--- Starting Simulation for {config.SIM_TIME} minutes ---")
    
    # Start the car generator
    env.process(car_generator(env, shop))
    
    # Run the simulation
    # We run until there are no more events. 
    # The car_generator stops generating at SIM_TIME, so this will continue
    # until the last car finishes processing.
    env.run()
    
    print(f"\n--- Simulation Ends at {env.now:.2f} minutes ---")
    
    # Report Metrics
    print("\n--- Final Metrics ---")
    print(f"Total Cars Completed: {monitor.cars_finished}")
    print(f"Alerts triggered: {monitor.total_alerts} times")
    
    if monitor.cars_finished > 0:
        avg_time = monitor.total_time_in_system / monitor.cars_finished
        print(f"Average Time in System: {avg_time:.2f} minutes")
    else:
        print("Average Time in System: N/A")

    print("\n--- Station Statistics ---")
    total_sim_time = env.now
    
    for station in monitor.stations:
        stats = monitor.queue_stats[station]
        busy_time = monitor.busy_time[station]
        
        # Calculate Utilization: Busy Time / (Total Time * machines)
        # Note: We need machine counts from config to calculate correctly
        if station == "Cleaning":
            machines = config.CLEANING_MACHINES
        elif station == "Primer":
            machines = config.PRIMER_MACHINES
        elif station == "Painting":
            machines = config.PAINTING_MACHINES
        else:
            machines = 1
            
        utilization = (busy_time / (total_sim_time * machines)) * 100
        
        avg_wait = stats["total_wait"] / stats["total_arrivals"] if stats["total_arrivals"] > 0 else 0
        
        print(f"Station: {station}")
        print(f"  Max Queue Length: {stats['max_len']}")
        print(f"  Avg Wait Time: {avg_wait:.2f} minutes")
        print(f"  Utilization: {utilization:.2f}%")

if __name__ == "__main__":
    main()
