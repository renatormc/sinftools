import click
import config
import questions
from subprocess import Popen
import os
import requests
from requests.exceptions import ConnectionError
from prettytable import PrettyTable


@click.group()
@click.pass_context
def cli(ctx):
    pass

@cli.command()
def process():
    table = PrettyTable()
    table.field_names = ['#','Nome','Perito', 'Inicio', 'Fim', 'Servidor', 'Status']
    i = 0
    for name, server in config.servers.items():
        try:
            url = f"{config.servers[name]['url']}/processes"
            response = requests.get(url)
            processes = response.json()
        
            for p in processes:
                table.add_row([i+1, p['name'], p['perito'], p['start'], p['finish'], name, p['status']])
                i += 1
        except ConnectionError:
            print(f"Servidor {name} sem conexão.")
    print(table)
            
@cli.command()
def ts():
  
    server = questions.choose_server()
    try:
        url = f"{config.servers[server]['url']}/someone-connected"
        response = requests.get(url)
    except ConnectionError:
        print("Não foi possível se conectar ao serviço no servidor.")
        return
    msg = response.content.decode("utf-8")
    if msg != 'no':
        res = input(f"{msg}. Deseja conectar mesmo assim? (N/s)")
        if res.lower() != "s":
            return
    windir = os.getenv("windir")

    try:
        url = f"{config.servers[server]['url']}/who-connected"
        who = os.getlogin()
        response = requests.post(url,json={"name": who})
        connection_file = str(config.servers[server]['connection_file'])
        Popen(f"{windir}\\system32\\mstsc.exe \"{connection_file}\"")
    except ConnectionError:
        print("Não foi possível se conectar ao serviço no servidor.")
        return

   
   


if __name__ == '__main__':
    cli(obj={})
