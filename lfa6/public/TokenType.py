import enum


class TokenType(enum.Enum):
    HTML_OPEN = 1
    HTML_CLOSE = 2
    HEAD_OPEN = 3
    HEAD_CLOSE = 4
    TITLE_OPEN = 5
    TITLE_CLOSE = 6
    BODY_OPEN = 7
    BODY_CLOSE = 8
    H1_OPEN = 9
    H1_CLOSE = 10
    P_OPEN = 11
    P_CLOSE = 12
    CONTENT = 13

    def __eq__(self, value: object) -> bool:
        return super().__eq__(value)