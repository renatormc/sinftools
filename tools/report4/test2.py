from pathlib import Path
import os

f = Path("C:/temp/teste.txt")

p1, ext = os.path.splitext(f)
f2 = Path(f"{p1}_2{ext}")
print(f2)


 def generate_name(self):
        return f"{uuid4()}{self.thumb_extension}"