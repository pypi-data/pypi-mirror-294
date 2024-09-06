import click

@click.group()
def cli():
    """Ultimate Manager CLI"""
    pass

@cli.command()
def mind():
    """Manage mind-related tasks"""
    click.echo("Managing mind tasks...")

@cli.command()
def body():
    """Manage body-related tasks"""
    click.echo("Managing body tasks...")

@cli.command()
def world():
    """Manage world-related tasks"""
    click.echo("Managing world tasks...")

if __name__ == '__main__':
    cli()
