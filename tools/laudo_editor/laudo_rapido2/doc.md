# Widgets
Os widgets serão mostrados na tela em linhas e colunas. A propriedade row define em qual linha do formulário aparecerá o widget. O fator stretch define qual a proporção cada widget ocupará em cada linha do formulário.

## Propriedades existentes de todos os widgets
#### name
Nome da variável que será repassada ao template
#### label
Rótulo eu aparecerá no formulário para preenchimento
#### converter
Pode ser utilizado para converter o formato antes de passar o valor para o template. Caso não seja utilizado será passado para o template como string. Caso o conversor utilize outro parâmetro de entrada além do valor do formulário é necessário definir o conversor como uma lista. Ex: ["str2datetime", "%d/%m/%Y %H:%M"]
#### mask
Especificar uma máscara de entrada. Ex: 00/00/000 para datas.
#### validator
Expressão regex para definir os valores válidos na entrada
#### mask
Especificar uma máscara de entrada. Ex: 00/00/000 para datas.
#### default
Valor padrão para já aparecer preenchido de início
#### editable
Se definido como true além das opções da lista é possível inserir outra.
Valor booleano: true ou false
#### list
Lista de ítems para escolha. Pode-se entrar uma lista direto no json ou inserir um arquivo do tipo txt dentro da pasta “listas” e no json colocar somente o nome da lista sem a extensão.
#### caption
Legenda
#### width
Largura
#### row
Linha do formulário
#### stretch
Define qual a fração da linha ocupará cada widget
#### initial
Quantidade de item iniciais quando utilizando o widget "repeat"
## line_edit
```
{
	"type": "edit",
	"name": "data_pericia",
	"default": "",
	"label": "Data da perícia",
	"mask": "00/00/0000",
	"converter": ["str2datetime", "%d/%m/%Y"],
	"validator": "\\d{2}/\\d{2}/\\d{4}",
	"row": 1,
	"stretch": 1
},
```

## text
```
{
	"type": "text",
	"name": "objetivo",
	"default": "",
	"label": "Objetivo da perícia",
	"row": 1,
	"stretch": 1
},
```
## combo
```
{
	"type": "combo",
	"name": "marca_celular",
	"label": "Marca do celular",
	"list": "marcas",
	"editable": true,
	"row": 1,
	"stretch": 1
},
```
## image_choose

```
{
	"type": "image_chooser",
	"name": "foto_celular",
	"label": "Foto completa",
	"caption": "Celular",
	"row": 8,
	"stretch": 1
},
```

## repeat
```
{
	"type": "repeat",
	"name": "chips",
	"label": "Chips",
	"initial": 1,
	"row": 7,
	"stretch": 1,
	"items": [
		{
			"type": "combo",
			"name": "operadora",
			"label": "Operadora",
			"list": "operadoras",
			"editable": true,
			"row": 1,
			"stretch": 1
		},
		{
			"type": "edit",
			"name": "iccid",
			"label": "ICCID",
			"default": "",
			"mask": "00000000000000000000",
			"row": 1,
			"stretch": 1
		}
	]
},
```