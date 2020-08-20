from bot import Bot

bot = Bot()

bot.MENU_MAIS = "Mais"
bot.EXPORTAR = "Exportar conversa"
bot.INCLUIR_MIDIA = "INCLUIR ARQUIVOS DE MÍDIA"
bot.APP_NAME = "Extrator 0.4"
bot.SALVAR = "SALVAR"
bot.VOLTAR = "KEYCODE_BACK"
# bot.VOLTAR = "KEYCODE_ESCAPE"
bot.ROLAR_N_VEZES = 5
bot.parte_ultimo_chat = "9855-7826"
bot.verbose = False #coloque True caso queira debugar, para que ele te informe mais detalhes do que está fazendo

bot.extract()
