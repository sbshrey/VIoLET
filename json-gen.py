import json
import random
import sys



num_devices = input("Total number of devices?\n")
num_pvt_networks = input("Number of Gateway/Fog devices?\n")
num_edge_devices = num_devices - num_pvt_networks
num_edge_per_network = (num_edge_devices/num_pvt_networks)
remanant = num_edge_devices % num_pvt_networks

devices_meta = {}

infra_config = {}
edge_device_types = {
    "Pi2B":{"cpus":"0.77"},
    "Pi3B":{"cpus":"1.18"}
}

fog_device_types = {
    "TX1":{"cpus":"2.27"},
    "SI":{"cpus":"6.57"}
}

sensor_types = json.load(open("dump/sensors.json"))

infra_config["edge_device_types"] = edge_device_types
infra_config["fog_device_types"] = fog_device_types
infra_config["sensor_types"] = sensor_types
devices_meta = {}

devices_meta["device_count"] = num_devices
Edge = {}
Edge["edge_device_count"] = num_edge_devices
e_type = edge_device_types.keys()
for  i in e_type:
    e = {}
    e["cpus"] = edge_device_types[i]["cpus"]
    e["count"] = input("Number of {0} devices?\n".format(i))
    Edge[i] = e

Fog = {}
Fog["fog_device_count"] = num_pvt_networks
f_type = fog_device_types.keys()
for i in f_type:
    f = {}
    f["cpus"] = fog_device_types[i]["cpus"]
    f["count"] = input("Number of {0} devices?\n".format(i))
    Fog[i] = f
devices_meta["Edge"] = Edge
devices_meta["Fog"] = Fog

num_sensors_per_device = input("number of sensors for each edge device?\n")
edge_denisty = input("edge_density for public networks\n")

print devices_meta

with open('dump/topo-devices-meta', 'w') as fd:
     fd.write(json.dumps(devices_meta))



print
print
print "Creating a network topology"

devices = {}
fog_types = []
edge_types = []
fog_devices = {}
edge_devices = {}


#CREATE FOG DEVICES
fog_types = devices_meta["Fog"].keys()
device_index = 1
for i in range(1,len(fog_types)):
    fog_type = fog_types[i]
    fog_type_count = devices_meta["Fog"][fog_type]["count"]
    for j in range(fog_type_count):
        device_type = {}
        fog_name = "Fog-{0}".format(device_index)
        device_index += 1
        device_type["device_type"] = fog_type
        fog_devices[fog_name] = device_type
devices["Fog"] = fog_devices

#CREATE EDGE DEVICES
edge_types = devices_meta["Edge"].keys()
subnet_index = 1
device_index = 1

#CREATE SENSORS
sensors = json.load(open("dump/sensors.json"))
sensor_types = []
for i in range(len(sensors["sensor_types"]["sensor"])):
    sensor_types.append(sensors["sensor_types"]["sensor"][i]["type"])

num_sensors = int(num_sensors_per_device / len(sensor_types))
rem = num_sensors + (num_sensors_per_device % len(sensor_types))
device_sensors = {}
for i in range(len(sensor_types)):
    if i == (len(sensor_types) - 1):
        device_sensors[sensor_types[i]] = str(rem)
    else:
        device_sensors[sensor_types[i]] = str(num_sensors)

for i in range(1,len(edge_types)):
    edge_type = edge_types[i]
    edge_type_count = devices_meta["Edge"][edge_type]["count"]
    for j in range(edge_type_count):
        device_type = {}
        edge_name = "Edge-{0}.{1}".format(subnet_index,device_index)
        if (device_index == num_edge_per_network):
            device_index = 1
            subnet_index += 1
        else:
            device_index += 1
        device_type["device_type"] = edge_type
        edge_devices[edge_name] = device_type
        edge_devices[edge_name]["sensors"] = device_sensors
devices["Edge"] = edge_devices
infra_config["devices"] = devices

num_edge_per_network = (num_edge_devices/num_pvt_networks)

#Create private networks
private_networks_dict = {}
BW = ["5","10","25","50"]
LATENCY = ["20","40","100","200"]
conn_dev = []
p = {}
for i in range(1, num_pvt_networks+1):
    p = {}
    conn_dev = []
    pvt = "violet-private-{0}".format(i)
    gw = "Fog-{0}".format(i)
    bw = BW[random.randint(0,3)]
    latency = LATENCY[random.randint(0,3)]
    if(i == num_pvt_networks and remanant != 0):
        num_edge_per_network += remanant
    for j in range(1, num_edge_per_network+1):
        e = "Edge-{0}.{1}".format(i,j)
        conn_dev.append(e)
    p["gw"] = gw
    p["bw"] = bw
    p["latency"] = latency
    p["conn_dev"] = conn_dev
    private_networks_dict[pvt]=p
infra_config["private_networks"] = private_networks_dict

#Create public networks
public_networks_dict = {}
BW = ["25","50","125","250"]
LATENCY = ["5","20","50","100"]
p = {}
conn_dev = []
pub = "violet-public-{0}".format(1)
bw = BW[random.randint(0,3)]
latency = LATENCY[random.randint(0,3)]
conn_dev = fog_devices.keys()
p["bw"] = bw
p["latency"] = latency
p["conn_dev"] = conn_dev
public_networks_dict[pub] = p
infra_config["public_networks"] = public_networks_dict

with open('infra-config.json', 'w') as fd:
    fd.write(json.dumps(infra_config))
