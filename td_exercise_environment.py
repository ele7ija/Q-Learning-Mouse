# ------------------------------------------------------- #
# Date: 22.02.2019.
# Author: Bojan Poprzen
# File: Temporal difference exercise: Environment model

# Environment should give us the information about:
#    1) What are all the possible states and state->state transitions
#    2) Rewards for the state->state transition
# ------------------------------------------------------- #

class State:
    """
    This class conceptually represents a State in the Environment.
    In the implementation context, it represents a field in a puzzle described
    by the Environment class.
    """
    def __init__(self, x, y, terminal=False):
        self._x = x
        self._y = y 
        self._terminal = terminal
    
    def get_terminal(self):
        return self._terminal

    def __str__(self):
        return "({},{})".format(self._x, self._y)


class Action:
    """
    This class represents a move in the puzzle. Depending on the state from which
    the agent chooses the move - type of the action can be 'r', 'l', 'u', 'd', 't'
    """
    def __init__(self, type):
        self._type = type

    def __str__(self):
        return self._type


class Environment:
    """
    API for this class:
        - get_states->set of State objects
        - get_reward->value of type double representing reward
        - get_transitioning_states->list of possible transitioning states
    """
    def __init__(self, size_y=4, size_x=4):
        self._size_y = size_y
        self._size_x = size_x

        self.states = []
        self.end_state = State(-1, -1, True)
        self._prev_state = None
        self._curr_state = None
        self._init_states(size_y, size_x)
        self._init_actions()

    def reset(self):
        """
        Resets the environment - sets the current state to the starting state

        Args:

        Returns:
            current_state: Starting state after this function
        """
        self._curr_state = self._start_state
        return self._curr_state

    def set_start_state(self, start_x, start_y):
        self._start_state = self.states[start_y][start_x]

    def step(self, action):
        """
        Emulates a step done by environment

        Args:
            action: Action object which has been previously chosen by the algorithm
        
        Returns:
            next_state: 
            reward:
            done:
        """
        self._prev_state = self._curr_state

        curr_x = self._curr_state._x
        curr_y = self._curr_state._y
        if action._type == 'r':
            self._curr_state = self.states[curr_y][curr_x+1]
        elif action._type == 'l':
            self._curr_state = self.states[curr_y][curr_x-1]
        elif action._type == 'u':
            self._curr_state = self.states[curr_y-1][curr_x]
        elif action._type == 'd':
            self._curr_state = self.states[curr_y+1][curr_x]
        else: # 't'
            self._curr_state = self.end_state

        return self._curr_state, self._get_reward(), self._curr_state.get_terminal()

    def get_states(self):
        return self.states

    def _manhattan_distance(self, state):
        """Calculates the manhattan distance to the terminal field"""
        return (self._size_x - state._x) + (self._size_y - state._y)

    def _get_reward(self):
        """
        This function provides the reward for transitioning from 
        self._prev_state to self._curr_state
        """
        if self._curr_state.get_terminal():
            return 800

        # if state1._x == 1 and state1._y == 2:
        #     return self._manhattan_distance(state1) * -10.0
        # elif state1._x == 2 and state1._y == 2:
        #     return self._manhattan_distance(state1) * -10.0
        # elif state1._x == 3 and state1._y == 2:
        #     return self._manhattan_distance(state1) * -10.0
        # elif state1._x == 4 and state1._y == 2:
        #     return self._manhattan_distance(state1) * -10.0
        # elif state1._x == 5 and state1._y == 2:
        #     return self._manhattan_distance(state1) * -10.0

        # if self._prev_state._y == 2 and \
        #     self._prev_state._x in range(1, self._size):
        #     return self._manhattan_distance(self._prev_state) * -10.0

        # if (self._curr_state._x, self._curr_state._y) in self.mouses:
        #     return self._manhattan_distance(self._curr_state) * -20.0
        if (self._curr_state._x, self._curr_state._y) in self.mouses:
            return -1000.0
        else:
            return self._manhattan_distance(self._curr_state) * -1.0

        # if self._curr_state._y == 2 and \
        #     self._curr_state._x in range(1, self._size_x):
        #     return self._manhattan_distance(self._curr_state) * -20.0
        # else:
        #     return self._manhattan_distance(self._curr_state) * -1.0

        # return self._manhattan_distance(self._curr_state) * -1.0
        

    def get_possible_actions(self, state):
        """
        This function returns 2, 3 or 4 of the possible actions to be done at a
        state
        """
        x = state._x
        y = state._y
        possible_actions = []

        if x == 0:
            if y == 0:
                possible_actions.append(self._actions['r'])
                possible_actions.append(self._actions['d'])
            elif y != self._size_y - 1:
                possible_actions.append(self._actions['r'])
                possible_actions.append(self._actions['d'])
                possible_actions.append(self._actions['u'])
            else:
                possible_actions.append(self._actions['r'])
                possible_actions.append(self._actions['u'])
        elif x != self._size_x - 1:
            if y == 0:
                possible_actions.append(self._actions['r'])
                possible_actions.append(self._actions['l'])
                possible_actions.append(self._actions['d'])
            elif y != self._size_y - 1:
                possible_actions.append(self._actions['r'])
                possible_actions.append(self._actions['l'])
                possible_actions.append(self._actions['d'])
                possible_actions.append(self._actions['u'])
            else:
                possible_actions.append(self._actions['r'])
                possible_actions.append(self._actions['l'])
                possible_actions.append(self._actions['u'])
        else:
            if y == 0:
                possible_actions.append(self._actions['l'])
                possible_actions.append(self._actions['d'])
            elif y != self._size_y - 1:
                possible_actions.append(self._actions['l'])
                possible_actions.append(self._actions['u'])
                possible_actions.append(self._actions['d'])
            else:
                possible_actions.append(self._actions['t'])
                # return_list.append(self.states[y][x - 1])
                # return_list.append(self.states[y - 1][x])
        return possible_actions


    def _init_states(self, size_y, size_x):
        """
        Creates a size*size puzzle in which a single field represents a state
        """
        for i in range(size_y):
            row = []
            for j in range(size_x):
                if i == self._size_y - 1 and j == self._size_x - 1:
                    s = State(j, i, False) # lul
                    row.append(s)
                    self.states.append(row)
                    return
                s = State(j, i)
                row.append(s)
            self.states.append(row)

    def _init_actions(self):
        self._actions = {}
        self._actions['r'] = Action('r')
        self._actions['l'] = Action('l')
        self._actions['u'] = Action('u')
        self._actions['d'] = Action('d')
        self._actions['t'] = Action('t')

    def set_mouses(self, mouses):
        self.mouses = mouses

    def __str__(self):
        return_string = ""
        for i in range(self._size_y):
            for j in range(self._size_x):
                return_string += str(self.states[i][j])
            return_string += "\n"
        return return_string

if __name__ == "__main__":
    e = Environment()
    print(e)