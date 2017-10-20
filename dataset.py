import json
from collections import Counter
import operator

class Dataset:
    filename = ""
    games = {}
    all_cards = {}
    hero_powers = []
    id_to_name_dict = {}
    final_data = {}
    paired_data = {}
    played_cards = []
    total_counts = {}

    def __init__(self, file):
        self.games = self.init_process_file(file)
        self.all_cards = self.parse_cards()
        self.hero_powers = self.parse_hero_powers()
        self.id_to_name_dict = self.init_id_to_name()
        self.final_data, self.paired_data = self.process_data()

    def process_data(self):
        final_data = {}
        paired_data = {}
        for game in self.games:
            card_history = game["card_history"]
            card_history = [card['card'] for card in card_history if card['player'] == "opponent"]
            card_history = [card['id'] for card in card_history if card['id'][-2:] != "t1" and card['id'] not in self.hero_powers and card['id'] != "GAME_005" and card['id'] != "GAME_005e"]
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
        top_cards = [self.id_to_name(k) for pair in top_cards for k in pair]
        # print(top_cards)
        # for key in most_played_card_pair:
            # print(self.id_to_name(key))
        # print()
        return final_data, paired_data

    def init_process_file(self, file):
        self.filename = file
        with open(file) as data_file:
            data = json.load(data_file)
        # print(file)
        # print("Number of unique users: " + str(data["unique_users"]))
        # print("Number of games: " + str(data["total_games"]))
        # print("Number of games (hard count): " + str(len(data["games"])))

        games = data["games"]
        c = Counter(games[x]["mode"] for x in range(len(games)))
        # print(c)

        games = [game for game in games if game["mode"] == "ranked"]
        # print("Number of ranked games: " + str(len(games)))
        return games

    def parse_hero_powers(self, file="cards.json"):
        return [card["id"] for card in self.all_cards if "type" in card and card["type"] == "HERO_POWER"]

    def parse_cards(self, file="cards.json"):
        with open(file, encoding="utf-8") as data_file:
            data = json.load(data_file)
        return data

    def init_id_to_name(self):
        id_to_name = {}
        for card in self.all_cards:
            if 'id' in card and 'name' in card and card['name'] not in id_to_name:
                id_to_name[card['id']] = card['name']
                id_to_name[card['name']] = card['id']
        return id_to_name

    def id_to_name(self, str):
        return self.id_to_name_dict[str]

    def add_card(self, name):
        self.played_cards.append(name)
        # print(self.paired_data[self.id_to_name(name)])
        for card_id, count in self.paired_data[self.id_to_name(name)].items():
            if card_id not in self.total_counts:
                self.total_counts[card_id] = 0
            self.total_counts[card_id] += count

    def get_probabilities(self):
        size = len(self.total_counts)
        maximum = max(self.total_counts.values())
        # print(self.total_counts)
        counter = Counter({self.id_to_name(card_id): '%.3f'%(count / maximum) for (card_id, count) in self.total_counts.items() if card_id in self.id_to_name_dict})
        # {(self.id_to_name(card_id), count) for (card_id, count) in self.total_counts.items() if card_id in self.id_to_name_dict}
        return counter.most_common(30)