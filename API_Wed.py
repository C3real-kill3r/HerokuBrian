from flask import *
import datetime
from functools import wraps
import jwt
app = Flask(__name__)

app.config['SECRET_KEY'] = 'brybzlee'
dict1 = {}
store =[]

@app.route ('/',methods=['GET'])
def home():
    return jsonify({'meassage' : 'welcome home techies'})

@app.route ('/register',methods=['POST','GET'])
def register():
    name=request.get_json()["name"]
    username=request.get_json()["username"]
    email=request.get_json()["email"]
    password=request.get_json()["password"]
    dict1.update({username:{"name":name,"email":email,"password":password}})
    return jsonify({'meassage' : 'you are succesfully registered'})

def loginauth(username, password):
    if username in dict1:
        if password == dict1[username]["password"]:
            return True
    return False

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') 

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 403

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated



@app.route('/login',methods=['POST'])
def log_in():
    username=request.get_json()["username"]
    password=request.get_json()["password"]
    if loginauth(username, password):
        token = jwt.encode({'username' : username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'message' : 'Login successful', 'token' : token.decode('UTF-8')})
    else:
        return jsonify({'meassage' : 'you are not succesfully logged in'})

@app.route ('/comments_post',methods=['POST','GET'])
@token_required
def comments_post():
    comment=request.get_json()["comment"]
    store.append(comment)
    return jsonify({'meassage' : 'comments posted'})

@app.route ('/get_comments', methods=['GET'])
@token_required
def get_comments():
    #comment=request.get_json()["comment"]
    if len(store)>0:
        return jsonify(store)
    else:
        return jsonify({'meassage' : 'no comments available'})

    

@app.route ('/delete_comments', methods=['DELETE'])
@token_required
def delete_comments():
    del store[:]
    return jsonify({'meassage' : 'comments deleted'})

@app.route ('/get_users', methods=['GET'])
@token_required
def get_users():
    return jsonify(dict1)

if __name__== '__main__':
    app.run(debug=True)