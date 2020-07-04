import os
import getpass
import click

@click.group()
@click.pass_context
def cli(ctx):
    pass

@cli.command()
def clear_password():
    os.system("setx PROXYPWD \"\"")


@cli.command()
def set_password():
    user = input("user: ")
    password = getpass.getpass()
    os.system(f"setx PROXYPWD {user}:{password}")


@cli.command()
@click.option('--local/--general', default=False)
def set_proxy(local):
    user_password = os.getenv("PROXYPWD")
    if user_password:
        if local:
            os.system(f"set HTTP_PROXY=http://{user_password}@webgateway.ssp.go.gov.br:8080")
            os.system(f"set HTTPS_PROXY=http://{user_password}@webgateway.ssp.go.gov.br:8080")
        else:
            os.system(f"setx HTTP_PROXY http://{user_password}@webgateway.ssp.go.gov.br:8080")
            os.system(f"setx HTTPS_PROXY http://{user_password}@webgateway.ssp.go.gov.br:8080")

@cli.command()
@click.option('--local/--general', default=True)
def clear_proxy(local):
    os.system("setx HTTP_PROXY \"\"")
    os.system("setx HTTPS_PROXY \"\"")
    os.system("set HTTP_PROXY=")
    os.system("set HTTPS_PROXY=")

cli(obj={})