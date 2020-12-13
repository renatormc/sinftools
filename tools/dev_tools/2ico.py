from PIL import Image
import sys
from pathlib import Path

filename = sys.argv[1]
img = Image.open(filename)
img.save(str(Path(filename).with_suffix(".ico")))