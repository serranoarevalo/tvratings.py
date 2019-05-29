from flask import Flask, Response, request
from tv_ratings import main

app = Flask(__name__)


@app.route("/")
def index():
    show_id = request.args.get("showId")
    if not show_id:
        return Response("Add the IMDB's show ID you want to the URL by doing /?showId=tt0944947 for example")
    else:
        image = main(show_id)
        return Response(image, mimetype="image/png")


if __name__ == "__main__":
    app.run()
