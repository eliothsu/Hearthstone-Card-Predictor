import json
from collections import Counter
import operator

class Dataset:
    filename = ""
    all_cards = {}
    hero_powers = []

    def __init__(self, file):
        self.init_process_file(file)
        self.all_cards = self.parse_cards()
        self.hero_powers = self.parse_hero_powers()

    def init_process_file(self, file):
        self.filename = file
        with open(file) as data_file:
            data = json.load(data_file)
        print(file)
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

        # all_cards = parse_cards("cards.json")
        # hero_powers = parse_hero_powers("cards.json")
        id_to_name = {}
        for card in self.all_cards:
            if 'id' in card and 'name' in card:
                id_to_name[card['id']] = card['name']
                id_to_name[card['name']] = card['id']

    def parse_hero_powers(self, file="cards.json"):
        return [card["id"] for card in self.all_cards if "type" in card and card["type"] == "HERO_POWER"]

    def parse_cards(self, file="cards.json"):
        with open(file, encoding="utf-8") as data_file:
            data = json.load(data_file)
        return data