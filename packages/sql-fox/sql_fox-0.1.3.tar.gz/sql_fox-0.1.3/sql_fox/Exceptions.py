from loguru import logger


class SQLFoxUnknownDBType(Exception):
    """When database type in db_init is incorrect"""
    def __init__(self, db_type):
        self.db_type = db_type
        logger.critical(f'Unknown {self.db_type} in db_init!')


class SQLFoxIncorrectDBInitArgs(Exception):
    """When necessary args in db_init are not found"""
    def __init__(self, incorrect_arg):
        self.incorrect_arg = incorrect_arg
        logger.critical(f'Unknown {self.incorrect_arg} in db_init!')


class SQLFoxIncorrectDBDict(Exception):
    """When database dictionary is incorrect"""
    def __init__(self):
        logger.critical('Incorrect database dictionary!')


class SQLFoxNotConnected(Exception):
    """When someone tries to create db classes without db connection"""
    def __init__(self):
        logger.critical('There is no connection to the database! Did you call "db_connect"?')


class SQLFoxRefusedToRecreateDB(Exception):
    """When user disagrees to recreate a database."""
    def __init__(self):
        logger.critical('You have refused to recreate the database.')
