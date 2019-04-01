import re
reserved = ['PRINT', 'END', 'BEGIN']
PRINT, END, BEGIN = reserved

class SymbolTable():
    def __init__(self):
        self.table = {}

    def setVariable(self, variable_name, variable_value):
        self.table[variable_name] = variable_value

    def getVariable(self, variable_name):
        if variable_name in self.table:
            return self.table[variable_name]
        else:
            raise Exception('Variavel nao declarada')
        
class Node():
    def __init__(self):
        self.value = None
        self.children = []

    def Evaluate(self, st):
        pass

class BinOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        if self.value == '-':
            return self.children[0].Evaluate(st) - self.children[1].Evaluate(st)

        elif self.value == '+':
            return self.children[0].Evaluate(st) + self.children[1].Evaluate(st)
        
        elif self.value == '*':
            return self.children[0].Evaluate(st) * self.children[1].Evaluate(st)

        elif self.value == '/':
            return self.children[0].Evaluate(st) // self.children[1].Evaluate(st)

class UnOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        if self.value == '-':
            return  -self.children[0].Evaluate(st)

        elif self.value == '+':
            return self.children[0].Evaluate(st)

class IntVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        return self.value

class IdentifierOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        return st.getVariable(self.value)

class AssigmentOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        st.setVariable(self.children[0].value, self.children[1].Evaluate(st))

class StatementsOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        for child in self.children:
            child.Evaluate(st)

class PrintOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        print(self.children[0].Evaluate(st))

class NoOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        pass

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
        ps = ''
        while self.position < len(self.origin) and (self.origin[self.position]==' '):
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
        elif self.position < len(self.origin) and self.origin[self.position] == '=':
            self.actual = Token('ASSIGNMENT', '=')
            self.position += 1
        elif self.origin[self.position] == '\n':
            self.actual = Token('LB', '\n')
            self.position += 1
        elif self.position < len(self.origin) and self.origin[self.position].isalpha():
            ps += self.origin[self.position]
            self.position += 1
            while self.position < len(self.origin) and (self.origin[self.position].isalpha() or self.origin[self.position].isdigit() or self.origin[self.position] == '_'):
                ps += self.origin[self.position]
                self.position += 1
            ps = ps.upper()
            if ps in reserved:
                self.actual = Token(ps, ps)
            else:
                self.actual = Token('IDENTIFIER', ps)
        else:
            raise Exception('caracter invalido')
        return self.actual

class PrePro:
    def filter(code):
        filtered_code = re.sub("'.*\n", "\n", code)
        # replace tab 4 espacos
        filtered_code_no_tab = re.sub("\t", "    ", filtered_code)
        # print(filtered_code)
        return filtered_code_no_tab

class Parser:
    
    def parseFactor():
        if Parser.tokens.actual.type_t == 'INT':
            node = IntVal(int(Parser.tokens.actual.value), [])
            Parser.tokens.selectNext()

        elif Parser.tokens.actual.type_t == 'IDENTIFIER':
            node = IdentifierOp(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()

        elif Parser.tokens.actual.type_t == 'OP':
            Parser.tokens.selectNext()
            node = Parser.parseExpression()
            if Parser.tokens.actual.type_t == 'CP':
                Parser.tokens.selectNext()
            else:
                raise Exception('Nao fechou parenteses')
        
        elif Parser.tokens.actual.type_t == 'PLUS':
            Parser.tokens.selectNext()
            node = UnOp("+",[Parser.parseFactor()])

        elif Parser.tokens.actual.type_t == 'MINUS':
            Parser.tokens.selectNext()
            node = UnOp("-",[Parser.parseFactor()])

        else:
            raise Exception('token invalido')

        return node

    def parseTerm():
        node = Parser.parseFactor()
        while Parser.tokens.actual.type_t == 'DIV' or Parser.tokens.actual.type_t == 'MULT':
            if Parser.tokens.actual.type_t == 'MULT':
                Parser.tokens.selectNext()
                node = BinOp('*', [node, Parser.parseFactor()])

            elif Parser.tokens.actual.type_t == 'DIV':
                Parser.tokens.selectNext()
                node = BinOp('/', [node, Parser.parseFactor()])
        return node


    def parseExpression():
        node = Parser.parseTerm()
        while Parser.tokens.actual.type_t == 'MINUS' or Parser.tokens.actual.type_t == 'PLUS':
            if Parser.tokens.actual.type_t == 'PLUS':
                Parser.tokens.selectNext()
                node = BinOp('+', [node, Parser.parseTerm()])

            elif Parser.tokens.actual.type_t == 'MINUS':
                Parser.tokens.selectNext()
                node = BinOp('-', [node, Parser.parseTerm()])
        return node

    def parseStatement():
        if Parser.tokens.actual.type_t == 'IDENTIFIER':
            variable_name = IdentifierOp(Parser.tokens.actual.value,[])
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type_t == 'ASSIGNMENT':
                Parser.tokens.selectNext()
                variable_value = Parser.parseExpression()
                node = AssigmentOp("=",[variable_name, variable_value])
        elif Parser.tokens.actual.type_t == 'PRINT':
            Parser.tokens.selectNext()
            node = PrintOp('PRINT', [Parser.parseExpression()])
        elif Parser.tokens.actual.type_t == 'BEGIN':
            node = Parser.parseStatements()
            # Parser.tokens.selectNext()
        else:
            node = NoOp(None, [])

        return node
        
    def parseStatements():
        node = StatementsOp('',[])
        if Parser.tokens.actual.type_t == 'BEGIN':
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type_t == 'LB':
                Parser.tokens.selectNext()
                while Parser.tokens.actual.type_t != 'END': 
                    node.children.append(Parser.parseStatement())
                    if Parser.tokens.actual.type_t == 'LB':
                        Parser.tokens.selectNext()
                    else:
                        raise Exception('faltou LB')
                if Parser.tokens.actual.type_t == 'END':
                    Parser.tokens.selectNext()
                    # while Parser.tokens.actual.type_t == 'LB':
                    #     Parser.tokens.selectNext()
                else:
                    raise Exception('faltou END')
            else:
                raise Exception('esperando LB do begin')
            
        else:
            raise Exception('sem BEGIN')
        return node
            

    def run(code):
        filtered_code = PrePro.filter(code)
        Parser.tokens = Tokenizer(filtered_code)
        res = Parser.parseStatements()
        while Parser.tokens.actual.type_t == 'LB':
            Parser.tokens.selectNext()
        if Parser.tokens.actual.type_t == 'EOF':
            return res
        else:
            raise Exception('nao chegou no EOF')


# exp = input('digite a expressão: ') + "\n"

with open('input.vbs', 'r') as f:
    exp = f.read() + '\n'

print(exp)
st = SymbolTable()
Parser.run(exp).Evaluate(st)