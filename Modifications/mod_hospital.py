

# This code must be copied in the file "hospital.py" from H-Outbreak


# ADD THIS CALL AT THE END OF initialize_hospital() FUNCTION, JUST BEFORE THE LINE: return L
printHospital(L)

# ADD FUNCTION TO GET THE FILE "hospital.txt"
def printHospital(L):
    file = open('./hospital.txt', 'w')
    toWrite = ""
    for l in L:
        toWrite += "{},{}\n".format(l.id,l.name.value)
        if l.children is not None:
            toWrite += "children\n"
            for child in l.children:
                toWrite += "{},{}\n".format(child.id,child.name.value)
            toWrite += "children_end\n"
        if l.located_in is not None:
            parent = l.located_in
            toWrite += "parent\n"
            toWrite += "{},{}\n".format(parent.id,parent.name.value)
        if l.adjacent is not None:
            toWrite += "neighbours\n"
            for neighbour in l.adjacent:
                toWrite += "{},{}\n".format(neighbour.id,neighbour.name.value)
            toWrite += "neighbours_end\n"
    file.write(toWrite)
    file.close()