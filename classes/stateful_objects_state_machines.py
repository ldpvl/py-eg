# You want to implement a state machine or an object that operates in a number of dif‐
# ferent states, but don’t want to litter your code with a lot of conditionals.

# This recipe is loosely based on the state design pattern found in Design Patterns: Ele‐
# ments of Reusable Object-Oriented Software by Erich Gamma, Richard Helm, Ralph
# Johnson, and John Vlissides (Addison-Wesley, 1995).

# Original implementation
class State:
    def __init__(self):
        self.state = 'A'

    def action(self, x):
        if self.state == 'A':
            # Action for A
            ...
            state = 'B'
        elif self.state == 'B':
            # Action for B
            ...
            state = 'C'
        elif self.state == 'C':
            # Action for C
            ...
            state = 'A'

# Alternative implementation
class State:
    def __init__(self):
        self.new_state(State_A)

    def new_state(self, state):
        self.__class__ = state

    def action(self, x):
        raise NotImplementedError()

class State_A(State):
    def action(self, x):
        # Action for A
        ...
        self.new_state(State_B)

class State_B(State):
    def action(self, x):
        # Action for B
        ...
        self.new_state(State_C)

class State_C(State):
    def action(self, x):
        # Action for C
        ...
        self.new_state(State_A)