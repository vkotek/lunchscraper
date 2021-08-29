# mailer.py

# Take body, recipient, and send email.

from lunchscraper import settings

# Generate html email template for user with given data
email_html = self.render_email('master.html', data)


def send_email(email_html, email):

    config = {
        "from": settings.FROM,
        "to": email,
        "subject": "Daily Menu for {}".format(datetime.now().strftime("%A, %d-%b")),
        "html": email_html,
    }
    r = requests.post(self.settings.MAIL_URL, auth=auth, data=config)
    
    if r.status_code != 200:
        return False
    return True

def send_messages_html(self, email=None):

        if email:
            users = controller.User()
            user = users.get(email=email)
            if not user:
                temp_email = True
                user = users.add(email, verify=True)
            recipients = [user]
        else:
            recipients = self.get_recipients()

        auth = ("api", self.settings.MAIL_API_KEY)

        notice = controller.Email.get_notice()

        send_counter = 0

        recipients = [recipient for recipient in recipients if recipient['verified'] is not False]

        for recipient in recipients:

            try:

                print( "Sending email to {}".format(recipient['email'].ljust(40, ".") ), end="")

                # Get menus for preferences of given user
                menus = [r for r in self.menus if str(r['id']) in recipient['preferences']]

                # Define language so it corresponds to dictionary keys of languages in menu dict
                if recipient['language'] in ['cs', 'en']: # Check if language is set for user.
                    language = str('menu_' + recipient['language'])
                else: # Use original menu language
                    language = 'menu'
                for menu in menus:
                    menu['menu'] = menu[language]

                data = {
                    'title': "Daily Menu for {}".format(datetime.now().strftime("%A, %d-%b")),
                    'notice': notice,
                    'recipient': {
                        'email': recipient['email'],
                        'url': SETTINGS.URL + "/edit?token=" + recipient['token'],
                    },
                    'menus': menus,
                    'language': language,
                }

                # Generate html email template for user with given data
                email_html = self.render_email('master.html', data)

                config = {
                    "from": self.settings.FROM,
                    "to": recipient['email'],
                    "subject": "Daily Menu for {}".format(datetime.now().strftime("%A, %d-%b")),
                    "html": email_html,
                }
                r = requests.post(self.settings.MAIL_URL, auth=auth, data=config)

                if r.status_code == 200:
                    send_counter += 1
                    print("OK!")
                else:
                    print("FAILED ({})".format(str(r.status_code)))
                
                if temp_user:
                    users.remove(email=email)

            except Exception as e:
                print("ERROR: {}".format(str(e)))


        print("{} / {} Emails sent successfully.".format( send_counter, len(recipients) ) )

        return True
