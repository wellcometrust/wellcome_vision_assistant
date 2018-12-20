import os

GITHUB_OAUTH_TOKEN = os.environ['GITHUB_OAUTH_TOKEN']
GITHUB_USER = os.environ['GITHUB_USER']
GITHUB_REPO = os.environ['GITHUB_REPO']

ISSUES_URL = f'https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/issues'


SLACK_ADD_REMINDERS_ENDPOINT = 'https://slack.com/api/reminders.add'
SLACK_OAUTH_TOKEN = os.environ['OAUTH_TOKEN']
