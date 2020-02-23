from room import Room
from player import Player
from world import World
from util import Queue, Stack

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
graph = {}
visited = set()

while len(visited) < len(room_graph):
    current_room = player.current_room.id
    visited.add(current_room)

    if current_room not in graph:
        graph[current_room] = {}

        for exit in player.current_room.get_exits():
            graph[current_room][exit] = '?'

    unexplored_exits = []
    for k, v in graph[current_room].items():
        if v == '?':
            unexplored_exits.append(k)

    if len(unexplored_exits) > 0:
        direction = random.choice(unexplored_exits)
        player.travel(direction)
        graph[current_room][direction] = player.current_room.id
        traversal_path.append(direction)
    else:
        def back_track(graph, player):
            q = Queue()
            _visited = set()

            q.enqueue([(player.current_room.id, None)])

            while q.size() > 0:
                curr_path = q.dequeue()
                last_room = curr_path[-1][0]

                if '?' in graph[last_room].values():
                    path = []
                    for p in curr_path:
                        path.append(p[1])
                    return path

                if last_room not in _visited:
                    _visited.add(last_room)

                    for k,v in graph[last_room].items():
                        path_copy = list(curr_path)
                        path_copy.append((v, k))
                        q.enqueue(path_copy)

        back_list = back_track(graph, player)

        for d in back_list:
            player.travel(d)
            traversal_path.append(d)





# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")