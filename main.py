"""


"""
import logging
from logging.config import dictConfig

from fastapi import FastAPI
from dotenv import load_dotenv

from log_config import log_config

dictConfig(log_config)
logger = logging.getLogger('development')


load_dotenv()


app = FastAPI()


@app.get("/ping")
async def ping():
    logger.debug(f'Ping request: Logs are operational; log level {logger.level}')
    return {"message": "Server is up and running"}


@app.post("/incoming_message")
async def incoming_message(body):
    logger.debug(f'Incoming message: {body}')


@app.get("/privacy_policy")
async def privacy_policy():
    logger.debug('Privacy policy page accessed')
    return "FIXME This is a privacy policy. We won't sell your data to 3rd parties."
    