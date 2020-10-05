class NumeroExtenso():
    trioextenso = ()
    classextenso = ()

    def __init__(self):
        self.trioextenso_masculino = (
            ("dummy", "um", "dois", "três", "quatro", "cinco", "seis", "sete",
                      "oito", "nove"),
            ("dez", "onze", "doze", "treze", "quatorze", "quinze", "dezesseis",
             "dezessete", "dezoito", "dezenove"),
            ("dummy", "dummy", "vinte", "trinta", "quarenta", "cinquenta",
                      "sessenta", "setenta", "oitenta", "noventa"),
            ("dummy", "cento", "duzentos", "trezentos", "quatrocentos",
                      "quinhentos", "seiscentos", "setecentos", "oitocentos",
                      "novecentos"))
        self.trioextenso_feminino = (
            ("dummy", "uma", "duas", "três", "quatro", "cinco", "seis", "sete",
                      "oito", "nove"),
            ("dez", "onze", "doze", "treze", "quatorze", "quinze", "dezesseis",
             "dezessete", "dezoito", "dezenove"),
            ("dummy", "dummy", "vinte", "trinta", "quarenta", "cinquenta",
                      "sessenta", "setenta", "oitenta", "noventa"),
            ("dummy", "cento", "duzentas", "trezentas", "quatrocentas",
                      "quinhentas", "seiscentas", "setecentas", "oitocentas",
                      "novecentas"))
        self.classextenso = (
            "dummy", "mil", "milh", "bilh", "trilh", "quatrilh",
            "quintilh", "sextilh", "septilh", "octilh",
            "nonilh", "decilh", "undecilh", "duodecilh",
                      "tredecilh", "quatordecilh", "quindecilh",
                      "sexdecilh", "setedecilh", "octodecilh",
                      "novedecilh", "vigesilh")
        self.trioextenso = self.trioextenso_masculino
        

    def escrever_trio_extenso(self, trio):
        """
        Retorna um trio por extenso.

        Entrada: trio na forma de string.

        Retorno: trio em extenso.
        """
        saida = []

        if trio == '100':
            # Erro antigo aqui. Consertado usando "return"
            return 'cem'
        elif trio == '000':
            return 'zero'
        else:
            c, d, u = trio
            c, d, u = int(c), int(d), int(u)

            if c != 0:
                saida.append(self.trioextenso[3][c])
            if d == 1:
                saida.append(self.trioextenso[1][u])
            else:
                if d != 0:
                    saida.append(self.trioextenso[2][d])
                if u != 0:
                    saida.append(self.trioextenso[0][u])
        return ' e '.join(saida)

    def nao_e_ultimo_trio(self, totalTrios, contador):
        """
        Retorna verdadeiro se o trio indicado pelo contador
        não é o último (isso é, não é o mais à direita).

        Entrada: Número total de trios e o contador.

        Retorno: Verdadeiro se o trio NÃO é o último e
        falso caso contrário.
        """
        return contador < (totalTrios - 1)

    def trio_a_esquerda_eq_zero(self, trioLista, contador):
        """
        Retorna verdadeiro se o trio à esquerda do trio
        indicado pelo contador é igual a zero.

        Entrada: Os trios em forma de Lista e o contador.

        Retorno: Verdadeiro se o trio à esquerda do contador
        for zero e falso caso contrário.
        """

        # Contador igual a zero indexa o elemento mais à direita,
        # por isso devemos acrescentar tamanho da lista.
        t = len(trioLista)-1
        return trioLista[t-contador-1] == '000'

    def getExtenso(self, num, quebradelinhas=0, feminino=False):
        """
        Algoritmo principal. Recebe um número na forma de
        string e retorna sua escrita em extenso.

        Entrada: Número na forma de string e uma flag que, se
        tiver o valor 0 (zero), o extenso é retornado em uma
        só linha. Um valor 1 (um) faz o extenso ser quebrado
        em várias linhas.

        Retorno: O número de entrada em extenso na forma de
        string.
        """
        self.trioextenso = self.trioextenso_feminino if feminino else self.trioextenso_masculino
        # Remove os zeros iniciais e faz padding
        # para números com quantidade de algarismos
        # não múltipla de 3
        num = num.lstrip('0')
        pad = 3 - len(num) % 3
        if pad < 3:
            num = '0'*pad + num

        it = iter(num)
        trioLista = [''.join([a, b, c]) for a, b, c in zip(it, it, it)]

        if len(trioLista) > len(self.classextenso):
            raise IndexError('Número muito grande')

        contador = 0
        saida = ''
        extensofinal = ''

        for trio in reversed(trioLista):
            trioInt = int(trio)

            if trioInt > 0:
                saida = self.escrever_trio_extenso(trio)
                if contador > 0:
                    saida = saida + ' ' + self.classextenso[contador]
                if contador > 1:
                    if trioInt > 1:
                        saida = saida + 'ões'
                    else:
                        saida = saida + 'ão'
                if quebradelinhas == 0:
                    if self.nao_e_ultimo_trio(len(trioLista), contador):
                        if self.trio_a_esquerda_eq_zero(trioLista, contador):
                            saida = ' e ' + saida
                        elif trioInt >= 100:
                            saida = ', ' + saida
                        else:
                            saida = ' e ' + saida
                else:
                    saida = saida + '\n'

                extensofinal = saida + extensofinal
            contador = contador + 1
        return extensofinal.rstrip('\n')


def get_extenso(num, feminino=False):
    if not isinstance(num, str):
        num = str(num)
    n = NumeroExtenso()
    return n.getExtenso(num, quebradelinhas=0, feminino=feminino)


if __name__ == "__main__":
    print(get_extenso(1, feminino=True))
