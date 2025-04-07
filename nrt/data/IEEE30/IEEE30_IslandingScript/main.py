from islanding_utils.networks import IEEE30_buses
from islanding_utils.gridEventManager import GridEventManager


if __name__ == "__main__":
        
    events =  { 
    } 

    ieee14 = GridEventManager(IEEE30_buses, events, stop_time=1000, name = "IEEE30", with_curves=True)   
    ieee14.initialize()
    ieee14.run()

     