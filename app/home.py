from framework.request_handler import YumSearchRequestHandler

class Home(YumSearchRequestHandler):
    def get(self):
        self.render('home/home.html')