from api.model import EggStockRecord, Recipe, app, connect_to_db


@app.route("/api/")
def index():
    return f"welcome to full spectrum eggs"


@app.route("/api/stock", methods=["GET"])
def get_stock():
    pass


@app.route("/api/egg-stock-records", methods=["GET"])
def get_egg_stock_records():
    records = EggStockRecord.query.all()
    return [record.to_json() for record in records]


@app.route("/api/about", methods=["GET"])
def get_about():
    return "Full Spectrum Eggs is based in Clarkston, Georgia."


@app.route("/api/recipes", methods=["GET"])
def get_recipes():
    recipes = Recipe.query.all()
    return [recipe.to_json() for recipe in recipes]


@app.route("/api/recipe/<recipe_id>", methods=["GET"])
def get_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    return recipe.to_json()


if __name__ == "__main__":
    connect_to_db(app)
    app.run(port=5000, host="0.0.0.0")
