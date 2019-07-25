# cli.py
import click
import sys

# Local imports
sys.path.insert(0,'..')

try:
    import controller
    import lunchscraper
except:
    from lunchscraper import controller, lunchscraper

@click.group()
def main():
    """
    Admin tools for the lunchScraper app.
    """
    pass

@main.command()
@click.argument('email')
def test(email):
    click.echo("Sending test email to {}".format(email))
    ls = lunchscraper.lunchScraper()
    ls.scrape_restaurants()
    result = ls.send_messages_html(email)
    if result:
        click.echo( "Email sent ({})".format(result) )
    else:
        click.echo( "Error sending email: {}".format(result) )

@main.command()
@click.argument('email')
@click.option('--verify','-v', is_flag=True)
def add(email, verify):

    result = controller.User().add(email, verify=verify)
    click.echo("Adding {} to subscribers. Forcing verification: {}. Result: {}".format(email, verify, result))

@main.command()
@click.option('--count','-c', is_flag=True)
def subscribers(count):

    users = controller.User().get()

    if count:
        count = len(users)
        click.echo("There are {} subscribers.".format(count))
    else:
        for user in users:
            click.echo("{}".format(user['email']))

@main.command()
@click.option('-i', type=int)
def scrape(i):

    ls = lunchscraper.lunchScraper()
    x = ls.scrape_restaurants()

    for r in ls.menus:
        if i and i == r['id']:
            click.echo(r)
        elif not i:
            click.echo(r)

if __name__ == '__main__':
    main()
