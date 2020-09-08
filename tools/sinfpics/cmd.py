import click
import qrcode
import os


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command("hello-world")
def hello_world():
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )


    qr.add_data('Some data')
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save("test.png")
    os.system("powershell -c test.png")


if __name__ == '__main__':
    cli(obj={})
