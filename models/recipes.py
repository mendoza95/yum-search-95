from google.appengine.ext import ndb
from google.appengine.api import search

class Recipes(ndb.Model):
    user = ndb.KeyProperty(kind="Users")#relaciona con un usuario
    parsed = ndb.BooleanProperty(required=True)#no se para que es
    source_url = ndb.StringProperty(required=True)#tampoco se para que es
    title = ndb.StringProperty(required=True)
    cuisine = ndb.StringProperty()
    difficulty = ndb.StringProperty(choices=['Easy','Medium','Hard'])
    prep_time= ndb.IntegerProperty(default=0)
    cook_time = ndb.IntegerProperty(default=0)
    ingredients = ndb.JsonProperty()
    directions =ndb.TextProperty(repeated=True)
    photo_key = ndb.BlobKeyProperty()
    photo_url = ndb.StringProperty()

    @classmethod
    def parse_ingredients(cls, string_of_ingredients):
        pass

    @classmethod
    def parse_directions(cls, string_of_directions):
        pass

    @classmethod
    def add_new_recipe(cls, title, cuisine, difficulty, prep_time, cook_time, ingredients, directions, photo_key, photo_url, user_key=None, source_url=None):
        json_ingredients = cls.parse_ingredients(ingredients)
        list_directions = cls.parse_directions(directions)

        parsed = True
        user_id = ""

        if user_key:
            parsed=False
            user_id = str(user_key.id())

        recipe_key = cls(
            user=user_id,
            parsed=parsed,
            source_url=source_url,
            title=title,
            cuisine=cuisine,
            difficulty=difficulty,
            prep_time=int(prep_time),
            cook_time=int(cook_time),
            ingredients=json_ingredients,
            directions=list_directions,
            photo_key=photo_key,
            photo_url=photo_url
        ).put()

        index = search.Index('recipes')
        doc = search.Document(
            doc_id=str(recipe_key.id()),
            fields=[
                search.TextField(name="user_id", value=user_id),
                search.AtomField(name='parsed', value= '1' if parsed else '0'),
                search.TextField(name='title', value=title),
                search.TextField(name='cuisine', value=cuisine),
                search.TextField(name='difficulty', value=difficulty),
                search.NumberField(name='prep_time', value=int(prep_time)),
                search.NumberField(name='cook_time', value=int(cook_time)),
                search.TextField(name='ingredients', value=ingredients),
                search.TextField(name='directions', value=directions),
                search.TextField(name='photo_url', value=photo_url),

            ]
        )

        index.put(doc)