import re
from graphviz import Digraph
from Parser import Parser
from TokenType import TokenType

TOKENS = [
    (TokenType.HTML_OPEN, r'<html>'),
    (TokenType.HTML_CLOSE, r'</html>'),
    (TokenType.HEAD_OPEN, r'<head>'),
    (TokenType.HEAD_CLOSE, r'</head>'),
    (TokenType.TITLE_OPEN, r'<title>'),
    (TokenType.TITLE_CLOSE, r'</title>'),
    (TokenType.BODY_OPEN, r'<body>'),
    (TokenType.BODY_CLOSE, r'</body>'),
    (TokenType.H1_OPEN, r'<h1>'),
    (TokenType.H1_CLOSE, r'</h1>'),
    (TokenType.P_OPEN, r'<p>'),
    (TokenType.P_CLOSE, r'</p>'),
    (TokenType.CONTENT, r'[^<]*'),  # Match any content not containing '<' or '>'
]


def lexer(html):
    tokens = []
    while html:
        html = html.strip()
        match_found = False
        for token_type, token_regex in TOKENS:
            regex = re.compile(token_regex)
            match = regex.match(html)
            if match:
                value = match.group(0).strip()
                tokens.append((token_type, value))
                html = html[match.end():]
                match_found = True
                break
        if not match_found:
            raise SyntaxError(f'Unknown HTML: {html}')
    return tokens


html_code = """
<html>
<head>
<title>Sample Page</title>
</head>
<body>
<h1>Welcome</h1>
<p>This is a sample page.</p>
</body>
</html>
"""

tokens = lexer(html_code)
print("Tokens:")
print(tokens)
parser = Parser()
ast = parser.parse(tokens)
print("AST: ")
print(ast)

def visualize_ast(node, graph=None):
    if graph is None:
        graph = Digraph()
    graph.node(str(id(node)), label=f"{node.type.name}\n{node.value}")
    for child in node.children:
        graph.edge(str(id(node)), str(id(child)))
        visualize_ast(child, graph)
    return graph


graph = visualize_ast(ast)
graph.render('ast', view=True)