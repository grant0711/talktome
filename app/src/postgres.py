"""
Copyright (C) 2022 myAgro. All Rights Reserved.

Description:
    Re-usable functions for interaction with Postgres database

Author(s):
    @myagro-lib version
    @20220604 grant simplified version with removed pandas and sqlalchemy dependencies
"""
import os
import json
from types import NoneType

import psycopg2
from psycopg2.extras import RealDictCursor


def convert_to_str(input):
    """
    FIXME this is a temporary work-around function to convert different python datatypes
    to the properly formatted string version

    To be replaced with proper psycopg2 datatype handling down the line
    """
    if type(input) == int:
        return str(input)
    elif type(input) == dict:
        return "'" + json.dumps(input) + "'"
    elif type(input) == str:
        return "'" + input + "'"
    elif type(input) == bool:
        return 'TRUE' if input else 'FALSE'
    elif type(input) == NoneType:
        return 'NULL'
    raise Exception(f'Input datatype : {type(input)} not handled')


def execute(logger, sql, commit=False):
    """
    Establishes a connection with a database and executes a sql statement

    Inputs:
        - logger: logger object
        - sql: str sql command to execute
        - commit: bool set to True to commit after executing query
    Outputs:
        - dict or list of dict objects for each row of table, keys are column names
          values are returning values within column for row

    NOTE:
        - returns dict if only single row returns from query
        - returns list of dict if multiple rows return from query
        - returns empty list if no rows returned from query
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

            if len(dict_result) == 1:
                return dict_result[0]

            return dict_result
        except psycopg2.Error as e:
            logger.debug(f'ERROR while executing postgres.execute: {e}')
        finally:
            cursor.close()
