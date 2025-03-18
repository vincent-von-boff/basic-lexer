# Basic Lexer


A basic lexer for a basic language, written in Python.

Usage
-----


./input_file_example.txt
```C
#include <stdlib.h>

int main(void){
  return 42;
}

```

The file above will give the following output:

```Console
>> py main.py ./input_file_example.txt

Input text: 
#include <stdlib.h>

int main(void){
        return 42;
    }

TOKEN( Value: #, Type: Token_t.HASH_SYMB)
TOKEN( Value: include, Type: Token_t.NAME)
TOKEN( Value: <, Type: Token_t.LESS_THAN_SIGN)
TOKEN( Value: stdlib, Type: Token_t.NAME)
TOKEN( Value: ., Type: Token_t.PERIOD)
TOKEN( Value: h>, Type: Token_t.NAME)
TOKEN( Value: , Type: Token_t.NEW_LINE)
TOKEN( Value: , Type: Token_t.NEW_LINE)
TOKEN( Value: int, Type: Token_t.NAME)
TOKEN( Value: main, Type: Token_t.NAME)
TOKEN( Value: (, Type: Token_t.OPEN_PAREN)
TOKEN( Value: void, Type: Token_t.NAME)
TOKEN( Value: ), Type: Token_t.CLOSE_PAREN)
TOKEN( Value: {, Type: Token_t.OPEN_CURLY)
TOKEN( Value: , Type: Token_t.NEW_LINE)
TOKEN( Value: return, Type: RETURN_KW)
TOKEN( Value: 42, Type: Token_t.NUMBER)
TOKEN( Value: ;, Type: Token_t.SEMICOLON_SIGN)
TOKEN( Value: , Type: Token_t.NEW_LINE)
TOKEN( Value: }, Type: Token_t.CLOSE_CURLY)
TOKEN( Value: , Type: Token_t.NEW_LINE)
Error_t.EOF


Error log:
[ERROR(type=<Error_t.EOF: 2>, location=Location(pos=62, char=''), message='Lexer has reached end of file.')]

>>
```
