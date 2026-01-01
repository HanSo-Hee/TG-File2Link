# (c) @AvishkarPatil | @EverythingSuckz

import os
from os import environ, getenv
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

class Var(object):
    API_ID = int(getenv('API_ID'))
    API_HASH = str(getenv('API_HASH'))
    BOT_TOKEN = str(getenv('BOT_TOKEN'))
    SESSION_NAME = str(getenv('SESSION_NAME', 'FileStreamBot'))
    SLEEP_THRESHOLD = int(getenv('SLEEP_THRESHOLD', '60'))
    WORKERS = int(getenv('WORKERS', '4'))
    BIN_CHANNEL = int(getenv('BIN_CHANNEL'))
    PORT = int(os.environ.get("PORT", 8080))
    BIND_ADRESS = str(getenv('WEB_SERVER_BIND_ADDRESS', '0.0.0.0'))
    OWNER_ID = int(getenv('OWNER_ID', '1287407305'))
    NO_PORT = str(getenv('NO_PORT', 'False')).lower() in ('1', 'true', 'yes', 'on')

    APP_NAME = str(getenv('APP_NAME', '')).strip() or None
    ON_HEROKU = 'DYNO' in environ

    render_host = getenv('RENDER_EXTERNAL_HOSTNAME')
    render_url = getenv('RENDER_EXTERNAL_URL')
    custom_fqdn = getenv('FQDN')

    if custom_fqdn:
        FQDN = custom_fqdn
    elif render_host:
        FQDN = render_host
    elif render_url:
        FQDN = urlparse(render_url).netloc
    elif ON_HEROKU and APP_NAME:
        FQDN = f"{APP_NAME}.herokuapp.com"
    elif APP_NAME:
        FQDN = f"{APP_NAME}.onrender.com"
    else:
        FQDN = BIND_ADRESS

    URL = "https://{}/".format(FQDN) if NO_PORT or ON_HEROKU else "http://{}:{}/".format(FQDN, PORT)
    DATABASE_URL = str(getenv('DATABASE_URL'))
    PING_INTERVAL = int(getenv('PING_INTERVAL', '500'))
    UPDATES_CHANNEL = str(getenv('UPDATES_CHANNEL', None))
    BANNED_CHANNELS = list(set(int(x) for x in str(getenv("BANNED_CHANNELS", "-1001296894100")).split()))
