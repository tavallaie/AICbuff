import json
from pprint import pprint
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
        self.constant = self.data[0]


    def flat_export(self, **kwargs):
        for key, data in kwargs.items():
            print(key)
            print(data)
            data_flatten = [flatten(d) for d in data]
            df = pd.DataFrame(data_flatten)
            df.to_csv(key + ".csv")


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
        self.currentTurn = 85
        self.flat_export(castabilities=self.data[self.currentTurn]["castAbilities"])
        self.flat_export(players= self.data[self.currentTurn]["players"][0]["heroes"])









if __name__ == "__main__":

    gamePlay = GamePlay()
