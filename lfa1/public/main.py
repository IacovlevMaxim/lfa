# Variant 15:
# VN={S, A, B},
# VT={a, b, c},
# P={
#     S → aS
#     S → bS
#     S → cA
#     A → aB
#     B → aB
#     B → bB
#     B → c
# }

import random

class Grammar:
    def __init__(self):
        self.nonterminal = {'S', 'A', 'B'}
        self.terminal = {'a', 'b', 'c'}
        self.production_rules = {
            'S': ('aS', 'bS', 'cA'),
            'A': ('aB'),
            'B': ('aB', 'bB', 'c')
        }

    def generate_string(self, start_symbol='S'):
        result = start_symbol

        # While there are non-terminal symbols
        while any(symbol in self.nonterminal for symbol in result):
            for symbol in result:
                if symbol in self.nonterminal:
                    # Get a random rule for this non-terminal symbol
                    rule = random.choice(self.production_rules[symbol])

                    # Replace the non-terminal symbol with the given rule
                    result = result.replace(symbol, rule, 1)
                    break

        return result

    def to_finite_automaton(self):
        # Empty string indicates the final state
        states = {'S', 'A', 'B', ''}
        alphabet = self.terminal
        transitions = {}
        initial_state = 'S'
        # Represent empty string as final state (aka epsilon)
        final_states = {''}

        fa = FiniteAutomaton(states, alphabet, transitions, initial_state, final_states)
        fa.add_transition('S', 'a', 'S')
        fa.add_transition('S', 'b', 'S')
        fa.add_transition('S', 'c', 'A')
        fa.add_transition('A', 'a', 'B')
        fa.add_transition('B', 'a', 'B')
        fa.add_transition('B', 'b', 'B')
        fa.add_transition('B', 'c', '')

        return fa

class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = set(final_states)

    def string_belong_to_language(self, input_string):
        # Start from initial state
        current_state = self.initial_state
        for char in input_string:
            # If char is not in the alphabet, it is 100% not of this language
            if char not in self.alphabet:
                return False

            # Get state transitions for current state
            state_transitions = self.transitions.get(current_state, {})

            # If we cant reach the character from current state, wrong language
            if char not in state_transitions:
                return False

            # Change the state to the state, with which this char was generated
            current_state = state_transitions[char]

        return current_state in self.final_states

    def add_transition(self, from_state, input_char, to_state):
        if from_state not in self.transitions:
            self.transitions[from_state] = {}
        self.transitions[from_state][input_char] = to_state

    def set_start_state(self, start_state):
        self.initial_state = start_state

    def add_final_state(self, final_state):
        self.final_states.add(final_state)


grammar = Grammar()
strs = []
while len(strs) < 5:
    random_string = grammar.generate_string()
    if random_string not in strs:
        print(f"Generated string: {random_string}")
        strs.append(random_string)

fa = grammar.to_finite_automaton()
test_string = "cabcc"
print(f"String '{test_string}' belongs to language: {fa.string_belong_to_language(test_string)}")
