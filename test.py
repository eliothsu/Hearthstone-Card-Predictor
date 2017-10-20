import json
from collections import Counter
import operator

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
    final_data = {}
    paired_data = {}
    print("Number of ranked games: " + str(len(games)))

    all_cards = parse_cards("cards.json")
    hero_powers = parse_hero_powers("cards.json")
    id_to_name = {}
    for card in all_cards:
        if 'id' in card and 'name' in card:
            id_to_name[card['id']] = card['name']
            id_to_name[card['name']] = card['id']

    for game in games:
        card_history = game["card_history"]
        card_history = [card['card'] for card in card_history if card['player'] == "opponent"]
        card_history = [card['id'] for card in card_history if card['id'][-2:] != "t1" and card['id'] not in hero_powers and card['id'] != "GAME_005" and card['id'] != "GAME_005e"]
        # print(card_history)
        for card_one in card_history:
            for card_two in card_history:
                if frozenset((card_one, card_two)) not in final_data:
                    final_data[frozenset((card_one, card_two))] = 1
                else:
                    final_data[frozenset((card_one, card_two))] += 1

                if card_one not in paired_data:
                    paired_data[card_one] = {}
                if card_two not in paired_data:
                    paired_data[card_two] = {}
                if card_one not in paired_data[card_two]:
                    paired_data[card_two][card_one] = 0
                if card_two not in paired_data[card_one]:
                    paired_data[card_one][card_two] = 0
                paired_data[card_one][card_two] += 1
                paired_data[card_two][card_one] += 1

    # print(final_data)
    most_played_card_pair = max(final_data.keys(), key=(lambda key: final_data[key]))
    top_cards = dict(sorted(final_data.items(), key=operator.itemgetter(1), reverse=True)[:5])
    top_cards = [id_to_name[k] for pair in top_cards for k in pair]
    print(top_cards)
    for key in most_played_card_pair:
        print(id_to_name[key])
        # print([(id_to_name[k], final_data[frozenset((key, k))]) for k in paired_data[key]])
    # print(id_to_name['The Coin'])
    print()
    return final_data, paired_data

def parse_hero_powers(filename):
    data = parse_cards("cards.json")
    return [card["id"] for card in data if "type" in card and card["type"] == "HERO_POWER"]

def parse_cards(filename):
    with open(filename, encoding="utf-8") as data_file:
        data = json.load(data_file)
    return data

# all_cards = parse_cards("cards.json")
# hero_powers = parse_hero_powers("cards.json")

print_basic_info("2017-10-18.json")
print_basic_info("2017-09.json")