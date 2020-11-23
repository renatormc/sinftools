import win32com.client as win32
import pythoncom
from pathlib import Path
import time

class DocPrinter(object):
    def __init__(self, printers) -> None:
        self.printers = printers

    def __enter__(self):
        pythoncom.CoInitialize()
        print("Abrindo Word")
        self.word = win32.Dispatch('Word.Application')
        self.word.Visible = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Fechando Word")
        self.word.Quit()
    

    def print_doc(self, doc: Path, n_copies: int, duplex: bool, save_pdf: bool = False):
        import time
        doc = self.word.Documents.Open(str(doc.absolute()), ReadOnly=True)
        if n_copies > 0:
            self.word.ActivePrinter = self.printers['duplex'] if duplex else self.printers['simple']
            for i in range(n_copies):
                doc.PrintOut(Copies=1)
                time.sleep(0.5)
        if save_pdf:
            path = Path(doc.FullName).with_suffix(".pdf")
            doc.SaveAs2(FileName=str(path), FileFormat=17)
        doc.Close()