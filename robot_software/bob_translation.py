# Takes the job object of the received JSON from the server, and returns a list
# of tuples (direction, distance) for bob to execute.
def extract(job):
    bobIns = []
    for j in job:
        command = j["command"]
        if(command == "move"):
            bobIns.append((j["parameters"]["direction"], j["parameters"]["blocks"]))
        elif(command == "lift"):
            bobIns.append(("L", j["parameters"]["height"]))
        elif(command == "grab"):
            bobIns.append(("G", 0))
    return bobIns