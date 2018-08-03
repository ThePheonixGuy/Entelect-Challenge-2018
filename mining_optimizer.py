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

def get_distance_from_start(distances, locations):
    for key, value in distances.items():
        mine_coord = locations[key]
        distance_from_start = distance([0,0], mine_coord)
        distances[key] = distances[key] + distance_from_start

    return distances

def get_isolation_bias(distances, locations):
    for key, value in distances.items():
        mine_coord = locations[key.lower()]
        for key, value in distances.items():
            distance_to_next_node = distance(mine_coord, locations[key])
            isolation_bias = distance_to_next_node / len(distances)
            distances[key] = distances[key] + isolation_bias
    return distances

def order_distances(distances):
    ordered = sorted(distances.items(), key=lambda x: x[1])
    return ordered


def allocate_workers(workers, work_list, distances):
    allocations = []
    non_valid_options = []
    current_worker = 0

    for x in range(workers):
        allocations.append([])
<<<<<<< HEAD
    print(work_list)
    for item in work_list:
        if item not in non_valid_options:
            pprint(distances)
            for key, value in distances.items():
                if key is not item:
                    result = distances[key] / distances [item[0]]
                    if 0.95 <= result <= 1.05:
                        # print("Cluster found: " + key )
                        if item not in non_valid_options:
                            allocations[current_worker].append(item)
                            non_valid_options.append(item)
            # allocations[current_worker].append(item)
        current_worker = current_worker + 1 if current_worker < workers - 1 else 0
            # non_valid_options.append(item)

    workers_list = []
    for index, worker_thread in enumerate(allocations):
        workers_list.append([])
        for index2, item in enumerate(worker_thread):
            workers_list[index].append(item[0])


    return workers_list
=======

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
    for x in range(workers):
        allocations.append([])

    for x in range(workers):
        for allocation in allocations:
            if len(allocation) <=0:
                if start_dists[0] not in non_valid_options:
                    allocation.append(start_dists[0])
                    non_valid_options.append(start_dists[0])
                last_allocation = allocation[-1]
                check_dist = depot_distances[last_allocation[0].lower()][0]

                for item in start_dists:
                    dist_from_start = distance([0,0], locations[check_dist[0]])
                    print(dist_from_start)

                    if check_dist[1] < dist_from_start:
                        print("going to nex tlocation is closer than dispatching new worker. continue")
                        break




>>>>>>> parent of 6e99674... New Allocation Algorithm

    print(allocations)

def print_allocations(allocations):
    string_list = []
    for worker in allocations:
        string_items = ""
        for item in worker:
            string_items += item + "," + item.lower() + ","
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

filename = "map_3.input"
workers, field_map = map_setup(filename)
location_dict = get_locations(field_map)
<<<<<<< HEAD
distance_dict = get_distances(location_dict)
distance_dict = get_distance_from_start(distance_dict, location_dict)
distance_dict = get_isolation_bias(distance_dict, location_dict)
orders = order_distances(distance_dict)
allocations = allocate_workers(workers, orders, distance_dict)
print_allocations(allocations)
=======
travel_distance_dict = get_distances(location_dict)
start_distance_dict = get_distance_from_start(travel_distance_dict, location_dict)
depot_distances = get_distance_to_next_depot(travel_distance_dict,location_dict)
new_allocations(workers, start_distance_dict, travel_distance_dict, depot_distances, location_dict)
# distance_dict = add_distance_from_start(distance_dict, location_dict)
# distance_dict = get_isolation_bias(distance_dict, location_dict)
#
# orders = order_distances(distance_dict)
# allocations = allocate_workers(workers, orders, distance_dict, depot_distances)
# print_allocations(allocations)
>>>>>>> parent of 6e99674... New Allocation Algorithm

tend = datetime.now()
print("Ended: " + str((tend - tstart).total_seconds()))
