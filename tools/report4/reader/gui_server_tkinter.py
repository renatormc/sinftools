from tkinter import *
from tkinter import messagebox
import socket
from waitress import serve
from app import app
import threading
from pathlib import Path
import os
import multiprocessing

script_dir = Path(os.path.dirname(os.path.realpath(__file__)))

def get_available_port():
    port = 5000
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        if result == 0:
            port += 1
            continue
        return port

def run(port):
    serve(app, host='0.0.0.0', port=port)

thread = None

class ThreadedTask(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port

    def run(self):
        serve(app, host='0.0.0.0', port=self.port)

port = get_available_port()

url = f"http://localhost:{port}"


def task():
    global thread
    t1 = multiprocessing.Process(target=run,args=(port,))
    t1.start()
    thread = ThreadedTask(port)
    thread.start()

def on_closing():
    global thread
    thread.quit()
    # if messagebox.askokcancel("Quit", "Do you want to quit?"):
    #     root.destroy()

root = Tk()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.title("Simple Prog")
root.after_idle(task)

# w = Label(root, text="Red", bg="red", fg="white")
# w.pack(fill=X)
message = f"Para vizualizar os dados abra o navegador\nMozilla Firefox no endereço abaixo:\n\n {url} \n\n Mantenha essa janela aberta."
text = Text(root, height=7)
text.config(font=('helvetica', 20))
text.insert(INSERT, message)
text.pack(fill=X)
btn = Button(text="Copiar endereço")
btn.config(bg='dark green', fg='white')
btn.config(font=('helvetica', 20, 'underline italic'))
btn.pack(fill=X)
# w = Label(root, text="Green", bg="green", fg="black")
# w.pack(fill=X)
# w = Label(root, text="Blue", bg="blue", fg="white")
# w.pack(fill=X)

root.geometry("600x300") #You want the size of the app to be 500x500
root.iconbitmap(script_dir / 'icon.ico')
root.resizable(0, 0) #D


mainloop()