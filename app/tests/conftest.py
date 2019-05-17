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

"""conftest.py is used to define common test fixtures for pytest."""

from flask import Flask
import pytest

#from bookshelf import model


@pytest.fixture()
def app():
    app = Flask(__name__)
    app.testing = True
    with app.test_request_context():
#        collection = model.COLLECTION
#        model.COLLECTION = 'test'
        yield app
#        model.COLLECTION = collection
