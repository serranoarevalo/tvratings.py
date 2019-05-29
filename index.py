from flask import Flask, Response, request, send_file
from tv_ratings import main

app = Flask(__name__)


@app.route("/")
def index():
    show_id = request.args.get("showId")
    if not show_id:
        return Response('Add the IMDB\'s show ID you want to the URL, for example: <a href="/?showId=tt0944947">/?showId=tt0944947</a> for Game of Thrones')
    else:
        image = main(show_id)
        return Response(image, mimetype="image/jpg")


if __name__ == "__main__":
    app.run()
