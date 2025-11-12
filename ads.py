# from typing import Type
#
# from flask import jsonify, request
# from flask.views import MethodView
# from sqlalchemy.exc import IntegrityError
#
# from models import Session, Ad
# from validate_scheme import CreateAd, PatchAd, validate
# from errors import HttpError
# from server import before_request
#
# # def validate(json_data: dict,
# #              model_class: Type[CreateAd] | Type[PatchAd]):
# #     try:
# #         model_item = model_class(**json_data)
# #         return model_item.model_dump(exclude_none=True)
# #     except ValidationError as err:
# #         print(request.json)
# #         raise HttpError(400, err.errors())
#
# request_session = before_request()

# def get_ad(ad_id: int) -> Ad:
#     ad = request_session.get(Ad, ad_id)
#     if ad is None:
#         raise HttpError(404, message='ad not found')
#     return ad
#
# def add_ad(ad: Ad):
#     request_session.add(ad)
#     try:
#         request_session.commit()
#     except IntegrityError:
#         raise HttpError(status_code=409, message='ad already exists with the same data')
#
# class AdView(MethodView):
#     def get(self, ad_id: int):
#         ad = get_ad(ad_id)
#         return jsonify(ad.json)
#         # # НАЙТИ
#         # with Session() as session:
#         #     ad = get_ad(ad_id, session)
#         #     return jsonify({
#         #         "id": ad.id,
#         #         "header": ad.header,
#         #         "description": ad.description,
#         #         "creation_time": ad.creation_time.isoformat(),
#         #         "user_id": ad.user_id
#         #     })
#
#     def post(self):
#         json_data = validate(CreateAd, request.json)
#         ad = Ad(header=json_data['header'], description=json_data['password'], user_id=['user_id'])
#         add_ad(ad)
#         return jsonify(ad.id_json)
#
#         # with Session() as session:
#         #     new_ad = Ad(**json_data)
#         #     session.add(new_ad)
#         #     try:
#         #         session.commit()
#         #     except IntegrityError as err:
#         #         raise HttpError(
#         #             409,
#         #             f'ad already exists with the same data   {err}'
#         #         )
#         #     return jsonify({
#         #         "status": "advertisement add success",
#         #         "id": new_ad.id
#         #     })
#
#     def patch(self, ad_id: int):
#         json_data = validate(PatchAd, request.json)
#         ad = get_ad(ad_id)
#         if 'header' in json_data:
#             ad.header = json_data['header']
#         if 'description' in json_data:
#             ad.description = json_data['description']
#         add_ad(ad)
#         return jsonify(ad.id_json)
#
#         # with Session() as session:
#         #     ad = get_ad(ad_id, session)
#         #     for field, value in json_data.items():
#         #         setattr(ad, field, value)
#         #     try:
#         #         session.commit()
#         #     except IntegrityError as err:
#         #         raise HttpError(409, 'username is busy')
#         #
#         #     return jsonify({
#         #         "status": "advertisement patch success",
#         #         "id": ad.id
#         #     })
#
#     def delete(self, ad_id: int):
#         ad = get_ad(ad_id)
#         request_session.delete(ad)
#         request_session.commit()
#         return jsonify({'status': 'advertisement delete success'})
#         # УДАЛИТЬ
#         # with Session() as session:
#         #     ad = get_ad(ad_id, session)
#         #     session.delete(ad)
#         #     session.commit()
#         #     return jsonify({
#         #         "id": ad.id,
#         #         "header": ad.header,
#         #         "creation_time": ad.creation_time.isoformat(),
#         #         "user_id": ad.user_id
#         #     })
