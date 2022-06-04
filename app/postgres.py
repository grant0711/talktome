"""
Copyright (C) 2022 myAgro. All Rights Reserved.

Description:
    Re-usable functions for interaction with Postgres database

Author(s):
    @20220604 grant simplified version with removed pandas and sqlalchemy dependencies
"""
import os

import psycopg2
from psycopg2.extras import RealDictCursor


def execute(logger, sql, commit=False):
    """
    Establishes a connection with a database and executes a sql statement

    Inputs:
        - logger: logger object
        - database: str name of database
        - sql: str sql command to execute
    Outputs:
        - list of dict objects for each row of table
    """
    with psycopg2.connect(os.environ['DATABASE_URL']) as connection:
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
