"""
Copyright (C) 2022 myAgro. All Rights Reserved.

Description:
    Re-usable functions for interaction with Postgres database

Author(s):
    myAgro Lib version
    20220529 @grant version for python 3.10, async support with removed pandas and sqlalchemy dependencies
"""
import os

import psycopg2
from psycopg2.extras import RealDictCursor


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
        port = os.getenv(f'{database}_port'),
        sslmode='require'
    )


def execute(logger, database, sql, commit=False):
    """
    Establishes a connection with a database and executes a sql statement

    Inputs:
        - logger: logger object
        - database: str name of database
        - sql: str sql command to execute
    Outputs:
        - list of dict objects for each row of table
    """
    with connect(database) as connection:
        try:
            logger.debug(f'EXECUTING postgres.execute: {sql}')
            cursor = connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute(sql)

            try:
                results = cursor.fetchall()
            except psycopg2.ProgrammingError as e:
                logger.debug(f'ERROR cursor.fetchall() did not return any results: {e}')
                results = []

            if commit:
                connection.commit()

            dict_result = []
            for row in results:
                dict_result.append(dict(row))

            return dict_result
        except psycopg2.Error as e:
            logger.debug(f'ERROR while executing postgres.execute: {e}')
        finally:
            cursor.close()


