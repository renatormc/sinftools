import os
import sys


if len(sys.argv) > 1 and (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
    print("Cria várias pastas com o mesmo nome numeradas. \n   -l cria dentro das pastas 'midia' e 'extracoes'")
    sys.exit()


if len(sys.argv) > 1 and sys.argv[1] == "-l":
    nome_base = input("Nome base: ")
    quantidade = int(input("Quantidade: "))
    if not os.path.exists("extracoes"):
        os.mkdir("extracoes")

    if not os.path.exists("midia"):
        os.mkdir("midia")
    
    if not os.path.exists("midia\\gravar\\dados"):
        os.mkdir("midia\\gravar\\dados")

    for i in range(quantidade):
        os.mkdir("extracoes\\{}{}".format(nome_base, i + 1))

    for i in range(quantidade):
        os.mkdir("midia\\{}{}".format(nome_base, i + 1))
    
    for i in range(quantidade):
        os.mkdir("midia\\gravar\\dados\\{}{}".format(nome_base, i + 1))

elif len(sys.argv) == 1:
    nome_base = input("Nome base: ")
    quantidade = int(input("Quantidade: "))
    for i in range(quantidade):
        os.mkdir("{}{}".format(nome_base, i + 1))