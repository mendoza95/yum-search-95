from google.appengine.ext import ndb
from hashlib import sha256
from base64 import b64encode
from os import urandom
import uuid

class Users(ndb.Model):
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    confirmation_code = ndb.StringProperty(required=True)
    confirmed_email = ndb.BooleanProperty(default=False)

    @classmethod
    def check_if_exists(cls, email):
        return cls.query(cls.email == email).get()

    @classmethod
    def add_new_user(cls, name, email, password):
        user = cls.check_if_exists(email)

        if not user:
            #si no hay nada en user, podemos crear un nuevo usuario
            #encriptamos el password, agregandole dos saltos(cadenas aleatorias)
            random_bytes = urandom(64)
            salt = b64encode(random_bytes).decode('utf-8')
            hashed_password = salt + sha256(salt+password).hexdigest()

            confirmation_code = str(uuid.uuid4().get_hex())

            new_user_key = cls(
                name=name,
                email=email,
                password=hashed_password,
                confirmation_code=confirmation_code
            ).put()
            print new_user_key.id()

            return {
                'created':True,
                'user_id':new_user_key.id(),
                'confirmation_code':confirmation_code
            }
        else:
            #si hay algo en user, no se puede crear nada
            return {
                'created':False,
                'title':'This email is already use',
                'message':'Please log in if this your email account'
            }

    @classmethod
    def check_password(cls, email, password):
        user = cls.check_if_exists(email)

        if user:
            hashed_password = user.password
            salt = hashed_password[:88]

            check_password = salt + sha256(salt+password).hexdigest()
            if check_password == hashed_password:
                return user.key.id()
            else:
                return None
        else:
            return None
