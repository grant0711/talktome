"""
Copyright (C) 2022 TalkToMe. All Rights Reserved.

Description:
    Re-usable functions for interaction with Postgres database

Author(s):
    20220529 @grant original version
"""
import logging
import os

import psycopg2
from dotenv import load_dotenv


load_dotenv()


def connect(database):
    """
    Creates and returns a psycopg2.connect object

    Inputs:
        - database: str name of database on env vars to obtain credentials
    Outputs:
        - psycopg2.connect object

    NOTE: Use with a 'with' statement as context manager
    """
    return psycopg2.connect(
        dbname = os.getenv(f'{database}_dbname'),
        user = os.getenv(f'{database}_user'),
        password = os.getenv(f'{database}_pass'),
        host = os.getenv(f'{database}_host'),
        port = os.getenv(f'{database}_port')
    )


def execute(database, sql, commit=False):
    """
    Establishes a connection with a database and executes a sql statement

    Inputs:
        - database: str name of database
        - sql: str sql command to execute
        - commit: bool commit connection, default False

    Outputs:
        - tuple cursor.fetchall() if sql statement produces a return
    """
    with connect(database) as connection:
        try:
            logging.debug(f'EXECUTING postgres.raw_query: {sql}')
            cursor = connection.cursor()
            cursor.execute(sql)

            if commit:
                connection.commit()

            return cursor.fetchall()
        except psycopg2.Error as e:
            logging.debug(f'ERROR while executing postgres.execute: {e}')
        finally:
            cursor.close()
