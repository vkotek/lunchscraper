# lunchScraper

Collects daily menu information from nearby restaurants and delivers it to your email every day at 11:00.

Sign up on https://web.kotek.co/lunch-scraper.
Or view the menu directly at https://web.kotek.co/lunch-scraper/menu

This code is created and managed by Vojtech Kotek. Suggestions for improvements are welcome.

## Minimal Customizable View (JIRA Friendly)
You can customize the direct menu view and make it embed-friendly.
- Root URL: https://web.kotek.co/lunch-scraper/menu
- ?compact=1 (makes view more compact, removes header/footer and margins)
- ?id=1,3,2 (id of the restaurants to show, in desired order)
- ?language={en,cs} (displays only the desired language to save space)

Example: https://web.kotek.co/lunch-scraper/menu?compact=1&language=en&id=11,1,15


## Changelog

### 2019-10-XX v2.0 [IN PROGRESS]
- Allow subscribers to define the order of menus on the preference page.

### 2019-10-21 v1.5.2 [MASTER]
- Added Facebook page scraping!

### 2019-10-21 v1.5.1
- When a menu cannot be retrieved, the restaurant still appears in the email with a message.
- Added Selenium and headless Chrome to support scraping of JavaScript rendered websites.

### 2019-08-XX v1.5
- Language translation of menus to English
- Add language selection to user preference page

### 2019-07-25 v1.4
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
- When running for the first time, one must create an empty subscribers.json file otherwise app fails. >> Fix this in code so that it auto-creates the file.
