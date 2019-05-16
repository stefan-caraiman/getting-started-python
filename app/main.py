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

from flask import Flask, redirect, render_template, request, url_for

from bookshelf import model, storage


app = Flask(__name__)


# [START upload_image_file]
def upload_image_file(file):
    """
    Upload the user-uploaded file to Google Cloud Storage and retrieve its
    publicly-accessible URL.
    """
    if not file:
        return None

    public_url = storage.upload_file(
        file.read(),
        file.filename,
        file.content_type
    )

    app.logger.info(
        "Uploaded file %s as %s.", file.filename, public_url)

    return public_url
# [END upload_image_file]


@app.route("/")
def list():
    token = request.args.get('page_token', None)
    #if token:
    #    token = token.encode('utf-8')

    books, next_page_token = model.list(cursor=token)

    return render_template(
        "list.html",
        books=books,
        next_page_token=next_page_token)


@app.route('/book/<id>')
def view(id):
    book = model.read(id)
    return render_template("view.html", book=book)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template("form.html", action="Add", book={})

    else:  # It's POST
        data = request.form.to_dict(flat=True)

        # If an image was uploaded, update the data to point to the new image.
        # [START image_url]
        image_url = upload_image_file(request.files.get('image'))
        # [END image_url]

        # [START image_url2]
        if image_url:
            data['imageUrl'] = image_url
        # [END image_url2]

        book = model.create(data)

        return redirect(url_for('view', id=book["id"]))


@app.route('/book/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    book = model.read(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        image_url = upload_image_file(request.files.get('image'))

        if image_url:
            data['imageUrl'] = image_url

        book = model.update(data, id)

        return redirect(url_for('view', id=book["id"]))

    return render_template("form.html", action="Edit", book=book)


@app.route('/book/<id>/delete')
def delete(id):
    model.delete(id)
    return redirect(url_for('list'))


# This is only used when running locally. When running live, gunicorn runs
# the application.
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
