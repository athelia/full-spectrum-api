from model import app, db


@app.route("/")
def index():
    return f"welcome to full spectrum eggs"


@app.route("/stock", methods=["GET"])
def get_stock():
    return


#
# if __name__ == "__main__":
#
