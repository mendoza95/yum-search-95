from framework.request_handler import YumSearchRequestHandler
from models.users import Users

class LoginUser(YumSearchRequestHandler):
    def get(self):
        self.render("login/login.html")

    def post(self):
        email = self.request.get("email")
        password = self.request.get("password")

        user_id = Users.check_password(email, password)

        if user_id:
            self.send_cookie('User',user_id)
            self.redirect('/account')
        else:
            self.redirect('/login')
