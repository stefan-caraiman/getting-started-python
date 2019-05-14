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


"""
model.py - Handles interacting with the actual data storage. This uses Cloud
Firestore with a collection called 'books'.
"""


from flask import current_app
from google.cloud import firestore


def init_app(app):
    pass


def get_collection():
    client = firestore.Client(current_app.config['PROJECT_ID'])
    return client.collection("books")


def list(limit=10, cursor=None):
    books = get_collection()

    query = books.order_by("title").limit(limit)
    if cursor is not None:
        # cursor is the document id of the last book displayed
        doc_snapshot = books.document(cursor).get()
        if doc_snapshot.to_dict() is not None:
            query = query.start_after(cursor)

    docs = [doc for doc in query.stream()]
    results = [doc.to_dict() for doc in docs]

    next_cursor = None
    if len(docs) > 0:
        next_cursor = docs[-1].id

    return results, next_cursor


def read(id):
    books = get_collection()
    result = books.document(key).get().to_dict()
    return result


def update(data, id):
    books = get_collection()
    doc = books.document(id).get()

    doc.update(data)
    return doc.to_dict()


def create(data):
    books = get_collection()
    doc = books.add(data)
    return doc.to_dict()


def delete(id):
    books = get_collection()
    doc = books.document(id)
    doc.delete()
