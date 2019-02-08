import json
import pandas as pd
from pandas.io.json import json_normalize
from flatten_json import flatten


class Parser:
    def __init__(self):
        with open('server_view.log') as f:
            self.data = json.load(f)
        self.gameName = "test"
        self.player = {0: "player1", 1: "player2"}
        self.phase = ""
        self.gameConstants = self.data[0]['gameConstants']

        # print(self.data[0].keys())
        # self.gameMaps = json_normalize(self.data[0]["map"])



    def flat_export(self, **kwargs):
        # print(kwargs.keys())
        for key, data in kwargs.items():
            data_flatten = [flatten(d) for d in data]
        df = pd.DataFrame(data_flatten)
        df.to_csv(key + ".csv")
        return df


class Constant(Parser):
    def __init__(self):
        super(Constant, self).__init__()
        self.gameConstant = self.constant["gameConstants"]
        maps = self.constant["map"]
        self.cells = maps["cells"]


class HeroConstants (Parser):
    def __init__(self):
        super(HeroConstants, self).__init__()
        self.heroConstant = self.constant["heroConstants"]


class PickedHero(Parser):
    def __init__(self):
        super(PickedHero, self).__init__()

        self.pickedheroes = self.data[1]["heroes"]
        # self.sort_by_id()
        # self.heroes = {i:pickedheroes[i].item() for i in pickedheroes.items()}
        # pprint(pickedheroes[0])

    def sort_by_id(self):
        for i in self.pickedheroes:
            d = {d:x for d,x in enumerate(i)}
            for j in range(len(d)):
                print(j)
                for key, value in d[j].items():
                    print(str(key) + " : " + str(value))


class GamePlay(Parser):
    def __init__(self):
        super(GamePlay, self).__init__()
        self.Turn = [15, 8]
        self.castAbility = ""
        self.player = ""
        self.make_game_play_great_again()

    def make_game_play_great_again(self):
        castabilities_list = []
        for currenturn in self.Turn:
            turn_castability = self.flat_export(castabilities=self.data[currenturn ]["castAbilities"])

            turn_castability["turn"] = currenturn
            castabilities_list.append(turn_castability)
            self.castAbility = pd.concat(castabilities_list, sort= False)
            # self.player = self.flat_export(players=self.data[currenturn]["players"][0]["heroes"])
        print(self.castAbility)
        self.castAbility.to_csv("castability.csv")


if __name__ == "__main__":

    gamePlay = GamePlay()
