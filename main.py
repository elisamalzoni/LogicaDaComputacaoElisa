import re
class Token:
    def __init__(self, type_t, value):
        self.type_t = type_t
        self.value = value

class Tokenizer:
    def __init__(self, origin):
        self.origin = origin
        self.position = 0
        self.actual = self.selectNext()

    def selectNext(self):
        num = ''
        while self.position < len(self.origin) and (self.origin[self.position]==' ' or self.origin[self.position]=='\n'):
            self.position += 1
        if self.position == len(self.origin):
            self.actual = Token('EOF', 'e')
        elif self.origin[self.position].isdigit():
            while self.position < len(self.origin) and self.origin[self.position].isdigit():
                num = num + self.origin[self.position]
                self.position += 1
            self.actual = Token('INT', num)
        elif self.position < len(self.origin) and self.origin[self.position] == '-':
            self.actual = Token('MINUS', '-')
            self.position += 1
        elif self.position < len(self.origin) and self.origin[self.position] == '+':
            self.actual = Token('PLUS', '+')
            self.position += 1
        elif self.position < len(self.origin) and self.origin[self.position] == '*':
            self.actual = Token('MULT', '*')
            self.position += 1
        elif self.position < len(self.origin) and self.origin[self.position] == '/':
            self.actual = Token('DIV', '/')
            self.position += 1
        elif self.position < len(self.origin) and self.origin[self.position] == '(':
            self.actual = Token('OP', '(')
            self.position += 1
        elif self.position < len(self.origin) and self.origin[self.position] == ')':
            self.actual = Token('CP', ')')
            self.position += 1
        else:
            raise Exception('caracter invalido')
        return self.actual

class PrePro:
    def filter(code):
        filtered_code = re.sub("'.*\n", "", code)
        # print(filtered_code)
        return filtered_code

class Parser:
    def parseFactor():
        resultado = 0
        if Parser.tokens.actual.type_t == 'INT':
            resultado = int(Parser.tokens.actual.value)
            Parser.tokens.selectNext()
        elif Parser.tokens.actual.type_t == 'OP':
            Parser.tokens.selectNext()
            resultado = Parser.parseExpression()
            if Parser.tokens.actual.type_t == 'CP':
                Parser.tokens.selectNext()
            else:
                raise Exception('Nao fechou parenteses')
        
        elif Parser.tokens.actual.type_t == 'PLUS':
            Parser.tokens.selectNext()
            resultado += Parser.parseFactor()

        elif Parser.tokens.actual.type_t == 'MINUS':
            Parser.tokens.selectNext()
            resultado -= Parser.parseFactor()

        else:
            raise Exception('token invalido')

        return resultado

    def parseTerm():
        factor = Parser.parseFactor()
        resultado = factor
        while Parser.tokens.actual.type_t == 'DIV' or Parser.tokens.actual.type_t == 'MULT':
            if Parser.tokens.actual.type_t == 'MULT':
                Parser.tokens.selectNext()
                resultado = resultado * int(Parser.parseFactor())

            elif Parser.tokens.actual.type_t == 'DIV':
                Parser.tokens.selectNext()
                resultado = resultado // int(Parser.parseFactor())
        return resultado


    def parseExpression():
        term = Parser.parseTerm()
        resultado = term
        while Parser.tokens.actual.type_t == 'MINUS' or Parser.tokens.actual.type_t == 'PLUS':
            if Parser.tokens.actual.type_t == 'PLUS':
                Parser.tokens.selectNext()
                resultado += Parser.parseTerm()

            elif Parser.tokens.actual.type_t == 'MINUS':
                Parser.tokens.selectNext()
                resultado -= Parser.parseTerm()
        return resultado

    def run(code):
        filtered_code = PrePro.filter(code)
        Parser.tokens = Tokenizer(filtered_code)
        res = Parser.parseExpression()
        if Parser.tokens.actual.type_t == 'EOF':
            return res
        else:
            raise Exception('nao chegou no EOF')


exp = input('digite a expressão: ') + "\n"

# f = open('input.txt', 'r') 
# exp = f.read() 
# print(exp)

print(Parser.run(exp))