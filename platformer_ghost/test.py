map_file = open("levels.txt", "r")
def make_map():
    for i in map_file.read().split("\n"):
        for j in i.split(","):
            if j == "w":

make_map()
map_file.close()