from constants import EPSILON
from Grammar import Grammar

non_terminals = ['S', 'A', 'B', 'C', 'D']
terminals = ['a', 'b']
rules = {
    'S': ['aB', 'DA'],
    'A': ['a', 'BD', 'aDADB'],
    'B': ['b', 'ASB'],
    'C': ['BA'],
    'D': ['BA', EPSILON]
}

grammar = Grammar(non_terminals, terminals, rules)

print('Original grammar:')
grammar.print_rules()

print("\n\nCNF:")
grammar.to_cnf()