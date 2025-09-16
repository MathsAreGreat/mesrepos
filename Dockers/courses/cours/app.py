import json
from random import shuffle

from bson.objectid import ObjectId
from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient
from pymongo.errors import PyMongoError

app = Flask(__name__)


def generate(nb):
    datas = "azertyuiopmlkjhgfdsqwxcvbn"
    datas += datas.upper()
    datas += "1234567890"
    datas = list(datas)
    datas = datas * nb
    shuffle(datas)
    return "".join(datas[:nb])


def reload():
    client = MongoClient("mongodb://mongo:27017/")
    db = client.cours_db
    return db.cours


cours_collection = reload()


@app.after_request
def add_header(response):
    # Disable caching
    response.headers["Cache-Control"] = (
        "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    )
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "-1"
    return response

@app.route("/")
@app.route("/home")
def Index():
    cours_collection = reload()
    todos = list(cours_collection.find())
    infos = {}
    for todo in todos:
        ID = str(todo["_id"])
        ch = todo["chapter"]
        if ch not in infos:
            if not todo.get("chapter_id"):
                cours_collection.update_many(
                    {"chapter": ch}, {"$set": {"chapter_id": generate(10)}}
                )
            infos[ch] = []
        infos[ch].append((ID, todo["code"], todo["title"]))
    todos = [[k, *infos[k]] for k in sorted(infos)]
    return render_template("index.html", corps=todos)


@app.route("/removeall")
def removeall():
    cours_collection.delete_many({})
    return jsonify({"msg": "Remove chapters"}), 500


@app.route("/add", methods=["GET", "POST"])
def manage_todo():
    if request.method == "GET":
        try:
            # Handle the GET request: Generate code and fetch unique chapters
            code = generate(10)
            chapters = {
                e["chapter_id"]: e["chapter"] for e in list(cours_collection.find())
            }
            chapters = sorted(chapters.items(), key=lambda x: x[-1])
            return render_template("add.html", code=code, chapters=chapters)
        except PyMongoError:
            return jsonify({"msg": "Failed to load chapters"}), 500

    elif request.method == "POST":
        try:
            # Handle the POST request: Add new todo item
            new_todo = request.json

            # Basic validation for the essential fields
            if not new_todo or "title" not in new_todo or "chapter" not in new_todo:
                return jsonify({"msg": "Invalid input data"}), 400

            # Capitalize the title and chapter
            new_todo["title"] = new_todo["title"].title()
            new_todo["chapter"] = (
                new_todo["chapter"].title()
                if "..." in new_todo["chapter"]
                else new_todo["title"]
            )

            result = cours_collection.insert_one(new_todo)
            return jsonify({"nb": str(result.inserted_id), "msg": "Added!"})
        except PyMongoError:
            return jsonify({"msg": "Failed to add the new item"}), 500


@app.route("/initial", methods=["GET"])
def init_todo():
    try:
        with open("mesdata.json", "r") as fl:
            todos = json.load(fl)
        seen_codes = set()
        for new_todo in todos:
            # Capitalize the title and chapter
            if new_todo["code"] in seen_codes:
                continue
            del new_todo["_id"]
            result = cours_collection.insert_one(new_todo)
            seen_codes.add(new_todo["code"])
        return jsonify({"nb": str(result.inserted_id), "msg": "Added!"})
    except PyMongoError:
        return jsonify({"msg": "Failed to add the new item"}), 500


@app.route("/edit/<id>", methods=["POST"])
def edit_todo(id):
    new_todo = request.json
    if new_todo.get("title"):
        new_todo["title"] = new_todo["title"].title().strip()
        cour = (
            new_todo["content"]
            .replace('"imgs/', '"/static/imgs/')
            .replace('"/imgs/', '"/static/imgs/')
        )
        cour = [e.strip() for e in cour.split("\n")]
        new_todo["content"] = " ".join(cour)
        if "Select A Chapter" in new_todo["chapter"]:
            new_todo["chapter"] = new_todo["title"]
            new_todo["chapter_id"] = generate(10)

    new_todo["chapter"] = new_todo["chapter"].title().strip()
    new_todo["nb"] = int(new_todo["nb"])
    cours_collection.update_one({"_id": ObjectId(id)}, {"$set": new_todo})
    return {"msg": "Added !", "todo": new_todo}


@app.route("/cours", methods=["GET"])
def cours():
    todos = list(cours_collection.find())
    for todo in todos:
        todo["_id"] = str(todo["_id"])
    return todos


@app.route("/search/<q>", methods=["GET"])
def search(q):
    todos = list(cours_collection.find({"chapter": q}))

    for todo in todos:
        todo["_id"] = str(todo["_id"])

    return todos


@app.route("/course/<id>", methods=["GET"])
def course(id):
    todo = cours_collection.find_one({"code": id})
    todo["_id"] = str(todo["_id"])
    return todo


@app.route("/cour/<id>", methods=["GET"])
def cour(id):
    cours_collection = reload()
    todo = cours_collection.find_one({"code": id})
    todo["_id"] = str(todo["_id"])
    related = [
        [e.get("nb", 1), e["code"], e["title"]]
        for e in cours_collection.find({"chapter": todo["chapter"]})
        if str(e["code"]) != id
    ]
    return render_template(
        "cour.html",
        todo=todo,
        related=sorted(related, key=lambda e: e[0]),
        titre=f"{todo['title']} | {todo['chapter']}",
    )


@app.route("/chapter/<id>", methods=["GET", "POST"])
def chapter(id):
    if request.method == "GET":
        todos = list(cours_collection.find({"chapter_id": id}))
        for i, todo in enumerate(todos):
            todo["_id"] = str(todo["_id"])
            todo["nb"] = todo.get("nb", 0)
            todos[i] = todo
        return render_template(
            "chapter.html",
            todos=sorted(todos, key=lambda todo: int(todo["nb"])),
            title=f"Classement | {id}",
        )


@app.route("/cour/edit/<id>", methods=["GET"])
def editcour(id):
    todos = cours_collection.find_one({"_id": ObjectId(id)})
    todos["nb"] = int(todos.get("nb", 1))
    chapters = {e["chapter_id"]: e["chapter"] for e in list(cours_collection.find())}
    chapters = sorted(chapters.items(), key=lambda x: x[-1])
    return render_template("edit.html", todo=todos, chapters=chapters)


if __name__ == "__main__":
    app.run(debug=True, port=7000, host="0.0.0.0")
