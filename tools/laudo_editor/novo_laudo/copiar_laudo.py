import os
import sys
import shutil
sinftools_dir = os.getenv("SINFTOOLS")

shutil.copyfile(f'{sinftools_dir}\\tools\\laudo_editor\\laudo_rapido2\\Styles.docx', "laudo.docx")
