# HackerOne-Notifier

A Pushover-compatible fork of https://github.com/VincentDS/HackerOne-Notifier

HackerOne-Notifier is a simple application which sends out a notification to your favorite device whenever a new program is available on HackerOne. Notifications are send out using Pushover. Currently the application supports the following functions: 

- Initial notification when the app launches. 
- Change the interval rate on which the app checks for new programs.

## Installation and Use

1. Clone the repository.
2. Create a new config file `config.py` similar to `config-example.py` with the preferred settings.
3. Define your Pushover user token and user key in hackerone-notify.py.
4. Install the requirements: `pip install -r requirements.txt`.
