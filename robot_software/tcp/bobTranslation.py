# Takes the job object of the received JSON from the server, and returns a list
# of tuples (direction, distance) for bob to execute.
def extract(j):
    command = j["command"]
    if(command == "move"):
        return (j["parameters"]["direction"], j["parameters"]["blocks"])
    elif(command == "lift"):
        return ("L", j["parameters"]["height"])
    elif(command == "grab"):
        return ("G", 0)
    