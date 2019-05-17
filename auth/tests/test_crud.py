# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
import pytest

from bookshelf import model


def test_list(app):
    for i in range(1, 12):
        model.create({'title': u'Book {0}'.format(i)})

    with app.test_client() as c:
        rv = c.get('/')

    assert rv.status == '200 OK'

    body = rv.data.decode('utf-8')
    assert 'Book 1' in body, "Should show books"
    assert len(re.findall('<h4>Book', body)) <= 10, (
        "Should not show more than 10 books")
    assert 'More' in body, "Should have more than one page"


def test_add(app):
    data = {
        'title': 'Test Book',
        'author': 'Test Author',
        'publishedDate': 'Test Date Published',
        'description': 'Test Description'
    }

    with app.test_client() as c:
        rv = c.post('/books/add', data=data, follow_redirects=True)

    assert rv.status == '200 OK'
    body = rv.data.decode('utf-8')
    assert 'Test Book' in body
    assert 'Test Author' in body
    assert 'Test Date Published' in body
    assert 'Test Description' in body

def test_edit(app):
    existing = model.create({'title': "Temp Title"})

    with app.test_client() as c:
        rv = c.post(
            '/books/%s/edit' % existing['id'],
            data={'title': 'Updated Title'},
            follow_redirects=True)

    assert rv.status == '200 OK'
    body = rv.data.decode('utf-8')
    assert 'Updated Title' in body
    assert 'Temp Title' not in body

def test_delete(app):
    existing = model.create({'title': "Temp Title"})

    with app.test_client() as c:
        rv = c.get(
            '/books/%s/delete' % existing['id'],
            follow_redirects=True)

    assert rv.status == '200 OK'
    assert not model.read(existing['id'])
