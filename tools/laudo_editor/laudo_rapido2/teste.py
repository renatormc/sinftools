import re

text ="""21/07/19 9:40 PM - As mensagens e chamadas dessa conversa estão protegidas com criptografia de ponta a ponta. Toque para mais informações.
21/07/19 9:40 PM - Piqueno: Opa boa noite
21/07/19 9:40 PM - Piqueno: 🤝🏾
21/07/19 10:16 PM - Luta Academia: Olá quem fala
21/07/19 11:16 PM - Piqueno: Adryan
21/07/19 11:16 PM - Piqueno: Eu queria fala sobre sua academia
21/07/19 11:16 PM - Piqueno: Como fuciona
21/07/19 11:17 PM - Piqueno: Queria luta
21/07/19 11:17 PM - Piqueno: Treina
22/07/19 10:34 AM - Piqueno: Iae amigao?
22/07/19 1:07 PM - Luta Academia: Boa tarde amigo q horas vc quer treina
22/07/19 1:10 PM - Piqueno: Di dia amigo
22/07/19 1:10 PM - Piqueno: Qual e o valor?
22/07/19 1:11 PM - Luta Academia: Todos os dias e 100 Quatro vezes e 90 Três vezes e 80
22/07/19 1:18 PM - Piqueno: Eu ia quere todo dia
22/07/19 1:18 PM - Piqueno: Q horas Posso ir ai conhece tudo
22/07/19 1:18 PM - Piqueno: ??
22/07/19 1:19 PM - Luta Academia: As 18:30
22/07/19 1:20 PM - Piqueno: Blz eu vou ai 
Ai nois conversa melhor blz
22/07/19 1:22 PM - Luta Academia: Blz 👍
22/07/19 6:07 PM - Piqueno: Iae amigo
22/07/19 6:07 PM - Piqueno: To indo ae blz
22/07/19 6:11 PM - Luta Academia: Blz"""

# text = "21/07/19 9:40 PM - Piqueno: Opa boa noite"

message_text = re.sub(r'((\d{2}/\d{2}/\d{2})?\s(\d{1,2}:\d{2} ((PM)|(AM))))', r'<!@#$%>\1', text)
splitted_text = message_text.split('<!@#$%>')[1:]

reg = re.compile(r'(?P<timestamp>(\d{2}/\d{2}/\d{2})?\s+(\d{1,2}:\d{2} ((PM)|(AM))))?\s+?(-(?P<from>.*?):)?\s?(?P<body>.*)')
for line in splitted_text:
    res = reg.findall(line)
    print(res[0])

# res = reg.findall(text)
# print(res[0])

