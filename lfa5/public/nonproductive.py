from constants import EPSILON
from Grammar import Grammar

non_terminals = ['S', 'A', 'B', 'C', 'D', 'E', 'F']
terminals = ['a', 'b']
rules = {
    'S': ['aB', 'DA', 'EC'],
    'A': ['a', 'BD', 'aDADB', 'FE'],
    'B': ['b', 'ASB'],
    'C': ['BA', 'EF'],  # Non-productive
    'D': ['BA', EPSILON],
    'E': ['FA'], # Non-productive
    'F': ['EB'], # Non-productive
}

grammar = Grammar(non_terminals, terminals, rules)

print('New grammar:')
grammar.print_rules()

print('\nConverting to CNF:')
grammar.to_cnf()