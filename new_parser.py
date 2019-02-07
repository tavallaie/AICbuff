import json


class Parser:
    def __init__(self):
        with open('server_view.log') as f:
            self.data = json.load(f)
        self.currentTurn = 0
        self.gameName = "test"
        self.player = {0:"player1", 1:"player2"}
        self.phase = ""
        self.constant = self.data[0]


class Constant(Parser):
    def __init__(self):
        super(Constant, self).__init__()
        self.gameConstant = self.constant["gameConstants"]
        self.map = self.constant["map"]
        self.cells = self.map["cells"]


class HeroConstants (Parser):
    def __init__(self):
        super(HeroConstants, self).__init__()
        self.heroConstant = self.constant["heroConstants"]
        self.heroID = 0
        print(self.heroConstant[3])




    
if __name__ == "__main__":

    a = HeroConstants()
