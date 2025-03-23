import itertools


class SimpleRegexGenerator:
    def __init__(self, pattern):
        self.pattern = pattern
        self.explanation = []  # To store explanation steps

    def add_explanation(self, part, explanation):
        """Adds an explanation for each part of the pattern being processed."""
        self.explanation.append(f"Processing '{part}': {explanation}")

    def parse_pattern(self):
        """
        Parses the simplified pattern into components, with explanations.
        """
        parts = []
        i = 0
        while i < len(self.pattern):
            if self.pattern[i] == '(':
                end = self.pattern.find(')', i)
                if end == -1:
                    raise ValueError("Unmatched parenthesis")
                group = self.pattern[i + 1:end].split('|')
                parts.append(group)
                self.add_explanation(self.pattern[i:end + 1],
                                     "Either of " + " or ".join(group) + " appears exactly once")
                i = end + 1
            elif self.pattern[i] == '{':
                end = self.pattern.find('}', i)
                if end == -1:
                    raise ValueError("Unmatched curly brace")
                repeat = int(self.pattern[i + 1:end])
                if parts:
                    last_part = parts.pop()
                    parts.append([''.join([c] * repeat) for c in last_part])
                self.add_explanation(self.pattern[i:end + 1], f"Previous character appears exactly {repeat} times")
                i = end + 1
            elif i + 1 < len(self.pattern) and self.pattern[i + 1] in '?*+':
                if self.pattern[i + 1] == '?':
                    parts.append([self.pattern[i], ''])
                    self.add_explanation(self.pattern[i:i + 2], f"'{self.pattern[i]}' is optional")
                elif self.pattern[i + 1] == '*':
                    parts.append(['', self.pattern[i]])
                    self.add_explanation(self.pattern[i:i + 2], f"'{self.pattern[i]}' appears zero or more times")
                elif self.pattern[i + 1] == '+':
                    parts.append([self.pattern[i], self.pattern[i] * 2])
                    self.add_explanation(self.pattern[i:i + 2], f"'{self.pattern[i]}' appears one or more times")
                i += 2
            else:
                parts.append([self.pattern[i]])
                self.add_explanation(self.pattern[i], f"'{self.pattern[i]}' appears exactly once")
                i += 1
        return parts

    def explain_process(self):
        """Prints the explanation of how the pattern was processed."""
        print(f"\nExplanation for Processing of Pattern {self.pattern}:")
        for step in self.explanation:
            print(step)
        print("\n")

    def generate_strings(self, parts):
        """
        Generate strings from the parsed pattern components.
        """
        for combination in itertools.product(*parts):
            yield ''.join(combination)

    def run(self):
        parts = self.parse_pattern()
        self.explain_process()
        print("Generated strings:")
        for string in self.generate_strings(parts):
            print(string)


pattern = 'M?N{2}(O|P){3}Q*R+'
# pattern = '(X|Y|Z){3}8+(9|0)'
# pattern = '(H|i)(J|K)L*N'
generator = SimpleRegexGenerator(pattern)
generator.run()
