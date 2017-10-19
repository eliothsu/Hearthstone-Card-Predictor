import json
from collections import Counter

def print_basic_info(filename):
    with open(filename) as data_file:
        data = json.load(data_file)
    print(filename)
    print("Number of unique users: " + str(data["unique_users"]))
    # print("Number of games: " + str(data["total_games"]))
    print("Number of games (hard count): " + str(len(data["games"])))

    games = data["games"]
    c = Counter(games[x]["mode"] for x in range(len(games)))
    print(c)

    games = [game for game in games if game["mode"] == "ranked"]
    print("Number of ranked games: " + str(len(games)))

    game = games[0]
    card_history = game["card_history"]
    card_history = [card['card'] for card in card_history if card['player'] == "opponent"]
    card_history = [card for card in card_history if card['id'][-2:] != "t1" and card['id'] not in hero_powers]
    # card['id'][:3] != "CS2" and 
    print(card_history)

    print()

def parse_hero_powers(filename):
    with open(filename, encoding="utf-8") as data_file:
        data = json.load(data_file)
    print(filename)
    return [card["id"] for card in data if "type" in card and card["type"] == "HERO_POWER"]

hero_powers = parse_hero_powers("cards.json")

print_basic_info("2017-10-18.json")
print_basic_info("2017-09.json")