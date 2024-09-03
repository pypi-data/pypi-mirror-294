import sys
import os
import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../sql_fox')))
from db_init import db_connect, db_create, db_disconnect, db_check, db_clear_all, db_init
from core import add, get, delete, update

db_structure = {
    'Users': {
        'id': {'data_type': 'Integer', 'primary_key': True, 'autoincrement': True},
        'name': {'data_type': 'String_100', 'nullable': False},
        'email': {'data_type': 'String_100', 'nullable': False, 'unique': True},
    },
    'Posts': {
        'id': {'data_type': 'Integer', 'primary_key': True, 'nullable': False, 'unique': True, 'index': True,
               'comment': 'id!!!'},
        'user_id': {'data_type': 'Integer', 'nullable': False},
        'title': {'data_type': 'String_100', 'nullable': False, 'default': 'test'},
        'content': {'data_type': 'Text', 'nullable': False},
    }
}


def test_crud():

    result_classes = db_init(db_structure, 'mysql', True, username='russkiylis', password='1234',
                             db_address='localhost', db_name='test')
    users = result_classes['users']
    posts = result_classes['posts']

    user = users(id=1488, name='тест', email='test@test.ru')
    post = posts(id=1488, user_id=1337, title='тест', content='russkiylis!')

    add(post)
    add(user)

    assert get(users, {'id': 1488}).email == 'test@test.ru'
    assert get(posts, {'user_id': {'>=': 1335}}).title == 'тест'

    delete(users)
    delete(posts, {'id': 1488})

    new_post = posts(title='ураа!', content='еееее')
    update(new_post, {'user_id': 1})
