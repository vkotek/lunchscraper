# cli.py
import click

@click.group()
def main():
    """
    Admin tools for lunchScraper app.
    """
    pass

@main.command()
@click.argument('email')
def test(email):
   click.echo("Sending test email to {}".format(email))

@main.command()
@click.argument('email')
@click.option('--verify','-v', is_flag=True)
def add(email, verify):
    click.echo("Adding {} to subscribers. Forcing verification: {}.".format(email, verify))

@main.command()
@click.option('--count','-c', is_flag=True)
def subscribers(count):
    if count:
        click.echo("There are XX subscribers.")
    else:
        click.echo("List all subscribers")

if __name__ == '__main__':
    main()
