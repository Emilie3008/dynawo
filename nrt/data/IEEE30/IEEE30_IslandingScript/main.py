from islanding_utils.networks import IEEE30_buses
from islanding_utils.gridEventManager import GridEventManager


if __name__ == "__main__":
        
    events =  { 
        "T-4-12-1" : 100, 
        "T-6-9-1" : 100, 
        "T-6-10-1":100, 
        "T-28-27-1":100
    } 

    ieee30 = GridEventManager(IEEE30_buses, events, stop_time=3500, name = "IEEE30", with_curves=True)   
    ieee30.initialize()
    ieee30.run()