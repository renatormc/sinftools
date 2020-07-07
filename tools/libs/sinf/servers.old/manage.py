import os
import config
import shutil
import click


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command()
def db_revision(comment):
    os.system(f'alembic revision -m "{comment}"')


@cli.command("db_migrate")
def db_migrate():
    os.system("alembic revision --autogenerate -m \"teste\"")


@cli.command("db_upgrade")
def db_upgrade():
    os.system("alembic upgrade head")


@cli.command("db_downgrade")
def db_downgrade():
    os.system("alembic downgrade head")


@cli.command("db_init")
def db_init():
    path = config.app_dir / "alembic/versions"
    if path.exists():
        shutil.rmtree(path)
    os.mkdir(path)


if __name__ == '__main__':
    cli(obj={})
