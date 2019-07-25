# lunchScraper

Collects daily menu information from nearby restaurants and delivers it to your email every day at 11:00.

Sign up on https://web.kotek.co/lunch-scraper.

This code is created and managed by Vojtech Kotek. Suggestions for improvements are welcome.


## Changelog

### 2019-08-XX v1.5 [DEV]
- Language analysis of menus and translation to English
- Add language selection to user preference page

#### 2019-07-25 v1.4.1 [HOTFIX]
- Add verification link to verification email.

### 2019-07-25 v1.4 [MASTER]
- Email templates are now stored and rendered locally rather than on relying on email provider service.

### 2019-07-XX v1.3 
- Command Line Interface added for main admin functions.
- Subscribers and Restaurants now stored in local 'data' folder in the application rather than web app.
- Automated testing added using pytest application.
- Adapted for and integrated with Travis CI for automated integration testing.
- Application structure changed to fit with CI, testing, and best practices.

### 2019-06-11 v1.2
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
- Email verification might not actually work now, need to add button to verify email to verification template.
