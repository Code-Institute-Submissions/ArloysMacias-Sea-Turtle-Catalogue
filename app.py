import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import pymongo


app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'turtleDB'
app.config["MONGO_URI"] =os.getenv("MONGO_URI")
mongo = PyMongo(app)


#  pymongo.MongoClient(os.getenv("MONGO_URI"))["turtleDB"]["turtle"].find() =  mongo.db.turtle.find()    another way


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    data=mongo.db.turtle.find()
    return render_template("about.html", page_title="About",
                           company=data)


@app.route("/about/<member_name>")
def about_member(member_name):
    member=mongo.db.turtle.find()
    return render_template("member.html",member=member)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method =="POST":
        flash("Thanks {}, we have received your message!".format(request.form["name"]))

    return render_template("contact.html", page_title="Contact")

@app.route('/turtles')
@app.route('/get_turtles')
def get_turtles():
    return render_template("turtlesEditable.html", turtles=mongo.db.turtle.find())

if __name__== "__main__":
    app.run(host=os.environ.get("IP"), port= int(os.environ.get("PORT", 5000)),debug=True)
