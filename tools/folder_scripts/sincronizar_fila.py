import pandas as pd
import MySQLdb
arquivo = r'C:\Users\renato\Downloads\teste.xlsx'
df = pd.read_excel(arquivo)



# con = MySQLdb.connect(user='sinf', password='iclrsinf',
#                               host='10.129.3.14',
#                               database='pericias')
con = MySQLdb.connect(user='root', password='808452',
                              host='localhost',
                              database='pericias')
cursor = con.cursor()


def normalizaObjetos(row):
    string  = row['Objetos.1']
    listaString = string.split(';')
    numCel = 0;
    numComp = 0;
    numObj = 0;
    for xstr in listaString:
        xstr = xstr.strip()
        xstr = xstr.lower()
       # print(xstr)
        if 'celular' in xstr:
            listaNum = xstr.split()
            #print(listaNumCel[0])
            try:
                if(len(xstr) >4):
                    numCel += int(listaNum[0])
            except:
                pass
               # print('error')

        elif 'cpu' in xstr or 'notebook' in xstr or xstr == 'hd':
            listaNum = xstr.split()
            #print(listaNumCel[0])
            try:
                if(len(xstr) >4):
                    numComp += int(listaNum[0])
            except:
                pass
               # print('error')
        else:
            if(len(xstr) >4):
                listaNum = xstr.split()
                try:
                    numObj += int(listaNum[0])
                except:
                    pass
                    #print('error')
    return {
        "cel": numCel,
        "comp": numComp,
        "obj": numObj
    }


def existe(sinf, rg, ano):
    cursor.execute("SELECT sinf, rg, ano FROM pericia WHERE sinf=%s AND rg=%s AND ano=%s", (int(sinf),int(rg),int(ano)))
    if cursor.fetchone():
        return True
    else:
        return False

def inserirNovo(row):
    pass


for i, row in df.iterrows():
    sinf, rg, ano = row['INT'], row['RG'], row['Ano']
    if not existe(sinf, rg, ano):
        objetos = normalizaObjetos(row)
        registro = (row['Entrada'].strftime('%d/%m/%Y'), row['INT'], row['RG'], row['Ano'], objetos['cel'], objetos['comp'], objetos['obj'], row['Objetos.1'])
        cursor.execute("INSERT INTO pericia (data_entrada, sinf, rg, ano, qtd_celulares, qtd_computadores, qtd_outros_objetos, observacao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", registro)
        print("Inserido SINF {}/{}".format(sinf, ano))