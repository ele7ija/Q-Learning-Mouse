# ------------------------------------------------------- #
# Date: 22.02.2019.
# Author: Bojan Poprzen
# File: Temporal difference exercise: Agent

# Agent 
# Agent should give us the information about:
#    1) Q-function value
# ------------------------------------------------------- #

from td_exercise_environment import Environment
import numpy as np
from random import random
import operator
class Agent:
    def __init__(self, environment):
        self._env = environment
        self.Q = {}

    def get_action_values(self, state):
        return self.Q[state]

    def set_action_value(self, state, action, value):
        self.Q[state][action] = value

    def init_q_values(self):
        for row in self._env.states:
            for state in row:
                state_action_values = {}
                for action in self._env.get_possible_actions(state):
                    state_action_values[action] = 0
                self.Q[state] = state_action_values
        
        self.Q[self._env.end_state] = {self._env._actions['t']: 0}

    def __str__(self):
        return_string = ""
        for row in self._env.states:
            for state in row:
                return_string += str(state) + "["
                for action in self.Q[state]:
                    return_string += str(action) + ": "
                    return_string += str(self.Q[state][action]) + "\t"
                return_string += "]  "
            return_string += "\n"
        return return_string

def make_epsilon_greedy_policy(Q, epsilon):
    """
    Creates an epsilon-greedy policy based on a given Q-function and epsilon.
    
    Args:
        Q: A dictionary that maps from state -> actions -> state-action-values.
        epsilon: The probability to select a random action . float between 0 and 1.
    
    Returns:
        A function that takes the observation as an argument and returns
        the probabilities for each action in the form of a numpy array of length nA.
    
    Variables:
        nA: number of possible action in a given state-observation
        A: dictionary with Action-value pairs
    """
    def policy_fn(observation):
        nA = len(Q[observation])
        A = {}
        for action in Q[observation]:
            A[action] = 1.0 * epsilon / nA
        best_action = max(Q[observation].items(), key=operator.itemgetter(1))[0]
        A[best_action] += 1.0 - epsilon
        return A
    return policy_fn

def get_random_action(action_probs):
    """
    Args:
        action_probs: dict with Action-value pairs

    Returns:
        Action object with the respect to the probabilities of choosing one randomly given in
        the action_probs
    """
    action_probs_items = list(action_probs.items())
    chosen_action_index = np.random.choice(
        np.arange(len(action_probs_items)), 
        p=[item[1] for item in action_probs_items])
    return action_probs_items[chosen_action_index][0]


def q_learning(env, num_episodes=500, epsilon=0.1, discount_factor=0.8, alpha=0.5):
    a = Agent(env)
    a.init_q_values()

    policy = make_epsilon_greedy_policy(a.Q, epsilon)

    for i in range(num_episodes):

        # Initialize state
        state = env.reset()

        while True:
            # Choose A from S using policy derived from Q
            action_probs = policy(state)
            action = get_random_action(action_probs)
            
            # Do a step in the environment
            next_state, reward, done = env.step(action)

            # TD control
            best_next_action = max(a.Q[next_state].items(), key=operator.itemgetter(1))[0]
            td_target = reward + discount_factor * a.Q[next_state][best_next_action]
            td_delta = td_target - a.Q[state][action]
            a.Q[state][action] += alpha * td_delta

            # Update the view with the new value for a.Q[state][action]

            # Check if the current state is terminal
            if done:
                break

            state = next_state

            # print(a)

    return a.Q

if __name__ == "__main__":
    env = Environment(4)
    Q = q_learning(env, 500)