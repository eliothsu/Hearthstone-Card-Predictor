import json
from collections import Counter

def print_basic_info(filename):
    with open(filename) as data_file:    
        data = json.load(data_file)
    print(filename)
    print("Number of unique users: " + str(data["unique_users"]))
    print("Number of games: " + str(data["total_games"]))
    print("Number of games (hard count): " + str(len(data["games"])))

    c = Counter(data["games"][x]["mode"] for x in range(len(data["games"])))
    print(c)
    print()

print_basic_info("2017-10-18.json")
print_basic_info("2017-09.json")