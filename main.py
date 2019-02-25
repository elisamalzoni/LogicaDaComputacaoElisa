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
        while self.position < len(self.origin) and self.origin[self.position]==' ':
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
        else:
            raise Exception('caracter invalido')
        return self.actual
class Parser:

    def parseExpression():
        resultado = 0
        if Parser.tokens.actual.type_t == 'INT':
            resultado = int(Parser.tokens.actual.value)

            Parser.tokens.selectNext()
            while Parser.tokens.actual.type_t == 'MINUS' or Parser.tokens.actual.type_t == 'PLUS':
                if Parser.tokens.actual.type_t == 'PLUS':
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type_t == 'INT':
                        resultado += int(Parser.tokens.actual.value)
                    else:
                        raise Exception('ordem invalida')
                
                elif Parser.tokens.actual.type_t == 'MINUS':
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type_t == 'INT':
                        resultado -= int(Parser.tokens.actual.value)
                    else:
                        raise Exception('ordem invalida')
                Parser.tokens.selectNext()
        
        # senao erro? ?????????
        # raise Exception('ordem invalida')

        return resultado



    def run(code):
        Parser.tokens = Tokenizer(code)
        print(Parser.parseExpression())


# print('running: 1+2')
# Parser.run('1+2')
# print('running: 1+2-3')
# Parser.run('1+2-3')
# print('running: 11+22-33')
# Parser.run('11+22-33')
# print('running: 789   +345  -   123')
# Parser.run('789   +345  -   123')

exp = input('digite a expressão: ')
Parser.run(exp)