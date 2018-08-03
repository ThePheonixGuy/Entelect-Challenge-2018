from pprint import pprint
from datetime import datetime

tstart = datetime.now()
print("Started: 0")


def distance(loc1, loc2):
    return abs(loc2[0] - loc1[0]) + abs(loc2[1] - loc1[1])


def map_setup(filename):
    with open(filename) as f:
        content = f.readlines()

    content = [x.strip() for x in content]
    workers = content[0]
    content.remove(content[0])
    my_map = []
    for index, line in enumerate(content):
        my_map.insert(index, list(line))
    return int(workers), my_map


def get_locations(field_map):
    distance_dict = {}
    for index, line in enumerate(field_map):
        for letter_index, letter in enumerate(line):
            if letter != '#':
                distance_dict[letter] = [index, letter_index]

    return distance_dict


def get_distances(locations):
    distances = {}
    matched_letters = []
    corrected_letters = []
    for key in locations:
        if key.upper() not in matched_letters:
            if key.lower() not in matched_letters:
                matched_letters.append(key)

    for letter in matched_letters:
        corrected_letters.append(letter.upper())

    for letter in corrected_letters:
        mine = locations[letter.upper()]
        depot = locations[letter.lower()]
        distances[letter] = distance(mine, depot)

    return distances

def add_distance_from_start(distances, locations):
    for key, value in distances.items():
        mine_coord = locations[key]
        distance_from_start = distance([0,0], mine_coord)
        distances[key] = distances[key] + distance_from_start

    return distances

def get_distance_from_start(distances_dict, locations):
    distances = {}

    for key, loc in distances_dict.items():
        mine_coord = locations[key]
        distance_from_start = distance([0, 0], mine_coord)
        distances[key] = distance_from_start

    ordered = sorted(distances.items(), key=lambda x: x[1])
    return ordered

def get_isolation_bias(distances, locations):
    for key, value in distances.items():
        mine_coord = locations[key.lower()]
        for key, value in distances.items():
            distance_to_next_node = distance(mine_coord, locations[key])
            isolation_bias = (distance_to_next_node / len(distances))
            distances[key] = distances[key] + isolation_bias
    return distances

def get_distance_to_next_depot(distances, locations):
    depot_dict = {}
    mine_dict = {}
    for key, value in distances.items():
        if key.lower() not in depot_dict.keys():
            depot_dict[key.lower()] = locations[key.lower()]

        if key not in mine_dict.keys():
            mine_dict[key] = locations[key]

    for depot_key, depot_loc in depot_dict.items():
        depot_dict[depot_key] = {}
        for mine_key, mine_loc in mine_dict.items():
            result = distance(depot_loc, mine_loc)

            depot_dict[depot_key][mine_key] = result

    for depot_key, mine_dict in depot_dict.items():
        mine_ordered = order_distances(mine_dict)
        depot_dict[depot_key] = mine_ordered

    return depot_dict




def order_distances(distances):
    ordered = sorted(distances.items(), key=lambda x: x[1])
    return ordered


def allocate_workers(workers, work_list, distances, depot_disances):
    allocations = []
    non_valid_options = []
    current_worker = 0

    print(work_list)
    print(distances)

    for x in range(workers):
        allocations.append([])

        allocations[x].append(work_list[x])


    # for item in work_list:
    #     if item not in non_valid_options:
    #         for key, value in distances.items():
    #             if key is not item:
    #                 result = distances[key] / distances [item[0]]
    #                 if 0.95 <= result <= 1.05:
    #                     # print("Cluster found: " + key )
    #                     if item not in non_valid_options:
    #                         allocations[current_worker].append(item)
    #                         non_valid_options.append(item)
    #         # allocations[current_worker].append(item)
    #     current_worker = current_worker + 1 if current_worker < workers - 1 else 0
    #         # non_valid_options.append(item)
    #
    # workers_list = []
    # for index, worker_thread in enumerate(allocations):
    #     workers_list.append([])
    #     for index2, item in enumerate(worker_thread):
    #         workers_list[index].append(item[0])
    #
    #
    # return workers_list

def new_allocations(workers, start_dists, travel_dists, depot_distances, locations):
    allocations = []
    non_valid_options = []
    current_worker = 0
    pprint(dict(start_dists))
    pprint(depot_distances)
    for x in range(workers):
        allocations.append([])

    break_continue = False
    next_stop = start_dists[0]
    for x in range(workers):
        for allocation in allocations:
            # Worker specific List
            if next_stop[0] not in non_valid_options:
                allocation.append(next_stop)
                non_valid_options.append(next_stop[0])

            next_possible_stops = depot_distances[allocation[-1][0].lower()]
            for possible_stop in next_possible_stops:
                if possible_stop[0] not in non_valid_options:
                    print("Possible Stop found: " +str(possible_stop[0]))
                    next_stop = possible_stop
                    start_dists_dict = dict(start_dists)
                    if next_stop[1] < start_dists_dict[next_stop[0]]:
                        allocation.append(next_stop)
                        non_valid_options.append(next_stop[0])
                    else:
                        allocate_secondary_worker(allocations, x+1, next_stop, non_valid_options)

                # else:
                #     break
            break

    print(allocations)
    print(non_valid_options)
    print(next_possible_stops)
    return(allocations)


def allocate_secondary_worker(allocations, worker, work_unit, non_valid_options):
    if work_unit not in non_valid_options:
        allocations[worker].append(work_unit)
        non_valid_options.append(work_unit[0])



def print_allocations(allocations):
    string_list = []
    for worker in allocations:
        string_items = ""
        for item in worker:
            string_items += item[0] + "," + item[0].lower() + ","
        string_items = string_items[:-1]
        string_list.append(string_items)
    output = ""
    for item in string_list:
        output += item +"\n"

    local_filename = filename.split(".")
    local_filename = local_filename[0] +".output"

    with open(local_filename, "w") as f:
        f.write(output)
    print(local_filename)

filename = "map_1.input"
workers, field_map = map_setup(filename)
location_dict = get_locations(field_map)
travel_distance_dict = get_distances(location_dict)
start_distance_dict = get_distance_from_start(travel_distance_dict, location_dict)
depot_distances = get_distance_to_next_depot(travel_distance_dict,location_dict)
allocations = new_allocations(workers, start_distance_dict, travel_distance_dict, depot_distances, location_dict)
# distance_dict = add_distance_from_start(distance_dict, location_dict)
# distance_dict = get_isolation_bias(distance_dict, location_dict)
#
# orders = order_distances(distance_dict)
# allocations = allocate_workers(workers, orders, distance_dict, depot_distances)
print_allocations(allocations)

tend = datetime.now()
print("Ended: " + str((tend - tstart).total_seconds()))
