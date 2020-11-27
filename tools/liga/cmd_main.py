import click
import config
from cmdtool import questions
from subprocess import Popen
import os
from requests.exceptions import ConnectionError
from models import *
from sinf_requests import Requester
from sinf_requests import TokenExpiredException, TokenNoFoundException
import json
from helpers.uteis import parse_ip_port
import sys

@click.group()
@click.pass_context
def cli(ctx):
    pass


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
            else:
                print(f"Servidor {server} não existe. Digite ba, sm ou mm.")
                sys.exit(1)
        
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


if __name__ == '__main__':
    cli(obj={})
