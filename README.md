# ParseBuillder

## О синтаксисе
ParseBuilder - библиотека для автоматического построения базовых парсеров для интерпретаторов.  Пока что библиотека строит парсеры лишь на Python, но в будущем планируется расширение функционала в виде поддаржки таких языков, как: C++, Go, Java/Kotlin. Для построения лексера можно воспользоваться библиотекой LexBuilder.

## Примеры
```python
from ParseBuilder.Builder import PyBuilder


parser = PyBuilder()
parser.build()
```

```python
from Lexer import *


class Parser:
    def __init__(self, lexer, symbol_table):
        '''
        Конструктор класса Parser.

        Параметры:
        - lexer: экземпляр класса Lexer для токенизации входного текста.
        - symbol_table: экземпляр класса SymbolTable для отслеживания переменных.

        symbol_table - объект класса SymbolTable, используется для
        хранения и управления переменными.
        '''
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.symbol_table = symbol_table

    def eat(self, token_type):
        '''
        Функция проверяет текущий токен и токен, с которого
        мы хотим перейти на другой токен.
        То есть у нас не получиться будучи на Token(VAR, "x") перейти на
        следущий токен с того, которого мы передаём в функцию:
        Текущий токен: VAR, мы передали в функцию токен PRINT -
        получаем ошибку, потому что мы находимся на токене VAR, а хотим перейти
        на следующий токен с токена PRINT.
        '''
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception(f"Error eating {self.current_token.type} token!")

    def factor(self):
        '''
        Функция отвечает за использование встроенных функций языка или других
        токенов которые возвращают значения:
        ... = input()
        ... = int(x)
        ... = True
        '''
        token = self.current_token
        if token.type == INT_NUMBER:
            self.eat(INT_NUMBER)
            return int(token.value)
        elif token.type == FLOAT_NUMBER:
            self.eat(INT_NUMBER)
            return float(token.value)
        elif token.type == STRING:
            string_value = token.value
            self.eat(STRING)
            return string_value
        elif token.type == VAR:
            var_name = token.value
            self.eat(VAR)
            return self.symbol_table.lookup(var_name)

    def term(self):
        '''
        Обработка терма (произведения или частного).

        Возвращает:
        - Результат вычисления терма.
        '''
        result = self.factor()

        while self.current_token.type in (MULTIPLY, DIVIDE):
            token = self.current_token
            if token.type == MULTIPLY:
                self.eat(MULTIPLY)
                result *= self.factor()
            elif token.type == DIVIDE:
                self.eat(DIVIDE)
                result /= self.factor()

        return result

    def expr(self):
        '''
        Обработка выражения (суммы или разности).

        Возвращает:
        - Результат вычисления выражения.
        '''
        result = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result += self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result -= self.term()

        return result

    def statement(self):
        '''
        Функция отвечает за встроенные функции и конструкции,
        которые не возвращают значения:
          print ...
          var = ...
          if ...

        '''
        if self.current_token.type == VAR:
            var_name = self.current_token.value
            self.eat(VAR)
            if self.current_token.type == ASSIGN:
                self.eat(ASSIGN)
                value = self.expr()
                self.symbol_table.define(var_name, value)
            else:
                sys.exit()

        else:
            self.current_token = self.lexer.get_next_token()

    def parse(self):
        '''
        Парсинг входного текста и выполнение выражений.

        Эта функция запускает парсинг входного текста и последовательно выполняет
        выражения, включая присваивание переменных и вывод значений.
        '''
        while self.current_token.type != EOF:
            self.statement()
```