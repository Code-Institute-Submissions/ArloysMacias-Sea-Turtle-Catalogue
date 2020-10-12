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
def index():
    return render_template('index.html', turtles=mongo.db.turtle.find())


                                        ##### TURTLES #######

@app.route('/get_turtles')
def get_turtles():
    return render_template("turtles.html",
                           turtles=mongo.db.turtles.find())


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
                'picture': picture.filename,
                'capture_location':request.form.get('capture_location')
            }
        )
    # turtles.insert_one(request.form.to_dict()) //Doesnt work with this way
    return redirect(url_for('get_turtles'))


@app.route('/edit_turtle/<turtle_id>')
def edit_turtle(turtle_id):
    the_turtle = mongo.db.turtles.find_one({"_id": ObjectId(turtle_id)})
    all_captures = mongo.db.capture_data.find()
    return render_template('editturtles.html', turtle=the_turtle, captures=all_captures, gender=mongo.db.gender.find(),
                           morphotype=mongo.db.morphotype.find())


@app.route('/update_turtle/<turtle_id>', methods=["POST"])
def update_turtle(turtle_id):
    turtles = mongo.db.turtles
    if 'picture' in request.files:
        picture = request.files['picture']
        mongo.save_file(picture.filename, picture)
        turtles.update({'_id': ObjectId(turtle_id)},
                       {
                           'turtle_name': request.form.get('turtle_name'),
                           'right_flipper_tag': request.form.get('right_flipper_tag'),
                           'morphotype': request.form.get('morphotype'),
                           'gender': request.form.get('gender'),
                           'picture': picture.filename,
                           'capture_location':request.form.get('capture_location')
                       })
    return redirect(url_for('get_turtles'))


@app.route('/delete_turtle/<turtle_id>')
def delete_turtle(turtle_id):
    mongo.db.turtles.remove({'_id': ObjectId(turtle_id)})
    return redirect(url_for('get_turtles'))


                                    ##### CAPTURE ########

@app.route('/get_captures')
def get_captures():
    return render_template("captures.html",
                           captures=mongo.db.capture_data.find())


@app.route('/add_capture/<route>')
def new_capture(route):
    return render_template('add_capture.html', source= route)


@app.route('/insert_capture/<source>', methods=['POST'])
def insert_capture(source):
    mongo.db.capture_data.insert_one(request.form.to_dict())
    # mongo.db.capture_data.insert(
    #     {
    #         'capture_location': request.form.get('capture_location'),
    #         'weather': request.form.get('weather'),
    #         'ocean_temperature': request.form.get('ocean_temperature'),
    #         'date': request.form.get('date')
    #         # 'monitoring_total_time': request.form.get('monitoring_total_time')
    #     }
    # )
    if source =='from_addTurtle':
        return redirect(url_for('add_turtle'))

    return redirect(url_for('get_captures'))



@app.route('/edit_capture/<capture_id>')
def edit_capture(capture_id):
    the_capture = mongo.db.capture_data.find_one({"_id": ObjectId(capture_id)})
    all_captures = mongo.db.capture_data.find()
    return render_template('editcapture.html', captureToedit=the_capture, captures=all_captures)


@app.route('/update_capture/<capture_id>', methods=["POST"])
def update_capture(capture_id):  # need to be equal to {url_for('update_capture'
    mongo.db.capture_data.update({'_id': ObjectId(capture_id)},
                                 {
                                     'capture_location': request.form.get('capture_location'),
                                     'weather': request.form.get('weather'),
                                     'ocean_temperature': request.form.get('ocean_temperature'),
                                     'date': request.form.get('date')
                                 })
    return redirect(url_for('get_captures'))


@app.route('/delete_capture/<capture_id>')
def delete_capture(capture_id):
    mongo.db.capture_data.remove({'_id': ObjectId(capture_id)})
    return redirect(url_for('get_captures'))


                                        ###### PICTURE ########

@app.route('/file/<file_name>')
def load_image(file_name):
    return mongo.send_file(file_name)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=int(os.environ.get("PORT", 5000)), debug=True)
