import flask
from flask import request, jsonify, redirect
import json
import sqlite3

DATABASE = '/path/to/database.db'
app = flask.Flask(__name__)
app.config["DEBUG"] = True


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("books.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn


@app.route('/books', methods=['GET'])
def getAll():
    conn = db_connection()
    cursor = conn.cursor()

    cursor = conn.execute("SELECT * FROM book")
    books = [
        dict(id=row[0], title=row[1], author=row[2],
             first_sentence=row[3], published=row[4])
        for row in cursor.fetchall()
    ]
    if books is not None:
        return jsonify(books)


@app.route('/addBooks', methods=['GET'])
def postBook():
    return '''<html>
   <body>
      <form action = "http://localhost:5000/addbook" method = "post">
        <p>Enter fields to create:</p>
        <p>title:<input type = "text" name = "title" /></p>
        <p>author:<input type = "text" name = "author" /></p>
        <p>first_sentence: <input type = "text" name = "first_sentence" /></p>
        <p>published: <input type = "number" name = "published" /></p>
        <p><input type = "submit" value = "submit" /></p>
      </form>   
   </body>
</html>'''


@app.route('/addbook', methods=['POST'])
def post_book():
    conn = db_connection()
    cursor = conn.cursor()

    new_author = request.form["author"]
    new_first_sentence = request.form["first_sentence"]
    new_title = request.form["title"]
    new_published = request.form['published']
    sql = """INSERT INTO book (title, author, first_sentence, published)
                 VALUES (?, ?, ?, ?)"""
    cursor.execute(sql, (new_title, new_author,
                   new_first_sentence, new_published))
    conn.commit()
    return f"Book created successfully", 201



@app.route("/book/<int:id>", methods=["GET", "PUT", "DELETE"])
def single_book(id):
    conn = db_connection()
    cursor = conn.cursor()
    book = None
    if request.method == "GET":
        cursor.execute("SELECT * FROM book WHERE id=?", (id,))
        rows = cursor.fetchall()
        for r in rows:
            book = r
        if book is not None:
            return jsonify(book), 200
        else:
            return "Something wrong", 404

    if request.method == "PUT":
        sql = """UPDATE book
                SET title=?,
                    author=?,
                    first_sentence=?,
                    published=?
                WHERE id=? """

        title = request.form['title']
        author = request.form['author']
        first_sentence = request.form['first_sentence']
        published = request.form['published']
        updated_book = {
            "id": id,
            "author": author,
            "first_sentence": first_sentence,
            "title": title,
            "published": published
        }
        conn.execute(sql, (title, author, first_sentence, published, id))
        conn.commit()
        return jsonify(updated_book)

    if request.method == "DELETE":
        sql = """ DELETE FROM book WHERE id=? """
        conn.execute(sql, (id,))
        conn.commit()
        return "The book with id: {} has been deleted.".format(id), 200



#PARTIE SANS DATABASE CETTE PARTIE A ETE FAITE INITIALEMENT MAIS A ETE AMELIOREE AVEC UN BDD SQLITE#

# @app.route('/books', methods=['GET'])

# def getAll():
#     with open('assets/book_library.json', 'r') as file:
#         books = json.load(file)
#     if 'id' in request.args:
#         id = int(request.args['id'])
#         results = []
#         for book in books['books']:
#             if book['id'] == id:
#                 results.append(book)
#         return jsonify(results)
#     else:
#         return jsonify(books)

        

 
# @app.route('/deleteBooks/<int:id>', methods=['DELETE'])
# def delete_book(id):

#     with open('assets/book_library.json', 'r') as file:
#         books = json.load(file)

  

#         for book in books["books"]:
#             if book['id'] == id:

#                 i = 0
#                 index = 0
#                 found = False
#                 while i < len(books["books"]) and found == False:
#                     if(books["books"][i]["id"] == id):
#                         index = i
#                         found = True
#                     i = i+1

#                 del books["books"][index]

#                 print(books)
#                 with open("assets/book_library.json", "w") as outfile:
#                     json.dump(books, outfile, indent=4)
#                 return '''<html>
#                             <body>
#                                 <p> YES ID </>  
#                             </body>
#                            </html>'''

#             else:
#                 text = '''<html>
#         <body>
#             <p> NO ID </>  
#         </body>
#         </html>'''

#     return text


# @app.route('/putbook', methods=['PUT'])

# def put_book():

#     id = request.form['id']
#     title = request.form['title']
#     author = request.form['author']
#     first_sentence = request.form['first_sentence']
#     published = request.form['published']
  
#     with open('assets/book_library.json', 'r') as file:
#         books = json.load(file)
  
#     if 'id' in request.form:
#         id = int(request.form['id'])
        
#         for book in books["books"]:
#             if book['id'] == id:

#                 i = 0
#                 index = 0
#                 found = False
#                 while i < len(books["books"]) and found == False:
#                     if(books["books"][i]["id"] == id):
#                         index = i
#                         found = True
#                     i = i+1

#                 books["books"][index]['title'] = title
#                 books["books"][index]['author'] = author
#                 books["books"][index]['first_sentence'] = first_sentence
#                 books["books"][index]['published'] = published

#                 with open("assets/book_library.json", "w") as outfile:
#                     json.dump(books, outfile, indent=4)
#                 return '''<html>
#                             <body>
#                                 <p> YES ID </>  
#                             </body>
#                            </html>'''

#             else:
#                 text = '''<html>
#         <body>
#             <p> NO ID </>  
#         </body>
#         </html>'''

#     return text




# @app.route('/addBooks', methods=['GET'])
# def postBook():
#     return '''<html>
#    <body>
#       <form action = "http://localhost:5000/addbook" method = "post">
#         <p>Enter fields to create:</p>
#         <p>title:<input type = "text" name = "title" /></p>
#         <p>author:<input type = "text" name = "author" /></p>
#         <p>first_sentence: <input type = "text" name = "first_sentence" /></p>
#         <p>published: <input type = "number" name = "published" /></p>
#         <p><input type = "submit" value = "submit" /></p>
#       </form>   
#    </body>
# </html>'''


# @app.route('/addbook', methods=['POST'])
# def post_book():
#     with open('assets/book_library.json', 'r') as file:
#         books = json.load(file)

#     title = request.form['title']
#     author = request.form['author']
#     first_sentence = request.form['first_sentence']
#     published = request.form['published']
#     id=0
#     for book in books['books']:
#         if book['id'] >= id:
#             id = book['id']
#     id+=1
#     data = {'id': id, 'title': title, 'first_sentence': first_sentence, 'author': author, 'published': published}
#     books["books"].append(data)
#     with open("assets/book_library.json", "w") as outfile:
#         json.dump(books, outfile, indent=4)

#     return redirect("http://www.localhost:5000/books")

app.run()
