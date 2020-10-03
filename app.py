from flask import Flask

from flask_pymongo import PyMongo

#This library is used to convert bson into Json
from bson.json_util import dumps

#This library will be to generate random string that will be our id for our records
from bson.objectid import ObjectId

#The justify  help to convert bson into json  and request will help to made a request to the server
from flask import jsonify,request

#generate_password library will be helpful to generating the hashes of the password 
# and check password library  will be checking the password hash whenever we are comparing the two hashes. 
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__) #Initializing our Flask App..

app.secret_key = "secretkey"

app.config['MONGO_URI'] = "mongodb://localhost:27017/Users" #Mongo db db path for connecting with mongodb
mongo = PyMongo(app)

#Creating a Add Route for POST REQUEST..........................................
@app.route('/add', methods=['POST'])
def add_user():
    _json = request.json #Convert all the json here and storing it to _json variable
    _name = _json['name'] #user name
    _email = _json['email'] #user email
    _password = _json['pwd'] #user password

    #Now for validation..
    if _name and _email and _password and request.method == 'POST':
        _hashed_password = generate_password_hash(_password)

        #for saving our details into our database
        id = mongo.db.user.insert({'name':_name,'email':_email,'pwd':_hashed_password})#For inserting the details and generating an id..
        resp = jsonify("User Has been Successfully Added!!")
        resp.status_code = 200
        return resp

    else:
        return not_found()
#...............................................................


#Creating a users route for GET REQUEST................
@app.route('/users')
def users():
    users = mongo.db.user.find()#For finding the users
    resp = dumps(users)
    return resp
#.........................................................

#creating an another users of id type for GET REQUEST..............
#This route will retuen the specific details of the users with specific id..
@app.route('/user/<id>')
def user(id):
    user = mongo.db.user.find_one({'_id':ObjectId(id)})#For finding the users with id
    resp = dumps(user)
    return resp
#...................................................................

#creating a delete route for deleting a users record with its specific id for DELETE REQUEST........
@app.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    mongo.db.user.delete_one({'_id':ObjectId(id)})
    resp = jsonify("This Users Record has been Deleted Sucessfully!!!")
    resp.status_code = 200
    return resp
#..............................................................................

#creating a update route for updating any secific user eith its Id for PUT REQUEST..................
@app.route('/update/<id>', methods=['PUT'])
def update(id):
    _id = id
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['pwd']

    if _name and _email and _password and _id and request.method == 'PUT':
        _hashed_password = generate_password_hash(_password)#This will convert our password into hash..
        mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'name':_name,'email':_email,'pwd':_hashed_password}})
        resp = jsonify("Hey User Updated Successfully!!!")
        resp.status_code = 200
        return resp
    else:
        return not_found()
#..........................................................................

#This function is for handling the error............
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found' + request.url
    }
    resp = jsonify(message) #convert the message into json message
    resp.status_code = 404
    return resp
#.................................................

if __name__ == "__main__":
    app.run(debug=True)   #This will auto start our app if we make any changes in it

