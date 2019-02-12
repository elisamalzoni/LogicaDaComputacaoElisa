dici = {'n':[], 'op': []}

string_conta = input('Digite a conta: ')

resultado = 0
numero = ''

for c, caracter in enumerate(string_conta):
    if caracter != ' ':
        if caracter in ['+', '-']:
            if c != 0:
                dici['n'].append(numero)
            dici['op'].append(caracter)
            numero = ''
        else:
            numero = numero+caracter
        
        if c == (len(string_conta)-1):
            dici['n'].append(numero)

if len(dici['n']) != len(dici['op']):
    dici['op'].insert(0, '+')

for i, num in enumerate(dici['n']):
    sinal = dici['op'][i]
    numsinal = int(sinal+num)
    print(numsinal)
    resultado += numsinal
print('resultado: ', resultado)
