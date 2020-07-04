## configurar
from sinf.android_macro.connector import Connector
conn = Connector()
conn.set_image_folder(r'crop_regions')
conn.set_image_map({
    'menu': 5,
    'mais': 9,
    'exportar': 11,
    'incluir_midia': 12,
    'icone_app': 13,
    'lista_chats': 1,
    'tela_chat': 4,
    'tela_chat2': 3,
    'final_chats': 2,
    'menu_aberto': 7,
    'menu_aberto2': 10,
    'menu_aberto3': 8,
    'spi_ok': 11,
    'spi_screen': 12
})
conn.load_images()

## Testar
#Seta para baixo
conn.arrow_down()
#seta para cima
conn.arrow_up()
#tecla enter
conn.enter()
#Tecla esc
conn.scape()
#Tecla delete
conn.delete()
#Pressiona botão voltar do Android
conn.back()
#Achar imagem e clicar
conn.find_and_tap('menu')
#Achar imagem e clicar ou ignorar caso encontre uma das imagens dentre other
conn.find_or_pass('exportar', other=['menu_aberto', 'menu_aberto2', 'menu_aberto3'])
#Salvar um print da tela
conn.save_screen('print.png')
#Garantir que uma determinada tela está aberta, caso não espera um tempo para ela aparecer, caso não apareça gera um erro
conn.assert_screen('menu')
#Fica aguardando uma determinada tela aparecer para sempre
conn.wait_screen('mais')
#Checa se uma tela está aberta, sem esperar, retorna true ou false
conn.check_screen('mais')
#Executa um comando adb genérico
conn.exec("adb shell input keyevent 111")

## Executar em loop
for i in range(10000):
    print(f"Executando {i+1}")
    conn.enter(sleep=0.5)
    conn.assert_screen(['tela_chat', 'tela_chat2'])
    conn.find_and_tap('menu')
    conn.find_and_tap('mais')
    conn.find_or_pass('exportar', other=['menu_aberto', 'menu_aberto2', 'menu_aberto3'])
    conn.find_or_pass('incluir_midia', other=['menu_aberto', 'icone_app'])
    conn.find_or_pass('icone_app', other='menu_aberto')
    conn.find_and_tap('spi_ok')
    conn.assert_screen('spi_screen')
    
    conn.back()
    conn.back(sleep=0.5)
    conn.assert_screen('lista_chats')
    
    conn.arrow_down(sleep=1)
    conn.arrow_down(sleep=1)
    if i == 2:
        break
    if conn.check_screen('final_chats'):
        break

