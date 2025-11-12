from flask import Flask, jsonify, request
from flask.views import MethodView
from errors import HttpError
from sqlalchemy.exc import IntegrityError
# from users import UserView
# from ads import AdView
from flask_bcrypt import Bcrypt
from models import Session, User, Ad
from validate_scheme import validate, CreateUser, PatchUser, CreateAd, PatchAd

app = Flask('ad_app')
bcrypt = Bcrypt(app)

def hash_password(password: str) -> str:
    password = password.encode()
    hashed_password = bcrypt.generate_password_hash(password)
    password = hashed_password.decode()
    return password

@app.errorhandler(HttpError)
def error_handler(err: HttpError):
    http_response = jsonify({"status": err.status_code,'message': err.message})
    http_response.status_code = err.status_code
    return http_response

@app.before_request
def before_request():
    session = Session()
    request.session = session

@app.after_request
def after_request(response):
    request.session.close()
    return response

def get_user(user_id: int) -> User:
    user = request.session.get(User, user_id)
    if user is None:
        raise HttpError(404, message='user not found')
    return user

def add_user(user: User):
    request.session.add(user)
    try:
        request.session.commit()
    except IntegrityError:
        raise HttpError(status_code=409, message='user with this login already exists')


class UserView(MethodView):
    def get(self, user_id: int):
        user = get_user(user_id)
        return jsonify(user.json)

    def post(self):
        json_data = validate(CreateUser, request.json)
        user = User(
            username=json_data['username'],
            password=hash_password(json_data['password']),
            email=json_data['email'])
        add_user(user)
        return jsonify(user.id_json)

    def patch(self, user_id: int):          # РЕДАКТИРОВАТЬ
        json_data = validate(PatchUser, request.json)
        user = get_user(user_id)
        if 'username' in json_data:
            user.username = json_data['username']
        if 'password' in json_data:
            user.username = hash_password(json_data['password'])
        add_user(user)
        return jsonify(user.id_json)


    def delete(self, user_id: int):
        user = get_user(user_id)
        request.session.delete(user)
        request.session.commit()
        return jsonify({'status': 'user delete success'})

user_view = UserView.as_view('user_view')

app.add_url_rule('/user/<int:user_id>',
                 view_func=user_view,
                 methods=['GET', 'PATCH', 'DELETE']
                 )
app.add_url_rule('/user/',
                 view_func=user_view,
                 methods=['POST']
                 )

def get_ad(ad_id: int) -> Ad:
    ad = request.session.get(Ad, ad_id)
    if ad is None:
        raise HttpError(404, message='ad not found')
    return ad

def add_ad(ad: Ad):
    request.session.add(ad)
    try:
        request.session.commit()
    except IntegrityError:
        raise HttpError(status_code=409, message='ad already exists with the same data')

class AdView(MethodView):
    def get(self, ad_id: int):
        ad = get_ad(ad_id)
        return jsonify(ad.json)

    def post(self):
        json_data = validate(CreateAd, request.json)
        ad = Ad(header=json_data['header'], description=json_data['description'], user_id=json_data['user_id'])
        add_ad(ad)
        return jsonify(ad.id_json)

    def patch(self, ad_id: int):
        json_data = validate(PatchAd, request.json)
        ad = get_ad(ad_id)
        if 'header' in json_data:
            ad.header = json_data['header']
        if 'description' in json_data:
            ad.description = json_data['description']
        add_ad(ad)
        return jsonify(ad.id_json)

    def delete(self, ad_id: int):
        ad = get_ad(ad_id)
        request.session.delete(ad)
        request.session.commit()
        return jsonify({'status': 'advertisement delete success'})

ad_view = AdView.as_view('ad_view')

app.add_url_rule('/ad/<int:ad_id>',
                 view_func=ad_view,
                 methods=['GET', 'PATCH', 'DELETE']
                 )
app.add_url_rule('/ad/',
                 view_func=ad_view,
                 methods=['POST']
                 )


def hello():
    return jsonify({
        "add-site": "Hello! REST API for ad-site is working yet!"
    })


app.add_url_rule('/',
                 view_func=hello,
                 methods=['POST', 'GET', 'PATCH', 'DELETE'])  # CRUD

if __name__ == '__main__':
    app.run()
