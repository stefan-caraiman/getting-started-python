# Copyright 2019 Google LLC
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

Every stored element contains a dictionary of data, and has a unique
identifier, that is not stored as data. However, we add that identifier to
the returned data when fetched, as it is used by the main program to
create URL paths.
"""

COLLECTION = "books"

from google.cloud import firestore


def get_collection():
    client = firestore.Client()
    return client.collection(COLLECTION)


def list(limit=10, cursor=None):
    books = get_collection()

    query = books.order_by("title").limit(limit)
    if cursor is not None:
        # cursor is the document id of the last book displayed
        doc_snapshot = books.document(cursor).get()
        if doc_snapshot.to_dict() is not None:
            query = query.start_after(doc_snapshot)

    results = []
    for doc in query.stream():
        result = doc.to_dict()  # Includes data, but not ID
        result["id"] = doc.id   # Templates need unique ID, too
        results.append(result)

    next_cursor = None
    if len(results) >= limit:
        next_cursor = results[-1]["id"]

    return results, next_cursor


def list_by_user(limit=10, cursor=None, user_id=None):
    if user_id is None:
        return [], None

    books = get_collection()

    query = books.where('createdById', '==', user_id)
    query = query.order_by("title").limit(limit)
    if cursor is not None:
        # cursor is the document id of the last book displayed
        doc_snapshot = books.document(cursor).get()
        if doc_snapshot.to_dict() is not None:
            query = query.start_after(doc_snapshot)

    results = []
    for doc in query.stream():
        result = doc.to_dict()  # Includes data, but not ID
        result["id"] = doc.id   # Templates need unique ID, too
        results.append(result)

    next_cursor = None
    if len(results) >= limit:
        next_cursor = results[-1]["id"]

    return results, next_cursor


def read(id):
    books = get_collection()
    result = books.document(id).get().to_dict()
    result["id"] = id
    return result


def update(data, id):
    books = get_collection()
    doc = books.document(id)

    doc.update(data)
    result = doc.get().to_dict()
    result["id"] = id
    return result


def create(data):
    books = get_collection()
    update_time, doc_ref = books.add(data)
    result = doc_ref.get().to_dict()
    result["id"] = doc_ref.id
    return result


def delete(id):
    books = get_collection()
    doc = books.document(id)
    doc.delete()
