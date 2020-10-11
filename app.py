import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

import pymongo

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'turtleDB'
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)


#  pymongo.MongoClient(os.getenv("MONGO_URI"))["turtleDB"]["turtle"].find() =  mongo.db.turtle.find()    another way


@app.route('/')
@app.route('/get_turtles')
def get_turtles():
    return render_template("turtles.html",
                           turtles=mongo.db.turtles.find())


@app.route('/get_captures')
def get_captures():
    return render_template("capture.html",
                           captures=mongo.db.capture_data.find())


@app.route('/add_turtle')
def add_turtle():
    return render_template('addturtle.html',
                           captures=mongo.db.capture_data.find(), morphotype=mongo.db.morphotype.find(),
                           gender=mongo.db.gender.find(), turtles=mongo.db.turtle.find())


@app.route('/insert_turtle', methods=['POST'])
def insert_turtle():
    turtles = mongo.db.turtles
    if 'picture' in request.files:
        picture = request.files['picture']
        mongo.save_file(picture.filename, picture)
        mongo.db.turtles.insert(
                           {
                               'turtle_name': request.form.get('turtle_name'),
                               'right_flipper_tag': request.form.get('right_flipper_tag'),
                               'morphotype': request.form.get('morphotype'),
                               'gender': request.form.get('gender'),
                               'picture': picture.filename
                           }
        )
    # turtles.insert_one(request.form.to_dict()) //Doesnt work with this way
    return redirect(url_for('get_turtles'))


@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)


@app.route('/add_capture')
def new_capture():
    return render_template('add_capture.html')


@app.route('/insert_capture', methods=['POST'])
def insert_capture():
    mongo.db.capture_data.insert_one(request.form.to_dict())
    return redirect(url_for('get_captures'))


@app.route('/edit_turtle/<turtle_id>')
def edit_turtle(turtle_id):
    the_turtle = mongo.db.turtles.find_one({"_id": ObjectId(turtle_id)})
    all_captures = mongo.db.capture_data.find()
    return render_template('editturtles.html', turtle=the_turtle, captures=all_captures)


@app.route('/edit_capture/<capture_id>')
def edit_capture(capture_id):
    the_capture = mongo.db.capture_data.find_one({"_id": ObjectId(capture_id)})
    all_captures = mongo.db.capture_data.find()
    return render_template('editcapture.html', captureToedit=the_capture, captures=all_captures)


@app.route('/update_turtle/<turtle_id>', methods=["POST"])
def update_turtle(turtle_id):
    turtles = mongo.db.turtles
    turtles.update({'_id': ObjectId(turtle_id)},
                   {
                       'turtle_name': request.form.get['turtle_name'],
                       'right_flipper_tag': request.form.get['right_flipper_tag'],
                       'morphotype': request.form.get['morphotype'],
                       'gender': request.form.get['gender'],
                       'picture': request.form.get['picture']
                   })
    return redirect(url_for('get_turtles'))


@app.route('/update_capture/<capture_id>', methods=["POST"])
def update_capture(capture_id):  # need to be equal to {url_for('update_capture'
    mongo.db.capture_data.update(
        {'_id': ObjectId(capture_id)},
        {'right_flipper_tag': request.form.get('right_flipper_tag')}  # request.form.get['capture_name'] is bad
    )
    return redirect(url_for('get_captures'))


@app.route('/delete_turtle/<turtle_id>')
def delete_turtle(turtle_id):
    mongo.db.turtles.remove({'_id': ObjectId(turtle_id)})
    return redirect(url_for('get_turtles'))


@app.route('/delete_capture/<capture_id>')
def delete_capture(capture_id):
    mongo.db.capture_data.remove({'_id': ObjectId(capture_id)})
    return redirect(url_for('get_captures'))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=int(os.environ.get("PORT", 5000)), debug=True)
