from data.load_data import parse_text
from model import Recipe, app, connect_to_db


@app.route("/")
def index():
    return f"welcome to full spectrum eggs"


@app.route("/stock", methods=["GET"])
def get_stock():
    return


@app.route("/about", methods=["GET"])
def get_about():
    return parse_text("about")


@app.route("/recipes", methods=["GET"])
def get_recipes():
    r = Recipe.query.first()
    return {
        "name": r.name,
        "ingredients": [
            {
                "name": ingredient.name,
                # "qty": r.ingredients_recipes.
                # "units": ingredient.ingredient_units,
            }
            for ingredient in r.ingredients
        ],
        "instructions": r.instructions,
        "servings": r.servings,
        "source": r.source,
    }


if __name__ == "__main__":
    connect_to_db(app)
    app.run(port=5000, host="0.0.0.0")
