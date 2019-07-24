# lunchScraper

Collects daily menu information from nearby restaurants and delivers it to your email every day at 11:00.

Sign up on https://web.kotek.co/lunch-scraper.

This code is created and managed by Vojtech Kotek. Suggestions for improvements are welcome.


## Changelog

### 2019-07-XX v1.3 [DEV]
- Command Line Interface added for main admin functions. [WIP]
- Subscribers and Restaurants now stored in local 'data' folder in the application rather than web app.
- Automated testing added using pytest application.
- Adapted for and integrated with Travis CI for automated integration testing.
- Application structure changed to fit with CI, testing, and best practices.

### 2019-06-11 v1.2 [MASTER]
- Email is now sent iteratively to each user, allowing for personalized experience.
- Added preference management page and link to email footer

### 2019-06-10 v1.1
- Self sign-up with email verification on web.kotek.co/subscription
- Subscribers are now managed in an external JSON file, path is specified in settings.py.
- Backend preparations for preference management
- Added Lavande restaurant

### 2019-06-03 v1.0
- lunchScraper is launched to the public.
- Added Potrefena Husa - Na Verandach on request


## Notes
- When running for the first time, one must create an empty subscribers.json file otherwise app fails. >> Fix this in code so that it autocreats the file.
- CLI is only a placeholder for now, needs to be finished.
- Tests are only preliminary, more need to be added.
- The Dev branch is pending merge into Master, but the subscibers.json location has changed and needs to also be updated in the front-end, which works with its own file.
