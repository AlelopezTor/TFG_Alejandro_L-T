import random
class Node:
    infoset: str = ''
    n_actions: int
    regret_sum: list[float] = []
    strategy: list[float] = []
    strategy_sum: list[float] = []
    def __init__(self, infoset: str, n_actions: int) -> None:
        self.n_actions = n_actions
        self.infoset = infoset
        
    def get_strategy(self, relizationWeight: float) -> list[float]:
        normalized_sum: float = 0
        for i in range(self.n_actions):
            self.strategy[i] = self.regret_sum[i] if self.regret_sum[i] > 0 else 0
            normalized_sum += self.strategy[i]
        for i in range(self.n_actions):
            if normalized_sum > 0:
                self.strategy[i] /= normalized_sum
            else:
                self.strategy[i] = 1/self.n_actions
            self.strategy_sum[i] += relizationWeight * self.strategy[i]
        return self.strategy
    
    def get_average_strategy(self) -> list[float]:
        avg_strategy: list[float] = []
        normalized_sum: float = 0
        for i in range(self.n_actions):
            normalized_sum += self.strategy_sum[i]
        for i in range (self.n_actions):
            avg_strategy.append(self.strategy_sum[i] / normalized_sum if normalized_sum > 0 else 1/self.n_actions)
        return avg_strategy
    
class CFR:
    CHEKC: str = 'c' #pasar si nadie apuesta
    BET: str = 'b' #apostar
    CALL: str = 'ca' #igualar la apuesta
    RAISE: str = 'r'
    FOLD: str = 'f' #retirarse
    BETS: tuple[int, int] = (2, 4)
    node_map: dict[str, Node]
    DECK = ['J', 'J', 'Q', 'Q', 'K', 'K']

    def __solve_winner(self, cards):
        if cards[0] == cards[2]:
            return 0
        elif cards[1] == cards[2]:
            return 1
        elif cards[0] == cards[1]:
            return -1
        else:
            return 0 if cards[0] > cards[1] else 1
            
            
            
            
    def __cfr(self, cards: list[str], history: str, p0: float, p1: float) -> float:
        last_round = history.split('/')[-1]
        to_move:int = len(last_round) % 2
        loser: int = 1 - to_move
        loser_count: int = 1
        winner_count: int = 1
        if history.endswith(self.FOLD):
            for r, round in enumerate(history.split('/')):
                for i, ch in enumerate(round):
                    if ch == self.BET or ch == self.RAISE:
                        if i%2 == to_move:
                            winner_count = loser_count + self.BETS[r]
                        else:
                            loser_count = winner_count + self.BETS[r]
                    if ch == self.CALL:
                        if i%2 == to_move:
                            winner_count = loser_count
                        else:
                            loser_count = winner_count
            return loser_count
        elif history.split('/')[-1].endswith(self.CHEKC+self.CHEKC) and len(history.split('/')) > 1:
            winner = self.__solve_winner(cards)
            if winner == -1:
                return 0
            for r, round in enumerate(history.split('/')):
                for i, ch in enumerate(round):
                    if ch == self.BET or ch == self.RAISE:
                        if i%2 == to_move:
                            winner_count = loser_count + self.BETS[r]
                        else:
                            loser_count = winner_count + self.BETS[r]
                    if ch == self.CALL:
                        if i%2 == to_move:
                            winner_count = loser_count
                        else:
                            loser_count = winner_count
            
            return loser_count if winner == to_move else -loser_count
            
        
                    
    def train(self, iterations:int):
        random.seed()
        util: float = 0
        for i in range (iterations):
            random.shuffle(self.DECK)
            cards = random.sample(self.DECK, 3)
            util += self.__cfr(cards, '', 1, 1)
        print(f"Media de valor por iteración: {util / iterations}")
        for node in self.node_map.values():
            print(node.infoset)
        
    
                    
        
            
    
    


    