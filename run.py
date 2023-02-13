from flask import Flask, request, render_template, redirect, url_for, jsonify, abort

from forms import Book
from models import library

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"


@app.route("/library/", methods=["GET", "POST"])
def library_list():
    form = Book()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit():
            library.create(form.data)
            library.save()
        return redirect(url_for("library_list"))

    return render_template("library.html", form=form, books=library.all(), error=error)

@app.route("/library/<int:book_id>/", methods=["GET", "POST"])
def book_details(book_id):
    book = library.get(book_id)
    form = Book(data=book)

    if request.method == "POST":
        if form.validate_on_submit():
            library.update(book_id, form.data)
        return redirect(url_for("library_list"))
    return render_template("book.html", form=form, book_id=book_id)

@app.route('/api/library/', methods=['GET'])
def library_list_api():
    return jsonify(library.all())

@app.route('/api/library/<int:book_id>', methods=['GET'])
def book_details_api(book_id):
    book = library.get(book_id)
    return jsonify(book)

@app.route('/api/library/<int:book_id>', methods=['PUT'])
def update_library(book_id):
    book = library.get(book_id)
    if not book:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'author' in data and not isinstance(data.get('author'), str),
        'rented' in data and not isinstance(data.get('rented'), str)
    ]):
        abort(400)
    book = {
        'csrf_token': 1,
        'title': data.get('title', book['title']),
        'author': data.get('author', book['author']),
        'rented': data.get('rented', book['rented'])
    }
    library.update(book_id, book)
    return jsonify({'book': book})

@app.route("/api/library/<int:book_id>", methods=['DELETE'])
def delete_book(book_id):
    result = library.delete(book_id)
    if not result:
        abort(404)
    return jsonify({'result': result})

@app.route("/api/library/", methods=['POST'])
def create_book():
    if not request.json or not 'title' in request.json:
        abort(400)
    book = {
        'csrf_token': 1,
        'title': request.json['title'],
        'author': request.json.get('author', ""),
        'rented': request.json.get('rented', "")
    }
    library.create(book)
    return jsonify({'book': book}), 201

if __name__ == "__main__":
    app.run(debug=True)