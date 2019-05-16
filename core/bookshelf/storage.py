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


import os
import os.path
from uuid import uuid4

from flask import current_app
from google.cloud import storage


SAFE_EXTENSIONS = set([".png", ".gif", ".jpg", ".jpeg"])


def _parsed_filename(filename):
    head, tail = os.path.split(filename)
    name, ext = os.path.splitext(tail)
    return name, ext


# [START upload_file]
def upload_file(contents, filename, content_type):
    """
    Uploads a file to a given Cloud Storage bucket and returns the public url
    to the new object. The Cloud Storage blob will be given a unique
    is raised and nothing is stored.
    """
    name, extension = _parsed_filename(filename)
    if extension not in SAFE_EXTENSIONS:
        raise TypeError("File extension {} not allowed.".format(extension))

    client = storage.Client()
    bucket = client.bucket(os.environ["CLOUD_STORAGE_BUCKET"])
    blob = bucket.blob(str(uuid4()))

    blob.content_disposition = "inline;filename={}{}".format(name, extension)
    blob.upload_from_string(
        contents,
        content_type=content_type)

    url = blob.public_url
    return url
# [END upload_file]
