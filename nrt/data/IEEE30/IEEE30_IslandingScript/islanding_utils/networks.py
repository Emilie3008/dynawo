IEEE14 = {
    "_BUS____1_SS" : {
        "_GEN____1_SM" : "connected",
        "_BUS____5_SS" : "_BUS____1-BUS____5-1_AC",
        "_BUS____2_SS" : "_BUS____1-BUS____2-1_AC"},

    "_BUS____2_SS" : {
        "_LOAD___2_EC" : "connected",
        "_GEN____2_SM" : "connected",
        "_BUS____1_SS" : "_BUS____1-BUS____2-1_AC",
        "_BUS____3_SS" : "_BUS____2-BUS____3-1_AC",
        "_BUS____4_SS" : "_BUS____2-BUS____4-1_AC",
        "_BUS____5_SS" : "_BUS____2-BUS____5-1_AC"},

    "_BUS____3_SS" : {
        "_LOAD___3_EC" : "connected",
        "_GEN____3_SM" : "connected",
        "_BUS____2_SS" : "_BUS____2-BUS____3-1_AC",
        "_BUS____4_SS" : "_BUS____3-BUS____4-1_AC"},

    "_BUS____4_SS" : {
        "_LOAD___4_EC" : "connected",
        "_BUS____2_SS" : "_BUS____2-BUS____4-1_AC",
        "_BUS____3_SS" : "_BUS____3-BUS____4-1_AC",
        "_BUS____5_SS" : "_BUS____4-BUS____5-1_AC",
        "_BUS____9_VL" : "_BUS____4-BUS____9-1_PT",
        "_BUS____7_VL" : "_BUS____4-BUS____7-1_PT", 
        
        },

    "_BUS____5_SS" : {
        "_LOAD___5_EC" : "connected",
        "_BUS____1_SS" : "_BUS____1-BUS____5-1_AC",
        "_BUS____2_SS" : "_BUS____2-BUS____5-1_AC",
        "_BUS____4_SS" : "_BUS____4-BUS____5-1_AC",
        "_BUS____6_VL" : "_BUS____5-BUS____6-1_PT",
        },

    "_BUS____6_VL" : {
        "_GEN____6_SM" : "connected", 
        "_LOAD___6_EC" : "connected", 
        "_BUS____5_SS" : "_BUS____5-BUS____6-1_PT", 
        "_BUS___11_SS" : "_BUS____6-BUS___11-1_AC",
        "_BUS___12_SS" : "_BUS____6-BUS___12-1_AC",
        "_BUS___13_SS" : "_BUS____6-BUS___13-1_AC"},

    "_BUS____7_VL" : {
        "_BUS____4_SS" : "_BUS____4-BUS____7-1_PT", 
        "_BUS____8_SS" : "_BUS____7-BUS____8-1_AC",
        "_BUS____9_VL" : "_BUS____7-BUS____9-1_AC"},

    "_BUS____8_SS" : {
        "_GEN____8_SM" : "connected",
        "_BUS____7_VL" : "_BUS____7-BUS____8-1_AC"},

    "_BUS____9_VL" : {
        "_LOAD___9_EC" : "connected", 
        "_BANK___9_SC" : "connected", 
        "_BUS____7_VL" : "_BUS____7-BUS____9-1_AC",
        "_BUS___10_SS" : "_BUS____9-BUS___10-1_AC",
        "_BUS___14_SS" : "_BUS____9-BUS___14-1_AC",
        "_BUS____4_SS" : "_BUS____4-BUS____9-1_PT"},

    "_BUS___10_SS" : {
        "_LOAD__10_EC" : "connected", 
        "_BUS___11_SS" : "_BUS___10-BUS___11-1_AC", 
        "_BUS____9_VL" : "_BUS____9-BUS___10-1_AC"}, 

    "_BUS___11_SS" : {
        "_LOAD__11_EC" : "connected",
        "_BUS___10_SS" : "_BUS___10-BUS___11-1_AC", 
        "_BUS____6_VL" : "_BUS____6-BUS___11-1_AC"},
     
    "_BUS___12_SS" : {
        "_LOAD__12_EC" : "connected", 
        "_BUS___13_SS" : "_BUS___12-BUS___13-1_AC",
        "_BUS___12_SS" : "_BUS____6-BUS___12-1_AC"},

    "_BUS___13_SS" : {
        "_LOAD__13_EC" : "connected", 
        "_BUS____6_VL" : "_BUS____6-BUS___13-1_AC",
        "_BUS___12_SS" : "_BUS___12-BUS___13-1_AC", 
        "_BUS___14_SS" : "_BUS___13-BUS___14-1_AC"},

    "_BUS___14_SS" : {
        "_LOAD__14_EC" : "connected", 
        "_BUS___13_SS" : "_BUS___13-BUS___14-1_AC",
        "_BUS____9_VL" : "_BUS____9-BUS___14-1_AC"}
}

IEEE30_buses={
     "VL1": {
         "VL2": "L-1-2-1", 
         "VL3":"L-1-3-1",
         "B1-G1": "connected"
        },

    "VL2": {
       "B2-G1": "connected",
       "B2-L1": "connected",
       "VL1": "L-1-2-1", 
       "VL4":"L-2-4-1",
       "VL5":"L-2-5-1",
       "VL6":"L-2-6-1"
        },

    "VL3": {
        "VL1":"L-1-3-1",
        "VL4":"L-3-4-1",
        "B3-L1": "connected"
    },

    "VL4": {
        "B4-L1": "connected",
        "VL3":"L-3-4-1",
        "VL2":"L-2-4-1",
        "VL6":"L-4-6-1",
        "VL12": "T-4-12-1"
    },
    "VL5":{
       "B5-L1": "connected",
       "VL2": "L-2-5-1",
       "VL7":"L-5-7-1"
    },

    "VL6":{
        "VL2":"L-2-6-1",
        "VL4":"L-4-6-1",
        "VL7": "L-6-7-1",
        'VL8':"L-6-8-1",
        "VL9": "T-6-9-1",
        "VL10": "T-6-10-1",
        "VL28":"L-6-28-1"
    },

    "VL7":{
        "B7-L1":"connected",
        "VL5":"L-5-7-1",
        "VL6":"L-6-7-1", 
    },

    "VL8":{
        "B8-L1": "connected",
        'VL6':"L-6-8-1",
        "VL28":"L-8-28-1"
    },

    "VL9":{
        "VL6" : "T-6-9-1",
        "VL10":"L-9-10-1",
        "VL11":"L-9-11-1"
    },

    "VL10":{
    
        "B10-SH 1" : "connected",
        "B10-L1": "connected",
        "VL6": "T-6-10-1",
        "VL9":"L-9-10-1",
        "VL20":"L-10-20-1",
        "VL17":"L-10-17-1",
        "VL21":"L-10-21-1", 
        "VL22":"L-10-22-1"
    },

    "VL11":{
        "VL9":"L-9-11-1"
    },

    "VL12":{
        "B12-L1": "connected",
        "VL4" : "T-4-12-1",
        "VL13":"L-12-13-1",
        "VL14":"L-12-14-1", #??? n'existe pas sur le schéma
        "VL15":"L-12-15-1",
        "VL16":"L-12-16-1"
    },

    "VL13":{
        "B13-G1":"connected",
        "VL12":"L-12-13-1", 
        # Connection avec VL14 ???
    },

    "VL14":{
        "B14-L1":"connected",
        "VL12":"L-12-14-1", 
        "VL15":"L-14-15-1"
    },

    "VL15":{
        "B15-L1":"connected",
        "VL12":"L-12-15-1", 
        "VL14":"L-14-15-1",
        "VL18":"L-15-18-1",
        "VL23":"L-15-23-1"
    },

    "VL16":{
        "B16-L1":"connected",
        "VL12":"L-12-16-1",
        "VL17":"L-16-17-1"
    },

    "VL17":{
        "B17-L1":"connected",
        "VL10":"L-10-17-1",
        "VL16":"L-16-17-1"
    },

    "VL18":{
        "B18-L1":"connected",
        "VL15":"L-15-18-1",
        "VL19":"L-18-19-1"
    },

    "VL19":{
        "B19-L1":"connected",
        "VL18":"L-18-19-1",
        "VL20":"L-19-20-1"
    },

    "VL20":{
        "B20-L1":"connected",
        "VL10":"L-10-20-1",
        "VL19":"L-19-20-1"
    },

    "VL21":{
        "B21-L1":"connected",
        "VL10":"L-10-21-1", 
        "VL22":"L-21-22-1"
    },

    "VL22":{
        "B22-G1":"connected",
        "VL10":"L-10-22-1",
        "VL21":"L-21-22-1",
        "VL24":"L-22-24-1"
    },

    "VL23":{
        "B23-G1":"connected",
        "B23-L1":"connected",
        "VL15":"L-15-23-1",
        "VL24":"L-23-24-1"
    },

    "VL24":{
        "B24-SH 1" : "connected",
        "B24-L1": "connected",
        "VL22":"L-22-24-1",
        "VL23":"L-23-24-1", 
        "VL25":"L-24-25-1"
    },

    "VL25": {  
        "VL24":"L-24-25-1", 
        "VL26":"L-25-26-1",
        "VL27":"L-25-27-1"
    },

    "VL26":{
        "B26-L1":"connected",
        "VL25":"L-25-26-1"
    },

    "VL27":{
        "B27-G1":"connected",
        "VL25" : "L-25-27-1",
        "VL28" : "T-28-27-1", 
        "VL29" : "L-27-29-1",
        "VL30" : "L-27-30-1"
    },
    "VL28":{
        "VL6":"L-6-28-1",
        "VL8":"L-8-28-1", 
        "VL27": "T-28-27-1"
    },
    "VL29":{
        "B29-L1":"connected",
        "VL27":"L-27-29-1", 
        "VL30":"L-29-30-1"
    },
    "VL30":{
        "B30-L1":"connected",
        "VL27":"L-27-30-1",
        "VL29":"L-29-30-1"
    }
}

IEEE30_lines = [
    "L-1-2-1", "L-1-3-1", "L-2-4-1", "L-2-5-1", "L-2-6-1",
    "L-3-4-1", "L-4-6-1", "L-5-7-1", "L-6-7-1", "L-6-8-1", 
    "L-6-28-1", "L-8-28-1", "L-9-10-1", "L-9-11-1", "L-10-17-1", 
    "L-10-20-1", "L-10-21-1", "L-10-22-1", "L-12-13-1", "L-12-14-1",
    "L-12-15-1", "L-12-16-1", "L-14-15-1", "L-15-18-1", "L-15-23-1",
    "L-16-17-1", "L-18-19-1", "L-19-20-1", "L-21-22-1", "L-22-24-1",
    "L-23-24-1", "L-24-25-1", "L-25-26-1", "L-25-27-1", "L-27-29-1",
    "L-27-30-1", "L-29-30-1"
]

IEEE30_tranfo = [
   "T-4-12-1",  "T-6-9-1", "T-6-10-1","T-28-27-1"
]
