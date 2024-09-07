import click
from ezy_cli.ezy_cli import cnt, crd, crf, lfd, prg


@click.group()
@click.version_option("1.0.0")
def cli():
    pass


cli.add_command(lfd)
cli.add_command(crd)
cli.add_command(crf)
cli.add_command(cnt)
cli.add_command(prg)


if __name__ == "__main__":
    cli()
