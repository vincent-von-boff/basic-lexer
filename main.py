import string
from enum import Enum, auto
from dataclasses import dataclass
from typing import List

class Error_t(Enum):
    SUCCESS = auto()
    EOF = auto()
    INVALID_CHAR = auto()
    EMPTY_STRING = auto()
    UNKNOWN_CHAR = auto()

    def __bool__(self):
        return False

@dataclass
class Location:
    pos : int
    char: str

@dataclass
class ERROR:
    type : Error_t
    location : Location
    message : str

class Token_t(Enum):
    NUMBER = auto()
    NAME = auto()

    # Keywords
    FUNC_KW = "function"
    RETURN_KW = "return"
    FOR_KW = "for"
    IF_KW = "if"
    ELSE_KW = "else"
    THEN_KW = "then" 
    WHILE_KW = "while"
    
    PLUS_SIGN = auto()
    MINUS_SIGN = auto()
    MULT_SIGN = auto()
    DIV_SIGN = auto()
    LESS_THAN_SIGN = auto()
    GREATER_THAN_SIGN = auto()
    OPEN_PAREN = auto()
    CLOSE_PAREN = auto()
    OPEN_BRACKET = auto()
    CLOSE_BRACKET = auto()
    OPEN_CURLY = auto()
    CLOSE_CURLY = auto()
    CARROT = auto()
    BAR = auto()
    PERCENT_SIGN = auto()
    EQUALS_SIGN = auto()
    COLON_SIGN = auto()
    SEMICOLON_SIGN = auto()
    INC_SIGN = auto()
    DEC_SIGN = auto()
    EXP_SIGN = auto()
    INC_BY_SIGN = auto()
    DEC_BY_SIGN = auto()
    MULT_ASSIGN_SIGN = auto()
    GREATER_EQ_SIGN = auto()
    LESS_EQ_SIGN = auto()
    LOGIC_EQ_SIGN = auto()
    TYPE_DECLARATION = auto()
    HASH_SYMB = auto()
    PERIOD = auto()
    COMMA = auto()

    NEW_LINE = auto()
    TAB = auto()

    STRING_LITERAL = auto()


class Token:
    def __init__(self, type, value=""):
        self.type : Token_t = type
        self.value : str = value

    def __str__(self):
        return f"TOKEN( Value: {self.value}, Type: {self.type})"

class Lexer:
    def __init__(self, text):
        self.initial_text : str= text
        self.text : str= text
        self.txt_size : int = len(text)

        self.pos : int = 0 # current position on string
        if not self.text:
            self.current : str=  ""
        else:
            self.current : str= self.text[self.pos]

        self.error_log : List[ERROR] = []

        self.valid_chars : str= string.ascii_letters + string.digits + ".,#:;.,><+*/-()^|%=[]{}'\" \n \t"
        self.valid_name_chars : str= string.ascii_letters + "_"
        if not all(char in self.valid_chars for char in self.text):
            self.push_error(ERROR(Error_t.INVALID_CHAR, Location(0,''), "Input string contain invalid characters."))
        
        self.keywords = [
            "function",
            "return",
            "for",
            "if",
            "else",
            "then",
            "while"
            ]

    def next(self):
        # print("debug: " + str(self.pos))
        if self.pos < self.txt_size - 1:
            self.pos += 1
            self.current = self.text[self.pos]
        elif self.pos == (self.txt_size - 1):
            self.pos += 1
            self.current = ""
        else:
            return self.current
        return self.current

    def peek(self) -> str:
        if self.pos >= self.txt_size - 1:
            return ""
        return self.text[self.pos + 1]

    def push_error(self, err : ERROR) -> None:
        self.error_log.append(err)

    def lex(self):
        # crop_blank: TO DO
        value = ""

        # lex_keyword()

        if not self.text:
            err = ERROR(Error_t.EMPTY_STRING, Location(0, ""), "Cannot tokenize empty string.")
            self.push_error(err)
            return Error_t.EMPTY_STRING

        while self.current == ' ':
            self.next()

        if self.current not in self.valid_chars:
            loc = Location(self.pos, self.current)
            self.push_error(ERROR(Error_t.INVALID_CHAR, loc, f"The character {self.current} is not allowed."))
            return Error_t.INVALID_CHAR

        if (self.pos == self.txt_size):
            loc = Location (self.pos, self.current)
            err = ERROR(Error_t.EOF, loc, "Lexer has reached end of file.")
            self.push_error(err)
            return Error_t.EOF

        # Lex number
        if self.current.isdigit() :
            save_pos = self.pos
            value = self.current
            self.next()
            while self.current.isdigit():
                value += self.current
                self.next()
            return Token(Token_t.NUMBER, value)

        # Lex name
        if self.current.isalnum() :
            save_pos = self.pos
            value = self.current
            value += self.next()
            i = self.peek()
            while i in self.valid_name_chars and i != "":
                value += self.next()
                i = self.peek()
            self.next()
            if value in self.keywords:
                token_type = [tk_type.name for tk_type in Token_t if tk_type.value == value][0]
                return Token(token_type, self.text[save_pos: self.pos])
            else:
                return Token(Token_t.NAME, self.text[save_pos: self.pos])

        # ><+*/-()^|%
        if self.current == '+':
            value = self.current
            self.next()
            if self.current == '+':
                self.next()
                value = "++"
                return Token(Token_t.INC_SIGN, value) 
            if self.current == '=':
                self.next()
                value = "+="
                return Token(Token_t.INC_BY_SIGN, value) 
            return Token(Token_t.PLUS_SIGN, value) 
        if self.current == '-':
            value = self.current
            self.next()
            if self.current == '-':
                self.next()
                value = "--"
                return Token(Token_t.DEC_SIGN, value) 
            if self.current == '=':
                self.next()
                value = "-="
                return Token(Token_t.DEC_BY_SIGN, value) 
            return Token(Token_t.MINUS_SIGN, value) 
        if self.current == '*':
            value = self.current
            self.next()
            if self.current == '*':
                self.next()
                value = "**"
                return Token(Token_t.EXP_SIGN, value) 
            if self.current == '=':
                self.next()
                value = "*="
                return Token(Token_t.MULT_ASSIGN_SIGN, value) 
            return Token(Token_t.MULT_SIGN, value) 
        if self.current == '/':
            value = self.current
            self.next()
            return Token(Token_t.DIV_SIGN, value) 
        if self.current == '>':
            value = self.current
            self.next()
            if self.current == '=':
                self.next()
                value = ">="
                return Token(Token_t.GREATER_EQ_SIGN, value) 
            return Token(Token_t.GREATER_THAN_SIGN, value)
        if self.current == '<':
            value = self.current
            self.next()
            if self.current == '=':
                self.next()
                value = "<="
                return Token(Token_t.LESS_EQ_SIGN, value) 
            return Token(Token_t.LESS_THAN_SIGN, value)
        
        if self.current == '\n':
            value = ""
            self.next()
            return Token(Token_t.NEW_LINE, value) 
        if self.current == '\t':
            value = ""
            self.next()
            return Token(Token_t.TAB, value) 

        if self.current == '(':
            value = self.current
            self.next()
            return Token(Token_t.OPEN_PAREN, value) 
        if self.current == ')':
            value = self.current
            self.next()
            return Token(Token_t.CLOSE_PAREN, value) 
        if self.current == '[':
            value = self.current
            self.next()
            return Token(Token_t.OPEN_BRACKET, value) 
        if self.current == ']':
            value = self.current
            self.next()
            return Token(Token_t.CLOSE_BRACKET, value) 
        if self.current == '{':
            value = self.current
            self.next()
            return Token(Token_t.OPEN_CURLY, value) 
        if self.current == '}':
            value = self.current
            self.next()
            return Token(Token_t.CLOSE_CURLY, value) 
        if self.current == '.':
            value = self.current
            self.next()
            return Token(Token_t.PERIOD, value) 
        if self.current == ',':
            value = self.current
            self.next()
            return Token(Token_t.COMMA, value) 
        if self.current == '#':
            value = self.current
            self.next()
            return Token(Token_t.HASH_SYMB, value) 

        if self.current == '^':
            value = self.current
            self.next()
            return Token(Token_t.CARROT, value) 
        if self.current == '|':
            value = self.current
            self.next()
            return Token(Token_t.BAR, value) 
        if self.current == '%':
            value = self.current
            self.next()
            return Token(Token_t.PERCENT_SIGN, value) 
        if self.current == '=':
            value = self.current
            self.next()
            if self.current == '=':
                self.next()
                value = "=="
                return Token(Token_t.LOGIC_EQ_SIGN, value) 
            return Token(Token_t.EQUALS_SIGN, value) 
        if self.current == ':':
            value = self.current
            self.next()
            if self.current == ':':
                self.next()
                value = "::"
                return Token(Token_t.TYPE_DECLARATION, value) 
            return Token(Token_t.COLON_SIGN, value) 
        if self.current == ';':
            value = self.current
            self.next()
            return Token(Token_t.SEMICOLON_SIGN, value) 
        if self.current == "'":
            value = ""
            self.next()
            while self.current != "'":
                value += self.current
                self.next()
            self.next()
            return Token(Token_t.STRING_LITERAL, value) 
        if self.current == '"':
            value = ""
            self.next()
            while self.current != '"':
                value += self.current
                self.next()
            self.next()
            return Token(Token_t.STRING_LITERAL, value) 

        self.push_error(ERROR(Error_t.UNKNOWN_CHAR, 
                              Location(self.pos, self.current), 
                              "Cannot tokenize unknown char."))
        return Error_t.UNKNOWN_CHAR

with open("./input_test.txt") as file:
    input_test = file.read()
lexer = Lexer(input_test)
print("Input text: ")
print(lexer.text)
i = True
while i:
    i = lexer.lex()
    print(i)
print("\n")
print("Error log:")
print(lexer.error_log)
