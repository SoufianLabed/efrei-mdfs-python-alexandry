import flask
from flask import request, jsonify,redirect
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
        dict(id=row[0], title=row[1], author=row[2], first_sentence=row[3], published=row[4])
        for row in cursor.fetchall()
    ]
    if books is not None:
        return jsonify(books)

    #PARTIE SANS DATABASE#
    # with open('D:/Users/sosol/Desktop/efrei-mdfs-python-alexandry/assets/book_library.json', 'r') as file:
    #     books = json.load(file)
    # if 'id' in request.args:
    #     id = int(request.args['id'])
    #     results = []
    #     for book in books['books']:
    #         if book['id'] == id:
    #             results.append(book)
    #     return jsonify(results)
    # else:
    #     return jsonify(books)



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

    with open('D:/Users/sosol/Desktop/efrei-mdfs-python-alexandry/assets/book_library.json', 'r') as file:
        books = json.load(file)

    title = request.form['title']
    author = request.form['author']
    first_sentence = request.form['first_sentence']
    published = request.form['published']
    id=0
    for book in books['books']:
        if book['id'] >= id:
            id = book['id']
    id+=1
    data = {'id': id, 'title': title, 'first_sentence': first_sentence, 'author': author, 'published': published}
    books["books"].append(data)
    with open("D:/Users/sosol/Desktop/efrei-mdfs-python-alexandry/assets/book_library.json", "w") as outfile:
        json.dump(books, outfile, indent=4)


    return redirect("http://www.localhost:5000/books")
    

@app.route('/deleteBooks', methods=['DELETE'])

def delete_book():

    with open('D:/Users/sosol/Desktop/efrei-mdfs-python-alexandry/assets/book_library.json', 'r') as file:
        books = json.load(file)
  
    if 'id' in request.args:
        id = int(request.args['id'])
        
        for book in books["books"]:
            if book['id'] == id:

                i=0 
                index=0
                found=False
                while i<len(books["books"]) and found==False :
                    if(books["books"][i]["id"]==id):
                        index=i
                        found=True
                    i=i+1
                               
                del books["books"][index]
                
                print(books)               
                with open("D:/Users/sosol/Desktop/efrei-mdfs-python-alexandry/assets/book_library.json", "w") as outfile:
                    json.dump(books, outfile, indent=4)
                return '''<html>
                            <body>
                                <p> YES ID </>  
                            </body>
                           </html>'''
                                    
            else:
                text = '''<html>
        <body>
            <p> NO ID </>  
        </body>
        </html>'''
            
    return text


@app.route('/putbook', methods=['PUT'])

def put_book():

    id = request.form['id']
    title = request.form['title']
    author = request.form['author']
    first_sentence = request.form['first_sentence']
    published = request.form['published']
  
    with open('D:/Users/sosol/Desktop/efrei-mdfs-python-alexandry/assets/book_library.json', 'r') as file:
        books = json.load(file)
  
    if 'id' in request.form:
        id = int(request.form['id'])
        
        for book in books["books"]:
            if book['id'] == id:

                i=0 
                index=0
                found=False
                while i<len(books["books"]) and found==False :
                    if(books["books"][i]["id"]==id):
                        index=i
                        found=True
                    i=i+1
                               
                books["books"][index]['title'] = title
                books["books"][index]['author'] = author
                books["books"][index]['first_sentence'] = first_sentence
                books["books"][index]['published'] = published
                
                          
                with open("D:/Users/sosol/Desktop/efrei-mdfs-python-alexandry/assets/book_library.json", "w") as outfile:
                    json.dump(books, outfile, indent=4)
                return '''<html>
                            <body>
                                <p> YES ID </>  
                            </body>
                           </html>'''
                                    
            else:
                text = '''<html>
        <body>
            <p> NO ID </>  
        </body>
        </html>'''
            
    return text


    

app.run()
