import os,json

import requests
from flask import Flask, render_template, flash, redirect, url_for, session, request,jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, apology

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        input = request.form.get("search")
        if input:
            info = db.execute("SELECT * FROM books WHERE LOWER(isbn) LIKE :book OR title LIKE :book OR author LIKE :book",
                              {"book": '%'+input+'%'}).fetchall()
            #print(info)
            if info:
                return render_template("searched.html", info=info)
            else:
                flash('Sorry, There is no such a book or author')
                return redirect('/')

        else:
            flash('Please type title,isbn number or author name')
            return redirect('/')


    else:
        return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        pwd = request.form.get("pwd")
        email=request.form.get("email")
        if db.execute("SELECT email FROM users WHERE email = :email", {"email": email}).rowcount == 0:
        # insert data into tab

            db.execute("INSERT INTO users(username,hash,email) VALUES(:username,:hash,:email)", {"username":username,
                       "hash":generate_password_hash(pwd),"email":email})
            db.commit()

            flash('Successfull')

            rows = db.execute("SELECT user_id FROM users WHERE username = :username",
                              {"username": request.form.get("username")}).fetchone()

            # Remember which user has logged in
            session["user_id"] = rows[0]

            # Redirect user to home page
            return redirect("/")


    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Query database for username
        rows = db.execute("SELECT hash FROM users WHERE username = :username",
                          {"username":request.form.get("username")}).fetchone()

        if rows == None:
            flash('No such user name')
            return render_template("login.html")

        if not check_password_hash(rows[0], request.form.get("pwd")):
            flash('invalid username or password')
            return render_template("login.html")


        user = db.execute("SELECT user_id FROM users WHERE username = :username",
                          {"username": request.form.get("username")}).fetchone()
        # Remember which user has logged in
        session["user_id"] = user[0]
        flash('success')

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():

    # remove session_id
    session.clear()
    return redirect("/")

@app.route("/<book>",methods=["GET", "POST"])
@login_required
def default(book):


    row = db.execute("SELECT isbn FROM books WHERE isbn LIKE :input OR title LIKE :input OR author LIKE :input",
                  {"input": '%' + book + '%'})

    isbn = row.fetchone()
    isbn = isbn[0]

    if request.method == "POST":
        # Save current user info
        currentUser = session["user_id"]

        # Fetch form data
        rating = request.form.get("rating")
        comment = request.form.get("comment")

        # Search book_id by ISBN
        row = db.execute("SELECT id FROM books WHERE isbn = :isbn",
                         {"isbn": book})

        # Save id into variable
        bookId = row.fetchone()  # (id,)
        bookId = bookId[0]

        # Check for user submission (ONLY 1 review/user allowed per book)
        if db.execute("SELECT * FROM ratings WHERE user_id = :user_id AND :book_id = :book_id",
                          {"user_id": currentUser,
                           "book_id": bookId}).rowcount != 0:
            flash('You cannot rate this book again!')
            return redirect("/" + book)


        rating = int(rating)

        db.execute("INSERT INTO ratings (user_id, rating, comments, book_id) VALUES (:user_id,:rating, :comments, :book_id)",
                   {"user_id": currentUser,
                    "book_id": bookId,
                    "comments": comment,
                    "rating": rating})

        # Commit transactions to DB and close the connection
        db.commit()

        flash("rating is saved, thank you!")
        return redirect("/" + book)

    else:
         # Search book_id by ISBN
        row = db.execute("SELECT id FROM books WHERE isbn = :isbn",
                        {"isbn": isbn})

        # Save id into variable
        bok = row.fetchone() # (id,)
        bok = bok[0]
        infos = db.execute("SELECT * FROM books WHERE LOWER(isbn) LIKE :input OR title LIKE :input OR author LIKE :input",
                           {"input": '%' + book + '%'}).fetchall()
        key = os.getenv("GOODREADS_KEY")
        # get the books info about avg rating and rewiew count
        res = requests.get("https://www.goodreads.com/book/review_counts.json",
                           params={"key": key, "isbns": isbn})
        data = res.json()
        review = data['books'][0]['average_rating']
        review_count = data['books'][0]['work_ratings_count']
        user_review =db.execute("SELECT AVG(rating) FROM ratings \
                                WHERE book_id=:book_id",{"book_id" :bok}).fetchall()
        user_review= "{:.2f}".format(user_review[0][0])


        return render_template("book.html", infos=infos, review=review, review_count=review_count,isbn=isbn,user_review=user_review)

@app.route("/contact")
def contact():
    return render_template("contact.html")