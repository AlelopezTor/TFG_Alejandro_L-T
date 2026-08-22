import random
import numpy as np
class Node:
    infoset: str
    n_actions: int
    regret_sum: np.ndarray
    strategy: np.ndarray
    strategy_sum: np.ndarray

    def __init__(self, infoset, legal_actions) -> None:
        self.n_actions = len(legal_actions)
        self.legal_actions = legal_actions
        self.infoset = infoset
        self.regret_sum = np.zeros(self.n_actions)
        self.strategy_sum = np.zeros(self.n_actions)
        self.strategy = np.zeros(self.n_actions)

    def get_strategy(self, relizationWeight: float) -> np.ndarray:
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
    CHEKC_CALL: str = 'c' #pasar si nadie apuesta o igualar la apuesta
    BET: str = 'b' #apostar
    RAISE: str = 'r'
    FOLD: str = 'f' #retirarse
    BETS: tuple[int, int] = (2, 4)
    node_map: dict[str, Node]
    DECK = ['J', 'J', 'Q', 'Q', 'K', 'K']
    RANKS = {'J': 0, 'Q': 1, 'K': 2}
    def __solve_winner(self, cards):
        if cards[0] == cards[2]:
            return 0
        elif cards[1] == cards[2]:
            return 1
        elif cards[0] == cards[1]:
            return -1
        else:
            return 0 if self.RANKS[cards[0]] > self.RANKS[cards[1]] else 1            
    
    def __legal_actions(self, history: str) -> tuple[str, ...]:
        last_round = history.split('/')[-1]
        if last_round and last_round[-1] in (self.BET, self.RAISE):
            if last_round[-1] == self.RAISE:
                return (self.FOLD, self.CHEKC_CALL)
            return (self.FOLD, self.CHEKC_CALL, self.RAISE)
        return (self.CHEKC_CALL, self.BET)
    
    def __terminal_unit(self, history, to_move, cards = None):
        rounds: str = history.split('/')
        last_round: str = rounds[-1]
        
        loser_count: int = 1
        winner_count: int = 1
        for r, rnd in enumerate(rounds):
            for i, ch in enumerate(rnd):
                if ch == self.BET or ch == self.RAISE:
                    if i%2 == to_move:
                        winner_count = loser_count + self.BETS[r]
                    else:
                        loser_count = winner_count + self.BETS[r]
                if ch == self.CHEKC_CALL:
                    if i%2 == to_move:
                        winner_count = loser_count
                    else:
                        loser_count = winner_count
        if history.endswith(self.FOLD):
            return (True, loser_count)
        elif len(rounds) > 1 and len(last_round) >= 2 and last_round.endswith(self.CHEKC_CALL):
            winner = self.__solve_winner(cards)
            if winner == -1:
                return (True, 0)
            return (True, loser_count) if winner == to_move else (True, -loser_count)
        return (False, None)
    
    def __round_closes(self, history: str, action: str) -> bool:
        last_round:str = history.split('/')[-1]
        return action == self.CHEKC_CALL and last_round != ''
            
                    
    def __cfr(self, cards: list[str], history: str, p0: float, p1: float) -> float:
        last_round: str = history.split('/')[-1]
        to_move: int = len(last_round) % 2
        finished, result = self.__terminal_unit(history, to_move, cards)
        if finished:
            return result #type: ignore
            
        carta_juagdor = cards[to_move]
        if len(history.split('/')) > 1:
            infoset = carta_juagdor + cards[-1] + '|' + history
        else: 
            infoset = carta_juagdor + '|' + history 
        
        node: Node = self.node_map.get(infoset) #type: ignore
        if node is None:
            node: Node = Node(infoset, self.__legal_actions(history))
            self.node_map[infoset] = node
            
        strategy: np.ndarray = node.get_strategy(p0 if to_move == 0 else p1)
        util: np.ndarray = np.zeros(node.n_actions)
        node_util: float = 0
        
        for i, action in enumerate(node.legal_actions):
            next_h = history + action 
            if self.__round_closes(history, action) and len(history.split('/')) == 1:
                next_h += '/'
            hijo_to_move = len(next_h.split('/')[-1]) % 2
            if to_move == 0:
                aux = self.__cfr(cards, next_h, p0 * strategy[i], p1)
            else:
                aux = self.__cfr(cards, next_h, p0, p1 * strategy[i])
            util[i] = -aux if hijo_to_move != to_move else aux  
            node_util += strategy[i]* util[i]
        for i in range (node.n_actions):
            regret: float = util[i] - node_util
            node.regret_sum[i] += (p1 if to_move == 0 else p0) * regret
        return node_util  
        
    def train(self, iterations:int):
        random.seed()
        util: float = 0
        for _ in range (iterations):
            cards: list[str] = random.sample(self.DECK, 3)
            util += self.__cfr(cards, '', 1, 1)
        print(f"Media de valor por iteración: {util / iterations:.5f}")
        for infoset in sorted(self.node_map):
            node = self.node_map[infoset]
            print(infoset, node.legal_actions, node.get_average_strategy())
    
    def __init__(self) -> None:
        self.node_map = {}
    
                    
        
            
    
    


    