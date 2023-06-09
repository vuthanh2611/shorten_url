import string
from datetime import datetime
import random
from repo_students import Link, repository
from flask import Flask, request, render_template, redirect, url_for
import requests

app = Flask(__name__)


def generate_hash_id():
    char = string.ascii_letters + string.digits
    return "".join(random.choice(char) for _ in range(6))


total_link = []


# class InvalidUrl(Exception):
#     pass


def is_valid_url(url):
    # schema, netloc, *_ = parse.urlparse(url)
    # if not schema or not netloc:
    #     return False
    # else:
    #     return True
    try:
        response = requests.head(url)
        return response.ok
    except requests.exceptions.RequestException:
        return False


@app.route("/", methods={"GET", "POST"})
def index_endpoint():
    shorten_link = ""
    if request.method == "POST":
        url_link = request.form.get("link")
        if is_valid_url(url_link):
            hash_id = generate_hash_id()
            link = Link(url=url_link, hash_id=hash_id, created_at=datetime.utcnow())
            repository.create(link)
            shorten_link = repository.get(hash_id=hash_id)
            total_link.append(shorten_link)
            return redirect(url_for("track_link_endpoint"))
        else:
            error_message = "Invalid URL. Please enter a valid URL."
            return render_template(
                "url.html", shorten_link=shorten_link, error_message=error_message
            )
    return render_template("url.html", shorten_link=shorten_link)


@app.route("/<hash_id>")
def redirect_to_original(hash_id):
    link = repository.get(hash_id=hash_id)
    if link is not None:
        repository.update(link)
        return redirect(link.url)
    else:
        return "invalid url"


@app.route("/track_link", methods={"GET", "POST"})
def track_link_endpoint():
    return render_template("track_link.html", total_link=total_link)


@app.route("/favicon.ico")
def favicon():
    return "", 404


if __name__ == "__main__":
    app.run(debug=True)
