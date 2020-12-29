import click

@click.group()
@click.pass_context
def cli(ctx):
    pass



@cli.command("hello-world")
@click.option('--name', '-n', default="Sem nome")
def hello_world(name):
    print(f"Olá {name}")


if __name__ == '__main__':
    cli(obj={})