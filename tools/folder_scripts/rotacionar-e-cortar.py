## [Inicio]
import sys
from PIL import Image
import os

os.chdir(r'F:\Laudos\Trabalhando\329.20210.2015\extracoes\Contatos')
angle = 90
retangulo = (649,1153,1849,2577)

## [Testar rotacionar]
img = Image.open("teste.jpg")
img = img.rotate(angle,resample=Image.BICUBIC, expand=True)
img.save("teste2.jpg")

## [Testar cortar]
img = Image.open("teste2.jpg")
img = img.crop(retangulo)
img.save("teste2.jpg")

## [Rotacionar todas]
for file in os.listdir():
    img = Image.open(file)
    img = img.rotate(angle,resample=Image.BICUBIC, expand=True)
    img.save(file)
    
## [Cortar todas]
for file in os.listdir():
    img = Image.open(file)
    img = img.crop(retangulo)
    img.save(file)
