# from hashlib import md5

# def hash_password(password: str) -> str:
#     # преобразуем в байты
#     password: bytes = password.encode()
#     # байты положили в md5, привели к строке
#     hashed_password = md5(password).hexdigest()
#     return hashed_password

# import server
# from flask_bcrypt import Bcrypt
#
# bcrypt = Bcrypt(server.app)
#
# def hash_password(password: str) -> str:
#     password = password.encode()
#     hashed_password = bcrypt.generate_password_hash(password)
#     password = hashed_password.decode()
#     return password