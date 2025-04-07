from islanding_utils.networks import IEEE30_buses
from islanding_utils.gridEventManager import GridEventManager


if __name__ == "__main__":
        
    events =  { 
    } 

    ieee30 = GridEventManager(IEEE30_buses, events, stop_time=1000, name = "IEEE30", with_curves=True)   
    ieee30.initialize()
    ieee30.run()

     