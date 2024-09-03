__all__ = ["session_autoopen_close_decorator", "add", "get", "delete", "update"]

from sql_fox.imports import *
import sql_fox.settings as settings


def session_autoopen_close_decorator(func):
    """This decorator automatically open and closes a session.

        Use it with functions which do something with a database. The function should take db(session) as last argument.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if settings.__db_connected:
            db = settings.__session
            function = func(db, *args, **kwargs)
            db.close()
            return function
        else:
            raise SQLFoxNotConnected

    return wrapper


@session_autoopen_close_decorator
def add(db, row):
    """
    Use it to add a row into your database.

    :param db: Ignore. It is used by decorator.
    :param row: A class filled with data. For example, if you have table 'users', db_init will provide you with 'users' class.
    :return:
    """
    db.add(row)
    db.commit()
    db.refresh(row)


@session_autoopen_close_decorator
def get(db, row_class, filters: dict = None, skip: int = 0, limit: int = 1):
    """
    An easy way to get information from your database.

    :param db: Ignore. It is used by decorator.
    :param row_class: Class of your table.
    :param filters: Dict of filters. if complex, {'email': {'like', 'russkiylis%'}}, if not, {'email': 'russkiylis@koshy.ru'}
    :param skip: If you need a lot of rows, but you need to skip n rows from beginning.
    :param limit: If you need n rows.
    :return: A list of rows or one row, don't touch skip and limit for one row.
    """
    query = db.query(row_class)
    conditions = []
    if filters:
        for key, condition in filters.items():
            column = getattr(row_class, key)
            if isinstance(condition, dict):
                for operator, value in condition.items():
                    if operator == "==":
                        conditions.append(column == value)
                    elif operator == "!=":
                        conditions.append(column != value)
                    elif operator == ">":
                        conditions.append(column > value)
                    elif operator == "<":
                        conditions.append(column < value)
                    elif operator == ">=":
                        conditions.append(column >= value)
                    elif operator == "<=":
                        conditions.append(column <= value)
                    elif operator == "like":
                        conditions.append(column.like(value))
                    elif operator == "in":
                        conditions.append(column.in_(value))
            else:
                conditions.append(column == condition)

            if conditions:
                query = query.filter(and_(*conditions))

    if skip == 0 and limit == 1:
        return query.first()
    else:
        return query.skip(skip).limit(limit).all()


@session_autoopen_close_decorator
def delete(db, row_class, filters: dict = None, skip: int = 0, limit: int = 1) -> int:
    """
    An easy way to delete information from your database.

    :param db: Ignore. It is used by decorator.
    :param row_class: Class of your table.
    :param filters: Dict of filters. if complex, {'email': {'like', 'russkiylis%'}}, if not, {'email': 'russkiylis@koshy.ru'}
    :param skip: If you need a lot of rows, but you need to skip n rows from beginning.
    :param limit: If you need n rows.
    :return: Number of deleted rows.
    """
    query = db.query(row_class)
    count = 0
    conditions = []

    if filters:
        for key, condition in filters.items():
            column = getattr(row_class, key)
            if isinstance(condition, dict):
                for operator, value in condition.items():
                    if operator == "==":
                        conditions.append(column == value)
                    elif operator == "!=":
                        conditions.append(column != value)
                    elif operator == ">":
                        conditions.append(column > value)
                    elif operator == "<":
                        conditions.append(column < value)
                    elif operator == ">=":
                        conditions.append(column >= value)
                    elif operator == "<=":
                        conditions.append(column <= value)
                    elif operator == "like":
                        conditions.append(column.like(value))
                    elif operator == "in":
                        conditions.append(column.in_(value))
            else:
                conditions.append(column == condition)

            if conditions:
                query = query.filter(and_(*conditions))

    if query:
        for instance in query.all():
            count += 1
            db.delete(instance)

    db.commit()
    return count


@session_autoopen_close_decorator
def update(db, row, filters: dict):
    """
    An easy way to update information in your database.

    :param db: Ignore. It is used by decorator.
    :param row: A class filled with data. For example, if you have table 'users', db_init will provide you with 'users' class.
    :param filters: Dict of filters. if complex, {'email': {'like', 'russkiylis%'}}, if not, {'email': 'russkiylis@koshy.ru'}
    :return: Number of updated rows.
    """
    query = db.query(row.__class__)
    count = 0
    conditions = []

    if filters:
        for key, condition in filters.items():
            column = getattr(row.__class__, key)
            if isinstance(condition, dict):
                for operator, value in condition.items():
                    if operator == "==":
                        conditions.append(column == value)
                    elif operator == "!=":
                        conditions.append(column != value)
                    elif operator == ">":
                        conditions.append(column > value)
                    elif operator == "<":
                        conditions.append(column < value)
                    elif operator == ">=":
                        conditions.append(column >= value)
                    elif operator == "<=":
                        conditions.append(column <= value)
                    elif operator == "like":
                        conditions.append(column.like(value))
                    elif operator == "in":
                        conditions.append(column.in_(value))
            else:
                conditions.append(column == condition)

            if conditions:
                query = query.filter(and_(*conditions))

    found_instances = query.all()
    count = 0
    for instance in found_instances:
        for attr in row.__mapper__.column_attrs:
            key = attr.key
            new_value = getattr(row, key)
            if new_value is not None:
                setattr(instance, key, new_value)
        db.add(instance)
        count += 1

    if count > 0:
        db.commit()

    return count
