# cli.py
import click
import sys
from datetime import datetime
import dateutil.parser
import json

# Local imports
sys.path.insert(0,'..')

try:
    import lunchscraper, controller, helpers
except:
    from lunchscraper import lunchscraper, controller, helpers

@click.group()
def main():
    """
    Admin tools for the lunchScraper app.
    """
    pass

@main.command()
@click.argument('email')
@click.option('--saved', '-s', is_flag=True) # TODO: Implement getting menu from json
def test(email, saved):
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
        click.echo("{} | {} | {} | {}".format(
            user['email'].ljust(35," "),
            helpers.pretty_datetime(user['verified']).rjust(16),
            # ",".join(list(user['preferences'])),
            ".".join(user['preferences']).ljust(22),
            user['language'] if user['language'] is not None else ""
        ))



@main.command()
@click.option('--id','-i', type=int)
@click.option('--save',' /-s', is_flag=True)
def scrape(id, save):

    temp = lunchscraper.lunchScraper()
    temp.scrape_restaurants(id)
    if save:
        temp.save_menu()
        click.echo("Menu saved to file.")
        
    json_menu = json.dumps(temp.menus)

    return click.echo(json_menu)

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

@main.command()
def saved_menu():
    return click.echo(controller.Menu.get())

@main.command()
def restaurants():

    restaurants = controller.Restaurants().restaurants
    
    click.echo(restaurants)

    click.echo("There are {} restaurants.".format(len(restaurants)) )
    
    for restaurant in restaurants:
        click.echo("{} | {}".format(
            str(restaurant['id']).rjust(3," "),
            restaurant['name'].ljust(22)
        ))


if __name__ == '__main__':
    main()
