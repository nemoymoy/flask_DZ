# from typing import Type
#
# from flask import jsonify, request
# from flask.views import MethodView
# from sqlalchemy.exc import IntegrityError
#
# from models import User
# from validate_scheme import CreateUser, PatchUser, validate
# from security import hash_password
# from errors import HttpError
# from server import before_request
#
# # def validate(json_data: dict,
# #              model_class: Type[CreateUser] | Type[PatchUser]):
# #     try:
# #         model_item = model_class(**json_data)
# #         return model_item.model_dump(exclude_none=True) # чтобы не было None
# #     except ValidationError as err:
# #         # будет список ошибок, полей от библ. pydantic с подробным описанием
# #         raise HttpError(400, err.errors())
#
# # def get_user_by_id(user_id: int):
# #     user = request.session.get(User, user_id)
# #     if user is None:
# #         raise HttpError(404, 'user not found')
# #     return user
#
#
# request_session = before_request()
#
# def get_user(user_id: int) -> User:
#     user = request_session.get(User, user_id)
#     if user is None:
#         raise HttpError(404, message='user not found')
#     return user
#
# def add_user(user: User):
#     request_session.add(user)
#     try:
#         request_session.commit()
#     except IntegrityError:
#         raise HttpError(status_code=409, message='user with this login already exists')
#
#
# class UserView(MethodView):
#     def get(self, user_id: int):
#         user = get_user(user_id)
#         return jsonify(user.json)
#         # НАЙТИ
#         # with Session() as session:
#         #     user = get_user(user_id, session)
#         #     return jsonify({
#         #         "id": user.id,
#         #         "username": user.username,
#         #         "creation_time": user.creation_time.isoformat()
#         #     })
#
#     def post(self):
#         json_data = validate(CreateUser, request.json)
#         user = User(username=json_data['username'], password=hash_password(json_data['password']))
#         add_user(user)
#         return jsonify(user.id_json)
#         # # извлекаем пароль (строку) для хэширования:
#         # pwd: str = json_data["password"]
#         # # кладем хэш (строку) обратно в json:
#         # json_data["password"] = hash_password(pwd)
#
#         # with Session() as session:
#         #     # используем символы распаковки json:
#         #     new_user = User(**json_data)
#         #     session.add(new_user)
#         #     try:
#         #         session.commit()
#         #     except IntegrityError as err:
#         #         raise HttpError(
#         #             409,
#         #             f'user already exists with the same username   {err}'
#         #         )
#         #     return jsonify({
#         #         "status": "user add success",
#         #         "id": new_user.id
#         #     })
#
#     def patch(self, user_id: int):          # РЕДАКТИРОВАТЬ
#         json_data = validate(PatchUser, request.json)
#         user = get_user(user_id)
#         if 'username' in json_data:
#             user.username = json_data['username']
#         if 'password' in json_data:
#             user.username = hash_password(json_data['password'])
#         add_user(user)
#         return jsonify(user.id_json)
#         #
#         # # если пароль пришел, то хэшируем его:
#         # if 'password' in json_data:
#         #     json_data["password"] = hash_password(json_data["password"])
#         #
#         # with Session() as session:
#         #     user = get_user(user_id, session)
#         #     for field, value in json_data.items():
#         #         setattr(user, field, value)
#         #     try:
#         #         session.commit()
#         #     except IntegrityError as err:
#         #         raise HttpError(409, 'username is busy')
#         #
#         #     return jsonify({
#         #         "status": "user patch success",
#         #         "id": user.id
#         #     })
#
#     def delete(self, user_id: int):
#         user = get_user(user_id)
#         request_session.delete(user)
#         request_session.commit()
#         return jsonify({'status': 'user delete success'})
#
#         # # УДАЛИТЬ
#         # with Session() as session:
#         #     user = get_user(user_id, session)
#         #     session.delete(user)
#         #     session.commit()
#         #     # можно в модель добавить метод
#         #     # подготовки нужного словарика для ответа
#         #     return jsonify({
#         #         "status": "user delete success",
#         #         "id": user.id,
#         #         "username": user.username,
#         #         "creation_time": user.creation_time.isoformat()
#         #         # прошло секунд
#         #         # "creation_time": int(user.creation_time.timestamp())
#         #     })
