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
def subscribers():

    users = controller.User().get()

    click.echo("There are {} subscribers.".format(len(users)) )
    for user in users:
        click.echo("{}|{}|{}".format(
            user['email'].ljust(35," "),
            user['verified'],
            list(user['preferences'])
        ))



@main.command()
@click.option('-id','-i', type=int)
def scrape(id):

    temp = lunchscraper.lunchScraper()
    temp.scrape_restaurants(id)

    return click.echo(temp.menus)

@main.command()
@click.argument('id', type=int)
def new_preference(id):
    """Assigns a preference to all users."""

    users = controller.User()

    try:
        users.add_restaurant_to_preferences(id)
        return True
    except:
        return False

@main.command()
@click.argument('email')
def verify(email):

    users = controller.User()

    try:
        user = users.get(email=email)
        if not user:
            return click.echo("User not found.")
        click.echo("User found. Verifying user {} ({})".format(user['email'], user['uuid']))
        result = users.verify(user['token'])
        if result:
            return click.echo("User verified.")
        else:
            click.echo("Could not verify user.")
    except Exception as e:
        return "Unexpected error:", click.echo(e)

@main.command()
@click.argument('email')
def resend_verification(email):

    users = controller.User()

    user = users.get(email=email)

    if not user:
        return click.echo("User not found.")

    if users.send_email_verification( user['uuid'] ):
        return click.echo("Verification email sent to {}.".format(user['email']))

    return click.echo("Could not resend verification email.")

if __name__ == '__main__':
    main()
