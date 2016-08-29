from framework.request_handler import YumSearchRequestHandler
from models.users import Users
from google.appengine.api import mail
import re
from os import environ

class RegisterUser(YumSearchRequestHandler):


    @classmethod
    def send_email(cls, to, user_id, confirmation_code):
        email_object = mail.EmailMessage(
            sender="una direccion",
            subject="Confirm your yum search account",
            to=to
        )
        email_parameters = {
            "domain":"http://localhost:8080" if environ['SERVER_SOFTWARE'].startswith('Development') else "http://yum-search-95.appspot.com",
            "user_id":user_id,
            "confirmation_code":confirmation_code
        }

        html_from_template = cls.jinja_enviroment.get_template("email/confirmation_email.html").render(email_parameters)
        email_object.html(html_from_template)
        email_object.send()

    def post(self):
        status = 200
        name = self.request.get('name')
        email = self.request.get('email')
        password = self.request.get('password')

        #validamos si se ingresaron los datos correspondientes
        if name and email and password:
            #expresion regular para correos electronicos
            email_validation_patter = ("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

            #validamos si el email introducido esta correcto
            if re.match(email_validation_patter, email):

                #agregamos un nuevo usuario
                user = Users.add_new_user(name,email,password)

                #si fue creado el usuario satisfactoriamente
                if user['created']:
                    html = self.jinja_enviroment.get_template('/commons/register_modal_success.html').render()
                    json_response = {
                        'html':html
                    }
                    #self.send_email(to=email, user_id=user['user_id'], confirmation_code=user['confirmation_code'])

                #caso contrario
                else:
                    status = 400
                    json_response = user

            #caso en que no sea valido el email
            else:
                status = 400
                json_response = {
                    'created' :False,
                    'title':'The email is invalid',
                    'message':'Please enter the valid email address'
                }
        #caso en que no se hayan ingresado datos
        else:
            status = 400
            json_response = {}

            if not name:
                json_response.update({
                    'title':'The name field is required',
                    'message' : 'Please fill in your name in order to continue'
                })
            if not email:
                json_response.update({
                    'title':'You have not send us an email!',
                    'message':'Please send us a valid email address, Thanks!'
                })
            if not password:
                json_response.update({
                    'title':'Please type in a password',
                    'message':'Please fill in your password in order to continue'
                })

        self.json_response(status_code=status, **json_response)