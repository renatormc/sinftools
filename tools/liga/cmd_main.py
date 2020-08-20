import click
import config
from cmdtool import questions
from subprocess import Popen
import os
import requests
from requests.exceptions import ConnectionError
from prettytable import PrettyTable
import shutil
from pathlib import Path
from models import *
from database import db_session
from sinf_requests import Requester
from pprint import pprint
import jwt
from sinf_requests import TokenExpiredException, TokenNoFoundException
import sys
import json
import re
from helpers.uteis import parse_ip_port


@click.group()
@click.pass_context
def cli(ctx):
    pass


# @cli.command()
# def process():
#     table = PrettyTable()
#     table.field_names = ['#', 'Nome', 'Perito',
#                          'Inicio', 'Fim', 'Servidor', 'Status']
#     i = 0
#     for name, server in config.servers.items():
#         try:
#             token_path = config.sinftools_dir / "var/sinftoken"
#             requester = Requester(token=token_path)
#             url = f"{config.servers[name]['url']}/processes"
#             response = requester.get(url)
#             processes = response.json()

#             for p in processes:
#                 table.add_row([i + 1, p['name'], p['perito'],
#                                p['start'], p['finish'], name, p['status']])
#                 i += 1
#         except ConnectionError:
#             print(f"Servidor {name} sem conexão.")
#     print(table)


@cli.command()
@click.argument('server', required=False)
def ts(server):
    try:
        token_path = config.sinftools_dir / "var/sinftoken"
        requester = Requester(token=token_path)
        if not server:
            server = questions.choose_server()
        else:
            if server == "ba":
                server = "batman"
            elif server == "sm":
                server = "superman"
            elif server == "mm":
                server = "mulher_maravilha"
        url = f"{config.servers[server]['url']}/who-is-connected"
        response = requester.get(url)
        if response.status_code == 401:
            input("Acesso não autorizado. Problema com o token.")
            return
        msg = response.content.decode("utf-8")
        if msg != 'nobody':
            res = input(f"{msg}. Deseja conectar mesmo assim? (N/s)")
            if res.lower() != "s":
                return

        try:
            url = f"{config.servers[server]['url']}/blocking-user"
            response = requester.get(url)
            if response.status_code == 401:
                input("Acesso não autorizado. Problema com o token.")
                return
            # print(response.content)
            # return
            data = response.json()
            if data['blocked']:
                msg = f"O computador está reservado para uso de {data['user']}."
                res = input(f"{msg}. Deseja conectar mesmo assim? (N/s)")
                if res.lower() != "s":
                    return
        except json.decoder.JSONDecodeError:
            pass
                
        url = f"{config.servers[server]['url']}/connection-intent"
        # who = os.getlogin()
        response = requester.post(url)

        # Generate connection file
        template = config.app_dir / "cmdtool/connection_files/template.rdp"
        rdpfile = config.app_dir / "cmdtool/connection_files/rdpfile.rdp"
        text = template.read_text(encoding="utf-16-le")
        ip, port = parse_ip_port(config.servers[server]['url'])
        text = text.replace("$server_ip", ip)
        rdpfile.write_text(text, encoding="utf-16-le")

        windir = os.getenv("windir")
        Popen(f"{windir}\\system32\\mstsc.exe \"{rdpfile}\"")
    except ConnectionError:
        print("Não foi possível se conectar ao serviço no servidor.")
    except TokenExpiredException:
        print("Token expirado. Acesse o Sinfweb no menu \"Usuário\" para um novo.")
    except TokenNoFoundException:
        print("Para maior segurança o acesso remoto aos servidores exigem um token de acesso, que não foi encontrado em sua máquina. \nAcesse o Sinfweb no menu \"Usuário\" para obter seu token de acesso.")


# @cli.command("telegram-updates")
# def telegram_updates():
#     data = telegram_api.get_updates()
#     for item in data['result']:
#         pprint(item)


# @cli.command("send-telegram")
# @click.argument("username")
# @click.argument("text")
# def send_telegram(username, text):
#     telegram_api.send_message(username, text)

 
# @cli.command("register-user")
# def register_user():
#     answers = questions.choose_user_telegram()
#     servers_com.register_user(answers['username'], answers['chat_id'])
#     print(f"Usuário {answers['username']} cadastrado.")


@cli.command("update-servers")
def update_servers():
    for name, conf in config.servers.items():
        try:
            print(
                "############################################################################################")
            print(f"Atualizando servidor {name}:\n")
            url = f"{config.servers[name]['url']}/update-sinftools"
            response = requester.get(url, timeout=None)
            print(response.content.decode("utf-8"))
        except ConnectionError:
            print(f"Servidor {name} sem conexão.")


# @cli.command("mark")
# def mark():
#     answers = questions.mark()
#     data = {
#         "type": "case",
#         "name": answers['name'],
#         "role": answers['role']
#     }
#     with Path("./.sinf_mark.json").open("w", encoding="utf-8") as f:
#         f.write(json.dumps(data, ensure_ascii=False, indent=4))


# @cli.command()
# def init():
#     answers = questions.choose_script()
#     to_script = Path(".") / f"{answers['script_name']}.bat"
#     shutil.copy(answers['script'], to_script)
#     process = Process()
#     process.script = str(to_script.absolute())
#     process.perito = answers['perito']
#     process.type = answers['process_type']
#     process.status = "ADICIONADO"
#     db_session.add(process)
#     db_session.commit()
#     print(
#         "Novo script cadastrado. Vá até o programa Fila, clique com o botão direito do mouse em cima na linha na tabela e escolha \"Editar script\", faça a edição e salve, e em seguida coloque o processo na fila.")


@cli.command("list-drives")
def list_drives():
    print("ATENÇÃO: Para listar todos os discos é necessário executar como administrador.\n")
    os.system("s-ftkimager --list-drives")

@cli.command("send-telegram")
@click.argument("username")
@click.argument("message")
def send_telegram(username, message):
    requester = Requester()
    try:
        err = requester.send_telegram(username, message)
        if err:
            print(err)
        else:
            print("Mensagem enviada")
    except ConnectionError:
        print("Não foi possível se conectar ao serviço no servidor.")
    except TokenExpiredException:
        print("Token expirado. Acesse o Sinfweb no menu \"Usuário\" para um novo.")
    except TokenNoFoundException:
        print("Para maior segurança o acesso remoto aos servidores exigem um token de acesso, que não foi encontrado em sua máquina. \nAcesse o Sinfweb no menu \"Usuário\" para obter seu token de acesso.")
# @cli.command("gen-system-token")
# def gen_system_token():
    

if __name__ == '__main__':
    cli(obj={})
