from opcua import ua, Server
import time

# Setup our server
server = Server()

# Define the endpoint URL
url = "opc.tcp://localhost:4841/freeopcua/server/"
server.set_endpoint(url)

# Setup our own namespace, not really necessary but should be as informative as possible
name = "OPCUA_SIMULATION_SERVER"
addspace = server.register_namespace(name)

# Get Objects node, this is where we should put our nodes
objects = server.get_objects_node()

CoBotAGV_Now = objects.add_folder(addspace, "CoBotAGV_Now")
FN_ID_6000 = CoBotAGV_Now.add_object(addspace, "FN_ID_6000")
nns = FN_ID_6000.add_folder(addspace, "[NNS] - Natural Navigation Signals")
var1 = nns.add_variable(addspace, "Going to ID", 0)
var2 = nns.add_variable(addspace, "Heading", 0)
var3 = nns.add_variable(addspace, "Speed", 0)
var4 = nns.add_variable(addspace, "X-coordinate", 0)
var5 = nns.add_variable(addspace, "Y-coordinate", 0)
var1.set_writable()
var2.set_writable()
var3.set_writable()
var4.set_writable()
var5.set_writable()
ens = FN_ID_6000.add_folder(addspace, "[ENS] - Energy Signals")
var6 = ens.add_variable(addspace, "Battery value", 0)
var6.set_writable()
FN_ID_6100 = CoBotAGV_Now.add_object(addspace, "FN_ID_6100")
nnc = FN_ID_6100.add_folder(addspace, "[NNC] - Natural Navigation Command")
var7 = nnc.add_variable(addspace, "3005 - Go to destination - Destination ID", 1)
var8 = nnc.add_variable(addspace, "3005 - Go to destination - Trigger", 1)
var7.set_writable()
var8.set_writable()

# Populate our address space
# First a folder to organise our nodes
myobj = objects.add_object(addspace, "MyObject")

# Add a variable to our object
myvar = myobj.add_variable(addspace, "MyVariable", 6.7)
myvar.set_writable()    # Set MyVariable to be writable by clients



# Starting the server
server.start()
print(f"Server started at {url}")

try:
    while True:
        # Update the variable with some random values
        time.sleep(1)
        new_val = myvar.get_value() + 0.1
        print(f"New value: {new_val}")
        myvar.set_value(new_val)
finally:
    # Close the connection, cleanup
    server.stop()
    print("Server stopped")

