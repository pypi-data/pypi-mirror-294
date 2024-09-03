import datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../sql_fox')))
from sql_fox.db_init import db_connect, db_create, db_disconnect, db_check, db_clear_all, db_init


def test_sqlite():
    db_structure = {
        'Users': {
            'id': {'data_type': 'Integer', 'primary_key': True},
            'name': {'data_type': 'String', 'nullable': False},
            'email': {'data_type': 'String', 'nullable': False, 'unique': True},
        },
        'Posts': {
            'id': {'data_type': 'Integer', 'primary_key': True, 'nullable': False, 'unique': True},
            'user_id': {'data_type': 'Integer', 'nullable': False},
            'title': {'data_type': 'String', 'nullable': False},
            'content': {'data_type': 'Text', 'nullable': True},
        }
    }
    result_classes = db_init(db_structure, 'sqlite', True, db_path='test_db.db')
    db_disconnect(True)
    assert 'users' in result_classes and 'posts' in result_classes


def test_mysql():
    db_structure = {
        'Users': {
            'id': {'data_type': 'Integer', 'primary_key': True, 'autoincrement': True},
            'name': {'data_type': 'String_100', 'nullable': False},
            'email': {'data_type': 'String_100', 'nullable': False, 'unique': True},
        },
        'Posts': {
            'id': {'data_type': 'Integer', 'primary_key': True, 'nullable': False, 'unique': True, 'index': True, 'comment': 'id!!!', 'onupdate': datetime.UTC},
            'user_id': {'data_type': 'Integer', 'nullable': False},
            'title': {'data_type': 'String_100', 'nullable': False, 'default': 'test'},
            'content': {'data_type': 'Text', 'nullable': False},
        }
    }
    result_classes = db_init(db_structure, 'mysql', True, username='russkiylis', password='1234', db_address='localhost', db_name='test')
    db_disconnect(True)
    assert 'users' in result_classes and 'posts' in result_classes
