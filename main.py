import re
import sys

reserved = ['PRINT', 'END', 'BEGIN', 'NOT', 'AND', 'OR', 'WHILE', 'WEND', 'IF', 'THEN', 'ELSE', 'INPUT']
PRINT, END, BEGIN, NOT, AND, OR, WHILE, WEND, IF, THEN, ELSE , INPUT= reserved

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

        elif self.value == '<':
            return self.children[0].Evaluate(st) < self.children[1].Evaluate(st)
        
        elif self.value == '>':
            return self.children[0].Evaluate(st) > self.children[1].Evaluate(st)

        elif self.value == '=':
            return self.children[0].Evaluate(st) == self.children[1].Evaluate(st)

        elif self.value == 'OR':
            return self.children[0].Evaluate(st) or self.children[1].Evaluate(st)

        elif self.value == 'AND':
            return self.children[0].Evaluate(st) and self.children[1].Evaluate(st)


class UnOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        if self.value == '-':
            return  -self.children[0].Evaluate(st)

        elif self.value == '+':
            return self.children[0].Evaluate(st)

        elif self.value == 'NOT':
            return not(self.children[0].Evaluate(st))  


class IntVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        return self.value

class IdentifierNode(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        return st.getVariable(self.value)

class AssignmentNode(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        st.setVariable(self.children[0].value, self.children[1].Evaluate(st))

class StatementsNode(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        for child in self.children:
            child.Evaluate(st)

class PrintNode(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        print(self.children[0].Evaluate(st))

class WhileNode(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        while self.children[0].Evaluate(st):
            self.children[1].Evaluate(st)
 
class IfNode(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        if self.children[0].Evaluate(st):
            self.children[1].Evaluate(st)
        elif len(self.children) == 3:
            self.children[2].Evaluate(st)

class InputNode(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        return int(input())

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
        elif self.position < len(self.origin) and self.origin[self.position] == '<':
            self.actual = Token('LESS', '<')
            self.position += 1
        elif self.position < len(self.origin) and self.origin[self.position] == '>':
            self.actual = Token('GREATER', '>')
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
            node = IdentifierNode(Parser.tokens.actual.value, [])
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

        elif Parser.tokens.actual.type_t == 'NOT':
            Parser.tokens.selectNext()
            node = UnOp("NOT",[Parser.parseFactor()])

        elif Parser.tokens.actual.type_t == 'INPUT':
            Parser.tokens.selectNext()
            node = InputNode("",[])

        else:
            raise Exception('token invalido')

        return node
    
    def parseRelExpression():
        node = Parser.parseExpression()
        if Parser.tokens.actual.type_t == 'LESS':
            Parser.tokens.selectNext()
            node = BinOp('<', [node, Parser.parseExpression()])

        elif Parser.tokens.actual.type_t == 'GREATER':
            Parser.tokens.selectNext()
            node = BinOp('>', [node, Parser.parseExpression()])
        
        elif Parser.tokens.actual.type_t == 'ASSIGNMENT':
            Parser.tokens.selectNext()
            node = BinOp('=', [node, Parser.parseExpression()])

        else:
            raise Exception('relexp invalida')

        return node



    def parseTerm():
        node = Parser.parseFactor()
        while Parser.tokens.actual.type_t == 'DIV' or Parser.tokens.actual.type_t == 'MULT' or Parser.tokens.actual.type_t == 'AND':
            if Parser.tokens.actual.type_t == 'MULT':
                Parser.tokens.selectNext()
                node = BinOp('*', [node, Parser.parseFactor()])

            elif Parser.tokens.actual.type_t == 'DIV':
                Parser.tokens.selectNext()
                node = BinOp('/', [node, Parser.parseFactor()])

            elif Parser.tokens.actual.type_t == 'AND':
                Parser.tokens.selectNext()
                node = BinOp('AND', [node, Parser.parseFactor()])

        return node


    def parseExpression():
        node = Parser.parseTerm()
        while Parser.tokens.actual.type_t == 'MINUS' or Parser.tokens.actual.type_t == 'PLUS' or Parser.tokens.actual.type_t == 'OR':
            if Parser.tokens.actual.type_t == 'PLUS':
                Parser.tokens.selectNext()
                node = BinOp('+', [node, Parser.parseTerm()])

            elif Parser.tokens.actual.type_t == 'MINUS':
                Parser.tokens.selectNext()
                node = BinOp('-', [node, Parser.parseTerm()])
            
            elif Parser.tokens.actual.type_t == 'OR':
                Parser.tokens.selectNext()
                node = BinOp('OR', [node, Parser.parseTerm()])

        return node

    def parseStatement():
        if Parser.tokens.actual.type_t == 'IDENTIFIER':
            variable_name = IdentifierNode(Parser.tokens.actual.value,[])
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type_t == 'ASSIGNMENT':
                Parser.tokens.selectNext()
                variable_value = Parser.parseExpression()
                node = AssignmentNode("=",[variable_name, variable_value])

        elif Parser.tokens.actual.type_t == 'PRINT':
            Parser.tokens.selectNext()
            node = PrintNode('PRINT', [Parser.parseExpression()])

        elif Parser.tokens.actual.type_t == 'WHILE':
            Parser.tokens.selectNext()
            node = WhileNode('WHILE', [Parser.parseRelExpression()])

            if Parser.tokens.actual.type_t == 'LB':
                Parser.tokens.selectNext()
                node.children.append(Parser.parseStatements())

                if Parser.tokens.actual.type_t == 'WEND':
                    Parser.tokens.selectNext()
                else:
                    raise Exception('nao existe wend')
            else:
                raise Exception('sem LB depois do WHILE')  

        elif Parser.tokens.actual.type_t == 'IF':
            Parser.tokens.selectNext()
            node = IfNode('IF', [Parser.parseRelExpression()])
            if Parser.tokens.actual.type_t == 'THEN':
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type_t == 'LB':
                    Parser.tokens.selectNext()
                    node.children.append(Parser.parseStatements())

                    if Parser.tokens.actual.type_t == 'ELSE':
                        Parser.tokens.selectNext()
                        if Parser.tokens.actual.type_t == 'LB':
                            Parser.tokens.selectNext()
                            node.children.append(Parser.parseStatements())
                        else:
                            raise Exception('sem LB depois do ELSE')
                    
                    if Parser.tokens.actual.type_t == 'END':
                        Parser.tokens.selectNext()

                        if Parser.tokens.actual.type_t == 'IF':
                            Parser.tokens.selectNext()
                        else:
                            raise Exception('falta IF em END IF')
                    else:
                        raise Exception('sem END do IF')
                else:
                    raise Exception('sem LB depois do THEN')
            else:
                raise Exception('falta THEN')
        else:
            node = NoOp(None, [])

        return node
        
    def parseStatements():

        filhosstatements = [Parser.parseStatement()]

        while (Parser.tokens.actual.type_t == 'LB'):
            Parser.tokens.selectNext()
            filhosstatements.append(Parser.parseStatement())

        return StatementsNode('', filhosstatements)
            

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


# $ python3 main.py test.vbs

with open(sys.argv[1], 'r') as f:
    exp = f.read() + '\n'

print(exp)
st = SymbolTable()
Parser.run(exp).Evaluate(st)