# Variant 15:
# Q = {q0,q1,q2,q3},
# ∑ = {a,b,c},
# F = {q3},
# δ(q0,a) = q0,
# δ(q1,b) = q2,
# δ(q0,a) = q1,
# δ(q2,a) = q2,
# δ(q2,b) = q3,
# δ(q2,c) = q0
# }

import random
from graphviz import Digraph

class Grammar:
    def __init__(self, non_terminals, terminals, productions, initial_state, final_states):
        self.nonterminal = non_terminals
        self.terminals = terminals
        self.production_rules = productions

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
        fa.add_transition('B', 'c', 'final')

        return fa

    def classify_grammar(self):
        type1 = type2 = type3 = type0 = True

        for left in self.production_rules:
            if len(left) > 1:
                type3 = False  # For structure like aAB -> a
                type2 = False  # For structure like AB -> a

            startedWithNonTerminal = False
            endedWithNonTerminal = False

            for right in self.production_rules[left]:
                # If the production is non-empty and the right side is shorter than the left side, it's invalid.
                if right != '' and len(right) < len(left):
                    type1 = False
                    print(f"Type 1 violation (shortened production): {left} -> {right}")

                # If an empty production is found, it is only allowed for the start symbol (if defined).
                if right == '' and left != self.start_symbol:
                    type1 = False
                    print(f"Empty production is only allowed for the start symbol: {left} -> {right}")

                startsWithNonTerminal = right and right[0] in self.nonterminal
                endsWithNonTerminal = right and right[-1] in self.nonterminal
                nonTerminalCount = sum(1 for symbol in right if symbol in self.nonterminal)

                if right == '':
                    continue

                if len(right) == 1:
                    if right not in self.terminal:
                        type3 = False  # For structure like A -> B
                        print("Vn -> Vn")
                elif not ((startsWithNonTerminal or endsWithNonTerminal) and nonTerminalCount == 1):
                    type3 = False  # For structure like A -> aBa or A -> BaB
                    print("Vn -> VnVn")

                if startsWithNonTerminal:
                    startedWithNonTerminal = True
                elif endsWithNonTerminal:
                    endedWithNonTerminal = True

                if startedWithNonTerminal and endedWithNonTerminal:
                    type3 = False  # For situations when A -> aB and A -> Ba
                    print("Vn -> VnVt/VtVn")

        if type3:
            return "Type 3 (Regular Grammar)"
        elif type2:
            return "Type 2 (Context-Free Grammar)"
        elif type1:
            return "Type 1 (Context-Sensitive Grammar)"
        else:
            return "Type 0 (Unrestricted Grammar)"

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

    def to_grammar(self):
        non_terminals = self.states
        terminals = self.alphabet
        productions = {}

        for state in self.states:
            productions[state] = []
            for symbol in self.alphabet:
                if state in self.transitions and symbol in self.transitions[state]:
                    next_states = self.transitions[state][symbol]
                    for next_state in next_states:
                        productions[state].append(symbol + next_state)
                        if next_state in self.final_states:
                            productions[state].append(symbol)

        return Grammar(non_terminals, terminals, productions, self.initial_state, self.final_states)

    def is_deterministic(self):
        for state in self.states:
            for symbol in self.alphabet:
                # Check if there are transitions for the current state and symbol
                if state in self.transitions and symbol in self.transitions[state]:
                    next_states = self.transitions[state][symbol]
                    # If there are multiple next states, it's non-deterministic
                    if len(next_states) > 1 and not isinstance(next_states, str):
                        return False

        return True


class NFAtoDFAConverter:
    def __init__(self, nfa):
        self.nfa = nfa
        self.alphabet = list(nfa.alphabet)  # Alphabet of the NFA
        self.states = []  # List of DFA states (each state is a set of NFA states)
        self.transitions = {}  # DFA transitions
        self.final_states = set()  # DFA final states
        self.initial_state = None  # DFA initial state
        self.convert()  # Perform the conversion

    def convert(self):
        # Compute the epsilon closure of the NFA's initial state
        initial_dfa_state = self.epsilon_closure({self.nfa.initial_state})
        self.states.append(initial_dfa_state)
        self.initial_state = self.state_to_string(initial_dfa_state)

        unprocessed_states = [initial_dfa_state]

        while unprocessed_states:
            current_state = unprocessed_states.pop()
            state_key = self.state_to_string(current_state)
            self.transitions[state_key] = {}

            for symbol in self.alphabet:
                # Compute the move for the current state and symbol
                next_state = self.epsilon_closure(self.move(current_state, symbol))
                if next_state:
                    next_state_key = self.state_to_string(next_state)

                    # If the next state is new, add it to the list of states
                    if not any(self.state_to_string(s) == next_state_key for s in self.states):
                        self.states.append(next_state)
                        unprocessed_states.append(next_state)

                    # Add the transition to the DFA
                    if symbol not in self.transitions[state_key]:
                        self.transitions[state_key][symbol] = []
                    self.transitions[state_key][symbol].append(next_state_key)

            # Check if the current state contains any NFA final states
            if any(state in self.nfa.final_states for state in current_state):
                self.final_states.add(state_key)

    def epsilon_closure(self, states):
        closure = set(states)
        stack = list(states)

        while stack:
            state = stack.pop()
            if state in self.nfa.transitions and '' in self.nfa.transitions[state]:
                for next_state in self.nfa.transitions[state]['']:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)

        return closure

    def move(self, states, symbol):
        result = set()
        for state in states:
            if state in self.nfa.transitions and symbol in self.nfa.transitions[state]:
                result.update(self.nfa.transitions[state][symbol])
        return result

    def state_to_string(self, state_set):
        return ','.join(sorted(state_set))

    def to_dfa(self):
        dfa_states = [self.state_to_string(state) for state in self.states]
        dfa_transitions = {}

        for state_key, transitions in self.transitions.items():
            dfa_transitions[state_key] = {}
            for symbol, next_states in transitions.items():
                dfa_transitions[state_key][symbol] = next_states[0]  # DFA has only one next state

        return FiniteAutomaton(
            states=dfa_states,
            alphabet=self.alphabet,
            transitions=dfa_transitions,
            initial_state=self.initial_state,
            final_states=self.final_states
        )


class NFAtoDFAConverter:
    def __init__(self, nfa):
        self.nfa = nfa
        self.alphabet = list(nfa.alphabet)  # Alphabet of the NFA
        self.states = []  # List of DFA states (each state is a set of NFA states)
        self.transitions = {}  # DFA transitions
        self.final_states = set()  # DFA final states
        self.initial_state = None  # DFA initial state
        self.convert()  # Perform the conversion

    def convert(self):
        # Compute the epsilon closure of the NFA's initial state
        initial_dfa_state = self.epsilon_closure({self.nfa.initial_state})
        self.states.append(initial_dfa_state)
        self.initial_state = self.state_to_string(initial_dfa_state)

        unprocessed_states = [initial_dfa_state]

        while unprocessed_states:
            current_state = unprocessed_states.pop()
            state_key = self.state_to_string(current_state)
            self.transitions[state_key] = {}

            for symbol in self.alphabet:
                # Compute the move for the current state and symbol
                next_state = self.epsilon_closure(self.move(current_state, symbol))
                if next_state:
                    next_state_key = self.state_to_string(next_state)

                    # If the next state is new, add it to the list of states
                    if not any(self.state_to_string(s) == next_state_key for s in self.states):
                        self.states.append(next_state)
                        unprocessed_states.append(next_state)

                    # Add the transition to the DFA
                    if symbol not in self.transitions[state_key]:
                        self.transitions[state_key][symbol] = []
                    self.transitions[state_key][symbol].append(next_state_key)

            # Check if the current state contains any NFA final states
            if any(state in self.nfa.final_states for state in current_state):
                self.final_states.add(state_key)

    def epsilon_closure(self, states):
        closure = set(states)
        stack = list(states)

        while stack:
            state = stack.pop()
            if state in self.nfa.transitions and '' in self.nfa.transitions[state]:
                for next_state in self.nfa.transitions[state]['']:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)

        return closure

    def move(self, states, symbol):
        result = set()
        for state in states:
            if state in self.nfa.transitions and symbol in self.nfa.transitions[state]:
                result.update(self.nfa.transitions[state][symbol])
        return result

    def state_to_string(self, state_set):
        return ','.join(sorted(state_set))

    def to_dfa(self):
        dfa_states = [self.state_to_string(state) for state in self.states]
        dfa_transitions = {}

        for state_key, transitions in self.transitions.items():
            dfa_transitions[state_key] = {}
            for symbol, next_states in transitions.items():
                dfa_transitions[state_key][symbol] = next_states[0]  # DFA has only one next state

        return FiniteAutomaton(
            states=dfa_states,
            alphabet=self.alphabet,
            transitions=dfa_transitions,
            initial_state=self.initial_state,
            final_states=self.final_states
        )


def visualize_fa(fa, title):
    graph = Digraph(comment=title)
    graph.attr(rankdir='LR')

    # Add states
    for state in fa.states:
        if state in fa.final_states:
            graph.node(state, shape='doublecircle')
        else:
            graph.node(state, shape='circle')

    graph.node('start', shape='none', label='')
    graph.edge('start', fa.initial_state)

    for from_state, transitions in fa.transitions.items():
        for symbol, to_states in transitions.items():
            if isinstance(to_states, str):
                graph.edge(from_state, to_states, label=symbol)
            else:
                for to_state in to_states:
                    graph.edge(from_state, to_state, label=symbol)

    graph.render(f'{title}.gv', view=True)


nfa_states = {'q0', 'q1', 'q2', 'q3'}
nfa_alphabet = {'a', 'b', 'c'}
nfa_transitions = {
    'q0': {'a': {'q0', 'q1'}},
    'q1': {'b': {'q2'}},
    'q2': {'a': {'q2'}, 'b': {'q3'}, 'c': {'q0'}}
}
nfa_initial_state = 'q0'
nfa_final_states = {'q3'}

nfa = FiniteAutomaton(nfa_states, nfa_alphabet, nfa_transitions, nfa_initial_state, nfa_final_states)
converter = NFAtoDFAConverter(nfa)
dfa = converter.to_dfa()

print("DFA States:", dfa.states)
print("DFA Alphabet:", dfa.alphabet)
print("DFA Transitions:", dfa.transitions)
print("DFA Initial State:", dfa.initial_state)
print("DFA Final States:", dfa.final_states)
print("DFA is deterministic:", dfa.is_deterministic())
visualize_fa(dfa, 'DFA')

print("")
print("nfa States:", nfa.states)
print("nfa Alphabet:", nfa.alphabet)
print("nfa Transitions:", nfa.transitions)
print("nfa Initial State:", nfa.initial_state)
print("nfa Final States:", nfa.final_states)
print("nfa is deterministic:", nfa.is_deterministic())
visualize_fa(nfa, 'NFA')
