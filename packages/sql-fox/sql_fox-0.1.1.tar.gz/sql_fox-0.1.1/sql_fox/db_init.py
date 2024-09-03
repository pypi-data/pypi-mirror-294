__all__ = ["db_connect", "db_disconnect", "data_type_mapping", "db_create", "db_check", "db_clear_all", "db_init"]

from sql_fox.imports import *
import sql_fox.settings as settings

global __engine, __session, __metadata


def db_connect(db_type: str = 'SQLite', silent: bool = True, **kwargs: str):
    """
    Use it to simply connect to your database.
    :param db_type: (str) Defines a database type. It can be 'sqlite', 'mysql'
    :param silent: silence in console?
    :param kwargs: (str) Use it to connect to your database. SQLite - db_path,
                                                             MySQL/MariaDB - username, password, db_address, db_name
    :return: session, engine, metadata: You can return session, engine and metadata if needed.
    """

    if not silent:
        logger.info('Connecting to database...')

    global __engine, __session, __metadata

    # Here we check if everything is correct in db_init args
    if db_type.lower() == 'sqlite':

        if 'db_path' in kwargs:
            db_path = kwargs['db_path']
        else:
            raise SQLFoxIncorrectDBInitArgs('db_path')

        __engine = create_engine(f'sqlite:///{db_path}', echo=True if not silent else False)
    elif db_type.lower() == 'mysql':

        if 'username' in kwargs:
            username = kwargs['username']
        else:
            raise SQLFoxIncorrectDBInitArgs('username')

        if 'password' in kwargs:
            password = kwargs['password']
        else:
            raise SQLFoxIncorrectDBInitArgs('password')

        if 'db_address' in kwargs:
            db_address = kwargs['db_address']
        else:
            raise SQLFoxIncorrectDBInitArgs('db_address')

        if 'db_name' in kwargs:
            db_name = kwargs['db_name']
        else:
            raise SQLFoxIncorrectDBInitArgs('db_name')

        __engine = create_engine(f'mysql+pymysql://{username}:{password}@{db_address}/{db_name}', echo=True if not silent else False)
    else:
        raise SQLFoxUnknownDBType(db_type)

    __engine.connect()
    __metadata = MetaData()
    __session = scoped_session(sessionmaker(bind=__engine))
    settings.__session = __session

    if not silent:
        logger.success('Seems like everything is good in your connection args. You are cool!')

    settings.__db_connected = True
    return __session, __engine, __metadata


def db_disconnect(silent: bool = True):
    """
    Use it if you need to totally disconnect from database.
    :param silent: silence in console?
    :return:
    """
    global __engine, __metadata, __session
    if not silent:
        logger.info('Disconnecting from database...')

    __engine.dispose()
    __session = None
    __metadata = None
    settings.__db_connected = False


def data_type_mapping():
    """Here we automatically create mapping for all sqlalchemy data types."""
    data_types_mapping = {}
    for name, obj in inspect.getmembers(types):
        if inspect.isclass(obj) and issubclass(obj, types.TypeEngine):
            data_types_mapping[name] = obj
    return data_types_mapping


def db_create(db_structure: dict, silent: bool = True) -> dict:
    """
    Use it to simply create your database tables and columns with all necessary flags. (if it doesn't exist.) It returns table classes dict.

    Your db_structure should look like:
        {
            'table_name': {
                'column_1': {'data_type': 'data_type', 'flag_name(nullable for example): True'},
                'column_2': {...}},
            'another_table': {...}}

    If you need to use, for example, String(10) in MySQL, write this as String_10.
    You can find information about data types and flags `here. <https://docs.sqlalchemy.org>`__

    BigInteger
    Boolean
    Date
    DateTime
    Double
    Float
    Integer
    SmallInteger
    String
    Text

    primary_key: Marks the column as part of the primary key for the table.
    nullable: Specifies whether the column can contain NULL values.
    unique: Ensures that all values in the column are unique across the table.
    index: Creates an index on the column to improve query performance.
    default: Sets a default value for the column if no value is provided.
    server_default: Defines a default value at the database level, often using an SQL expression.
    autoincrement: Indicates that the column's value should automatically increment, typically used with primary keys.
    comment: Adds a comment or description to the column.
    onupdate: Defines a value or function that is applied to the column whenever the row is updated.

    :param db_structure: a structure of your database.
    :param silent: silence in console?
    :return: All table classes stored in one dictionary. Their keys are similar to table_names but no capitalized.
    """

    if not silent:
        logger.info("Creating a database...")

    if not settings.__db_connected:
        raise SQLFoxNotConnected

    table_classes = {}  # Here we will store all generated table classes

    base = declarative_base()

    data_types_mapping = data_type_mapping()

    try:
        for table_name, columns in db_structure.items():  # Here we create table_attrs which we usually write manually when creating sqlalchemy table class.

            table_name = table_name.lower()

            if not silent:
                logger.info(f"Creating table '{table_name}'...")

            table_attrs = {'__tablename__': table_name}

            for column_name, column_attrs in columns.items():

                column_name = column_name.lower()

                if not silent:
                    logger.info(f"Creating column '{column_name}' with {column_attrs}...")

                data_type_split = column_attrs['data_type'].split('_')
                if len(data_type_split) > 1:
                    # noinspection PyArgumentList
                    column_data_type = data_types_mapping[data_type_split[0]](int(data_type_split[1]))
                else:
                    column_data_type = data_types_mapping[data_type_split[0]]

                flags = {key: value
                         for key, value in column_attrs.items() if key != 'type'}

                table_attrs[column_name] = Column(column_data_type, **flags)  # Table attrs ready to be used in table class creation.

            table_classes[table_name] = type(table_name, (base,), table_attrs)  # Here we create a table class.

        base.metadata.create_all(__engine)  # Here we create a database structure.

        if not silent:
            logger.success(f"Successfully created a database structure!")

    except Exception:
        raise SQLFoxIncorrectDBDict

    return table_classes


def db_check(db_structure: dict, silent: bool = True) -> bool:
    """
    Use it to check your database tables and columns.

    Your db_structure should look like:
    {
        'table_name': {
            'column_1': {'data_type': 'data_type', 'flag_name(nullable for example): True'},
            'column_2': {...}},
        'another_table': {...}}

    If you need to use, for example, String(10) in MySQL, write this as String_10.
    You can find information about data types and flags `here. <https://docs.sqlalchemy.org>`__

    BigInteger
    Boolean
    Date
    DateTime
    Double
    Float
    Integer
    SmallInteger
    String
    Text

    primary_key: Marks the column as part of the primary key for the table.
    nullable: Specifies whether the column can contain NULL values.
    unique: Ensures that all values in the column are unique across the table.
    index: Creates an index on the column to improve query performance.
    default: Sets a default value for the column if no value is provided.
    server_default: Defines a default value at the database level, often using an SQL expression.
    autoincrement: Indicates that the column's value should automatically increment, typically used with primary keys.
    comment: Adds a comment or description to the column.
    onupdate: Defines a value or function that is applied to the column whenever the row is updated.

    :param db_structure: a structure of your database.
    :param silent: silence in console?
    :return: True if database matches db_structure, False if it does not.
    """

    if not silent:
        logger.info("Checking database structure...")

    if not settings.__db_connected:
        raise SQLFoxNotConnected

    # data_types_mapping = data_type_mapping()

    inspector = Inspector.from_engine(__engine)  # Creating inspector

    existing_tables = inspector.get_table_names()
    for table_name, columns in db_structure.items():
        table_name = table_name.lower()
        if table_name not in existing_tables:  # if we don't have a table, db_check will return False
            if not silent:
                logger.error(f"Mismatch! No '{table_name}'.")
            return False

        existing_columns = {column['name']: column for column in inspector.get_columns(table_name)}
        for column_name, column_attrs in columns.items():
            column_name = column_name.lower()
            if column_name not in existing_columns:  # if we don't have a column, db_check will return False
                if not silent:
                    logger.error(f"Mismatch! No '{column_name}' in '{table_name}'.")
                return False
    return True
    # todo I also need to check data_type and flags. Unfortunately I don't know how to do it, also i don't have much time.


def db_clear_all(silent: bool = True):
    """
    PURGES EVERYTHING IN YOUR DATABASE (Everything which was created via SQLAlchemy)
    :param silent: silence in console?
    :return: None
    """
    global __metadata, __engine

    if not settings.__db_connected:
        raise SQLFoxNotConnected

    if not silent:
        logger.warning("Deleting all tables in the database...")

    __metadata.reflect(bind=__engine)

    __metadata.drop_all(bind=__engine, checkfirst=False)

    __metadata.reflect(bind=__engine)

    if not silent:
        logger.success("All generated tables have been successfully deleted")


def db_init(db_structure: dict, db_type: str = 'SQLite', silent: bool = True, **kwargs) -> dict:
    """
    This function is usually the only function you want to use if you want to initialize your database.
    It contains other initializing functions such as db_connect, db_check, db_clear_all and db_create.
    It also returns db_classes just as db_create.

    This function automatically checks the database and recreates it so the database is 100% similar to db_structure.

    Your db_structure should look like:
    {
        'table_name': {
            'column_1': {'data_type': 'data_type', 'flag_name(nullable for example): True'},
            'column_2': {...}},
        'another_table': {...}}

    If you need to use, for example, String(10) in MySQL, write this as String_10.
    You can find information about data types and flags `here. <https://docs.sqlalchemy.org>`__

    BigInteger
    Boolean
    Date
    DateTime
    Double
    Float
    Integer
    SmallInteger
    String
    Text

    primary_key: Marks the column as part of the primary key for the table.
    nullable: Specifies whether the column can contain NULL values.
    unique: Ensures that all values in the column are unique across the table.
    index: Creates an index on the column to improve query performance.
    default: Sets a default value for the column if no value is provided.
    server_default: Defines a default value at the database level, often using an SQL expression.
    autoincrement: Indicates that the column's value should automatically increment, typically used with primary keys.
    comment: Adds a comment or description to the column.
    onupdate: Defines a value or function that is applied to the column whenever the row is updated.

    :param db_structure: a structure of your database.
    :param db_type: (str) Defines a database type. It can be 'sqlite', 'mysql'
    :param silent: silence in console?
    :param kwargs: (str) Use it to connect to your database. SQLite - db_path,
                                                             MySQL/MariaDB - username, password, db_address, db_name
    :return: All table classes stored in one dictionary. Their keys are similar to table_names but not capitalized.
    """

    db_connect(db_type, silent, **kwargs)  # Connecting to db

    if not db_check(db_structure, silent):  # Checking db
        if not silent:
            if input('Database has been corrupted! Should it be destroyed to be recreated? y/n') == 'y' or 'Y':
                db_clear_all(silent)
            else:
                raise SQLFoxRefusedToRecreateDB

        db_clear_all(silent)

    db_classes = db_create(db_structure, silent)  # (re)Creating classes only
    return db_classes
