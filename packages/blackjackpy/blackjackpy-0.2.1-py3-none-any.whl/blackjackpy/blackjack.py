import random


class Card:
    """カード"""

    def __init__(self, num: int):
        self.suit = num // 13 + 1
        self.rank = num % 13 + 1

    def point(self) -> int:
        return min(10, self.rank)

    def __str__(self):
        n = self.rank * 2
        m = n - 2
        r = " A 2 3 4 5 6 7 8 910 J Q K"[m:n]
        s = "(" + "DHSC"[self.suit - 1] + ")"
        return r + s


class Owner:
    """手札を持ち、カードを引ける人"""

    def __init__(self):
        self.hands = []

    def draw(self, gm: "GameMaster") -> None:
        self.hands.append(gm.pop())

    def sequence(self, hided: bool = False) -> str:
        s = "".join(str(cd) for cd in self.hands)
        return (s[:5] + " *(*)" + s[10:]) if hided else s

    def point(self) -> int:
        p = sum(cd.point() for cd in self.hands)
        for cd in self.hands:
            if cd.rank == 1 and p + 10 <= 21:
                p += 10
        return p


class Player(Owner):
    """プレイヤー"""

    def ask(self) -> str:
        print("Hit? (y/n) ", end="")
        return input()

    def act(self, gm: "GameMaster") -> None:
        while self.point() <= 20:
            gm.show(True)
            s = ""
            while s != "y" and s != "n":
                s = self.ask()
            if s == "n":
                break
            self.draw(gm)


class Dealer(Owner):
    """ディーラー"""

    def act(self, gm: "GameMaster") -> None:
        while self.point() <= 16:
            self.draw(gm)


class GameMaster:
    """ゲームマスター"""

    def __init__(self, seed=None):
        self.cards = [Card(i) for i in range(52)]
        if seed is not None:
            random.seed(seed)
        random.shuffle(self.cards)
        self.player = Player()
        self.dealer = Dealer()

    def start_game(self) -> None:
        for _ in range(2):
            self.player.draw(self)
            self.dealer.draw(self)
        self.player.act(self)
        player_point = self.player.point()
        self.message = "You lose."
        if player_point <= 21:
            self.dealer.act(self)
            dealer_point = self.dealer.point()
            if player_point == dealer_point:
                self.message = "Draw."
            elif dealer_point >= 22 or dealer_point < player_point:
                self.message = "You win."
        self.show(False)
        print(self.message)

    def show(self, hided: bool) -> None:
        p = self.player.point()
        s = self.player.sequence()
        print(f"Player({p:2}): {s}")
        p = "--" if hided else self.dealer.point()
        s = self.dealer.sequence(hided)
        print(f"Dealer({p:2}): {s}")

    def pop(self) -> Card:
        return self.cards.pop(0)


def main():
    GameMaster().start_game()
