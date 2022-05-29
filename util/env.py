"""
Copyright (C) 2022 TalkToMe. All Rights Reserved.

Description:
    Utility function to retrieve environmental variables from Heroku app
    and write to local .env file for development

NOTE:
    - Requires login via Heroku cli: heroku auth:login
    - Check which username you are loggin in as via heroku auth:whoami
    - Reads the heroku app name from the git remotes
    - Generates a temporary token on each subsequent run

Author(s):
    20220529 @grant original version
"""
import logging
import os
import subprocess
import re

import heroku3



def get_heroku_token():
    token = subprocess.check_output(['heroku', 'auth:token'], stderr=subprocess.DEVNULL).decode('utf-8')
    token = token.replace('\n', '')
    return token


def get_heroku_app_name():
    remotes = subprocess.check_output(['git', 'remote', '-v'], stderr=subprocess.DEVNULL).decode('utf-8')

    # strip spaces and newlines and tabs
    remotes = remotes.replace(' ', '')
    remotes = remotes.replace('\n', '')
    remotes = remotes.replace('\t', '')

    # Pattern allows for Heroku app names with alphanumeric chars and hyphens only
    pattern = r"herokuhttps://git.heroku.com/(?P<app_name>[A-Za-z0-9\-+]{,50}).git\(fetch\)"
    m = re.search(pattern, remotes)
    if m:
        app_name = m.group('app_name')
    else:
        raise Exception("Couldn't parse Heroku app name from git remotes, have you set heroku git:remote -a [app-name]?")
    return app_name


def get_heroku_app_env_vars(token, app_name):
    heroku_conn = heroku3.from_key(token)
    heroku_app = heroku_conn.app(app_name)
    env_vars = heroku_app.config().to_dict()
    return env_vars


def main():
    logging.info('Generating temporary Heroku token')
    token = get_heroku_token()

    logging.info('Parsing Heroku remote from git remotes')
    app_name = get_heroku_app_name()

    logging.info(f'Retrieving env vars from app: {app_name}')
    env_vars = get_heroku_app_env_vars(token, app_name)

    root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(root_directory + '/.env', 'w+') as outfile:

        for key in env_vars:
            if env_vars[key][0] == '{':
                outfile.write(key + '=' + '\'' + env_vars[key] + '\'' + '\n')
            elif env_vars[key][0] == '[':
                outfile.write(key + '=' + '\"' + env_vars[key] + '\"' + '\n')
            else:
                outfile.write(key + '=' + env_vars[key] + '\n')
        outfile.close()

    logging.info('Env vars retrieved from Heroku app environment successfully')

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.DEBUG)
    main()
