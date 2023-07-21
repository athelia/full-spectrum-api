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


#
# if __name__ == "__main__":
#
