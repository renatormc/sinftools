import inquirer


def get_options():
   
    message = """\nA fim de otimização do tempo no cálculo do hash é recomendado não calcular 
o hash dos arquivos E01 e dos arquivos gerados pelo IPED pois por padrão já 
é feito este cálculo. O FTK Imager já calculou hash das imagens e o salvou 
nos arquivos de logs e também o IPED já calculou os hashes dos arquivos e os
salvou em um arquivo CSV. Sendo assim, não é necessário recalcular o que já 
foi calculado anteriormente.
O programa também é capaz de analisar as referências à arquivos de imagens 
no banco de dados do IPED e alterar as referências de endereços absolutos 
para endereços relativos deixando a mídia de resultados portável. 
    """
    print(message)
    questions = [
        inquirer.Checkbox('options', message="A seguir escolha as opções desejadas. Utilize espaço para selecionar ou desmacar",
                          choices=['Colocar iped portable', 'Não calcular hash de E01', 'Não calcular hash de indexação IPED'], default=['Colocar iped portable', 'Não calcular hash de E01', 'Não calcular hash de indexação IPED'])
    ]

    answers = inquirer.prompt(questions)
    return {
        'put_portable': 'Colocar iped portable' in answers['options'],
        'images_partial': 'Não calcular hash de E01' in answers['options'],
        'iped_partial': 'Não calcular hash de indexação IPED' in answers['options'],
    }
   
