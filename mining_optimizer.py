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


def order_distances(distances):
    ordered = sorted(distances.items(), key=lambda x: x[1])
    return ordered


def allocate_workers(workers, work_list):
    allocations = []
    non_valid_options = []
    current_worker = 0

    for x in range(workers):
        allocations.append([])

    for item in work_list:
        if item not in non_valid_options:
            allocations[current_worker].append(item)
            current_worker = current_worker + 1 if current_worker < workers - 1 else 0
            non_valid_options.append(item)

    workers_list = []
    for index, worker_thread in enumerate(allocations):
        workers_list.append([])
        for index2, item in enumerate(worker_thread):
            workers_list[index].append(item[0])


    return workers_list

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

filename = "map_1.input"
workers, field_map = map_setup(filename)
pprint(field_map)
location_dict = get_locations(field_map)
pprint(location_dict)
distance_dict = get_distances(location_dict)
pprint(distance_dict)
orders = order_distances(distance_dict)
pprint(orders)
allocations = allocate_workers(workers, orders)
pprint(allocations)
print_allocations(allocations)

tend = datetime.now()
print("Ended: " + str((tend - tstart).total_seconds()))
