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
    CHEKC: int = 0 #pasar si nadie apuesta
    BET: int = 1 #apostar
    CALL: int = 2 #igualar la apuesta
    RAISE: int = 3
    FOLD: int = 4 #retirarse
    node_map: dict[str, Node]
    
    


    