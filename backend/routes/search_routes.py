from flask import Blueprint, render_template, request

search = Blueprint('search', __name__)
db = None  # Will be initialized via init_search_routes

def init_search_routes(database):
    global db
    db = database

@search.route("/search", methods=["GET"])
def search_route():
    query = request.args.get('query')
    results = db.search(query)
    return render_template("search.html", results=results)
