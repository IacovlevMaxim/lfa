from TokenType import TokenType, enum


class ASTNode:
    def __init__(self, type, children=None, value=None):
        self.type = type
        self.value = value
        self.children = children if children is not None else []

    def __repr__(self):
        type_name = self.type.name if isinstance(self.type, enum.Enum) else self.type
        return f"{type_name}({self.value}, {self.children})"


class Parser:
    def __init__(self):
        self.root = None
        self.current_node = None
        self.stack = []

    def parse(self, tokens):
        self.root = ASTNode(TokenType.HTML_OPEN, value="ROOT")
        self.current_node = self.root
        self.stack = [self.root]

        for token_type, value in tokens:
            self.handle_token(token_type, value)

        return self.root

    def handle_token(self, token_type, value):
        if token_type == TokenType.HEAD_OPEN:
            self.handle_head_open()
        elif token_type == TokenType.TITLE_OPEN:
            self.handle_title_open()
        elif token_type == TokenType.BODY_OPEN:
            self.handle_body_open()
        elif token_type == TokenType.H1_OPEN:
            self.handle_h1_open()
        elif token_type == TokenType.P_OPEN:
            self.handle_p_open()
        elif token_type == TokenType.CONTENT:
            self.handle_content(value)
        elif token_type == TokenType.HEAD_CLOSE:
            self.handle_head_close()
        elif token_type == TokenType.TITLE_CLOSE:
            self.handle_title_close()
        elif token_type == TokenType.BODY_CLOSE:
            self.handle_body_close()
        elif token_type == TokenType.H1_CLOSE:
            self.handle_h1_close()
        elif token_type == TokenType.P_CLOSE:
            self.handle_p_close()
        elif token_type == TokenType.HTML_CLOSE:
            self.handle_html_close()

    def handle_head_open(self):
        head_node = ASTNode(TokenType.HEAD_OPEN)
        self.current_node.children.append(head_node)
        self.stack.append(head_node)
        self.current_node = head_node

    def handle_title_open(self):
        title_node = ASTNode(TokenType.TITLE_OPEN)
        self.current_node.children.append(title_node)
        self.stack.append(title_node)
        self.current_node = title_node

    def handle_body_open(self):
        body_node = ASTNode(TokenType.BODY_OPEN)
        self.current_node.children.append(body_node)
        self.stack.append(body_node)
        self.current_node = body_node

    def handle_h1_open(self):
        h1_node = ASTNode(TokenType.H1_OPEN)
        self.current_node.children.append(h1_node)
        self.stack.append(h1_node)
        self.current_node = h1_node

    def handle_p_open(self):
        p_node = ASTNode(TokenType.P_OPEN)
        self.current_node.children.append(p_node)
        self.stack.append(p_node)
        self.current_node = p_node

    def handle_content(self, content_value):
        self.current_node.children.append(ASTNode(TokenType.CONTENT, value=content_value))

    def handle_head_close(self):
        self.handle_close(TokenType.HEAD_OPEN)

    def handle_title_close(self):
        self.handle_close(TokenType.TITLE_OPEN)

    def handle_body_close(self):
        self.handle_close(TokenType.BODY_OPEN)

    def handle_h1_close(self):
        self.handle_close(TokenType.H1_OPEN)

    def handle_p_close(self):
        self.handle_close(TokenType.P_OPEN)

    def handle_html_close(self):
        self.handle_close(TokenType.HTML_OPEN)

    def handle_close(self, expected_open_token):
        if self.stack and self.stack[-1].type == expected_open_token:
            self.stack.pop()
            if self.stack:
                self.current_node = self.stack[-1]

        else:
            print(f"Error: Mismatched {expected_open_token.name.lower()} close token.")