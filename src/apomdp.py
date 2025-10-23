import pomdp
from dataclasses import dataclass, field
from typing import Dict, List, Any
import numpy as np
from itertools import product

class my_unknown:
    def __init__(self):
        raise Exception("This has not been implemented yet!")

@dataclass
class aPOMDP:
    n_actions: int
    state_values: Dict[int, Dict]
    n_v_s: int
    weights: np.ndarray
    transition_matrix: Dict
    reward_matrix: Dict
    discount_factor: float
    states: List[List[int]]
    state_indices: Dict
    state_structure: List[int]
    reward_type: str

    @staticmethod
    def normalize(weights, axis=None):
        """Normalize a numpy array over a given axis."""
        weights = np.asarray(weights, dtype=np.float64)
        total = weights.sum(axis=axis, keepdims=True)
        return weights / total if total != 0 else weights

    @classmethod
    def make(
        cls,
        reward_type: str = "svr",
        n_v_s: int = 1,
        state_structure: List[int] = None,
        n_actions: int = 3,
        weights: np.ndarray = None
    ):
        if state_structure is None:
            state_structure = [3, 3]
        if weights is None:
            weights = cls.normalize(np.random.rand(n_v_s), axis=0)

        # 1. Generate all possible states (cartesian product)
        vecs = [list(range(1, n + 1)) for n in state_structure]
        states = [list(s) for s in product(*vecs)]

        # 2. Initialize state_value dict: state_values[n][state] = 0 for each n in [1, ..., n_v_s]
        state_values_dict = dict()
        for n in range(1, n_v_s + 1):
            state_values_dict[n] = {}           # Layer for v-function index n
            for state in states:
                state_values_dict[n][tuple(state)] = 0.0  # Use tuple as key for mutability

        # 3. Initialize state_indices dict
        state_indices = {}
        for idx, state in enumerate(states, 1):
            state_indices[tuple(state)] = idx

        # 4. Transition matrix
        transition_dict = {}
        for state in states:
            for k in range(1, n_actions + 1):
                key = tuple(list(state) + [k])
                # numpy array of ones, shape = state_structure
                transition_dict[key] = np.ones(state_structure, dtype=np.float64) / 1000

        # 5. Reward matrix
        reward_dict = {}
        for state in states:
            for k in range(1, n_actions + 1):
                key = tuple(list(state) + [k])
                reward_dict[key] = 0.0

        return cls(
            n_actions=n_actions,
            state_values=state_values_dict,
            n_v_s=n_v_s,
            weights=weights,
            transition_matrix=transition_dict,
            reward_matrix=reward_dict,
            discount_factor=0.95,
            states=states,
            state_indices=state_indices,
            state_structure=state_structure,
            reward_type=reward_type
        )
    
    @classmethod
    def calculate_reward_matrix(self):
        for s, k in zip(self.states, 0:self.n_actions):
            key = np.vstack((s, [k]))
            sum_var = 0

            dist = transition(self, s, k)
            if self.reward_type == "msvr":
                for f in range(self.n_v_s):
                    inner_sum = 0
                    for state in dist.state_space:
                        inner_sum += pdf(dist, state)*(pomdp.state_values[f][state]-pomdp.state_values[f][s])
                    sum_var += pomdp.weights(f)*inner_sum
            else:
                for state in dist.state_space:
                    sum_var += pdf(dist, state)*(pomdp.state_values[0][state]-pomdp.state_values[0][s]) #off-by-one risk
            
            if pomdp.reward_type == "isvr" or pomdp.reward_type == "msvr":
                sum_var += self.calc_entropy(dist.dist)
            pomdp.reward_matrix[key] = sum_var
        
    @classmethod
    def calc_entropy(self, dist):
        h = 0
        for val in dist:
            h += val * np.log2(val)
        return -h
    
    @classmethod
    def integrate_transition(self, prev_state, final_state, action):
        key = prev_state[:] #risk
        key.append(action)
        self.transition_matrix[key][final_state] += 1 #risk, originally used splatting

    @classmethod
    def set_state_value(self, state, value, index=1):
        self.state_values[index][state[:]] = value

@dataclass
class apomdpDistribution:
    statespace: list
    dist: list

def apomdpDeterministicDistribution(pomdp: aPOMDP, state: list):
    dist = np.ones(pomdp.state_structure, dtype=np.float64)/1000.0
    dist[state] = 1000
    dist = dist / dist.sum()
    return apomdpDistribution(my_unknown(), dist)

def apomdpUniformDistribution(pomdp: aPOMDP):
    dist = np.ones(pomdp.state_structure, dtype=np.float64)/1000.0
    dist = dist / dist.sum()
    return apomdpDistribution(my_unknown, dist)

d = aPOMDP.make()