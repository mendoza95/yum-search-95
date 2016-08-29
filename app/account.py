from framework.request_handler import YumSearchRequestHandler


class UserAccount(YumSearchRequestHandler):

    @YumSearchRequestHandler.login_required
    def get(self):
        self.render("account/home.html")

class PostRecipe(YumSearchRequestHandler):
    @YumSearchRequestHandler.login_required
    def get(self):
        self.render("account/post_recipe.html")

    @YumSearchRequestHandler.login_required
    def post(self):
        user_key = self.check_user_logged_in.key
        title = self.request.get("title")
        cuisine = self.request.get("cuisine")
        difficulty = self.request.get("difficulty")
        ingredients = self.request.get("ingredients")
        prep_time = self.request.get("prep_time")
        cook_time = self.request.get("cooking_time")
        directions = self.request.get("directions")
        photo = self.request.POST['image']


