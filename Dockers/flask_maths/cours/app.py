import json
import re
from pathlib import Path

from bson.objectid import ObjectId
from flask import Flask, redirect, render_template, request, url_for
from pymongo import MongoClient

app = Flask(__name__)


# --- Utility Functions ---
def get_db():
    client = MongoClient("mongodb://mongo:27017/")
    db = client.course_db
    return db.chapters, db.courses


def save_ch(key, ch, module, titre, duree):
    if module:
        chapter = chapters_col.find_one({"key": ch})
        for i, chm in enumerate(chapter["modules"]):
            cours = [e for e in chm["cours"] if e[0] != key]
            chm["cours"] = cours
            chapter["modules"][i] = chm

        module -= 1
        infos = {}
        cours = chapter["modules"][module]["cours"]
        for k, n, d in cours:
            infos[k] = [n, d]

        infos[key] = [titre, duree]
        chapter["modules"][module]["cours"] = [[k, *v] for k, v in infos.items()]
        chapters_col.update_one({"_id": chapter["_id"]}, {"$set": chapter})


def format_key(text):
    text = text.lower()
    text = re.sub(r"[éèê]", "e", text)
    text = re.sub(r"[àâ]", "a", text)
    text = re.sub(r"î", "i", text)
    text = re.sub(r"ù", "u", text)
    text = re.sub(r"ç", "c", text)
    return re.sub(r"[^0-9a-z]+", "-", text)


def load_students():
    chapters_col, courses_col = get_db()
    parent_path = Path("static/datas")
    data_file = parent_path / "syllabes.json"
    if not data_file.exists():
        return chapters_col, courses_col

    with data_file.open("r") as f:
        datas = json.load(f)

    existing_chapters = {c["key"] for c in chapters_col.find()}
    existing_courses = {c["key"] for c in courses_col.find()}

    for data in datas:
        chapter_key = format_key(data["title"])
        for module in data["modules"]:
            for idx, (_, title, duration) in enumerate(module["cours"]):
                course_key = format_key(title)
                module["cours"][idx] = [course_key, title, duration]
                if course_key not in existing_courses:
                    courses_col.insert_one(
                        {
                            "key": course_key,
                            "chapter": chapter_key,
                            "title": title,
                            "level": data["level"],
                            "duration": duration,
                            "content": "",
                            "info": {},
                        }
                    )
        data["key"] = chapter_key
        if chapter_key not in existing_chapters:
            del data["_id"]
            chapters_col.insert_one(data)
    for chapter in chapters_col.find():
        for i, module in enumerate(chapter["modules"]):
            hs = 0
            for idx, cour in enumerate(module["cours"]):
                h = re.sub(r"[^0-9]", r"", f"{cour[-1]}")
                hr = int(h)
                hs += hr
                cour[-1] = hr
                module["cours"][idx] = cour
            module["hours"] = hs
            chapter["modules"][i] = module

        chapters_col.update_one({"_id": chapter["_id"]}, {"$set": chapter})

    return chapters_col, courses_col


# --- Global Setup ---
chapter_keys = ["key", "title", "duration", "description", "level", "price", "color"]

colors = [
    "primary",
    "purple-500",
    "green-500",
    "amber-500",
    "rose-500",
    "cyan-500",
    "blue-500",
    "orange-500",
    "violet-500",
    "lime-500",
]

chapters_col, courses_col = load_students()
myitems = [("", "-- Select Module --")] + [
    (c["key"], c["title"]) for c in chapters_col.find()
]


@app.after_request
def add_header(response):
    # Disable caching
    response.headers["Cache-Control"] = (
        "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    )
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "-1"
    return response


# --- Routes ---
@app.route("/")
@app.route("/home")
def index():
    testimonials = [
        {
            "msg": "The Calculus course completely changed my approach...",
            "stars": 5,
            "sigle": "JD",
            "name": "James Davidson",
            "title": "Engineering Student",
        },
        {
            "msg": "As someone returning to mathematics after years away...",
            "stars": 5,
            "sigle": "EM",
            "name": "Elena Martinez",
            "title": "Data Analyst",
        },
        {
            "msg": "The Linear Algebra course exceeded my expectations...",
            "stars": 5,
            "sigle": "RK",
            "name": "Raj Kumar",
            "title": "ML Engineer",
        },
    ]

    db_infos = list(chapters_col.find())
    featured_courses = [
        {k: v for k, v in doc.items() if k in chapter_keys}
        | {"color": colors[i % len(colors)]}
        for i, doc in enumerate(db_infos)
    ]

    specialized_courses = [
        {"title": "Differential Equations", "description": "...", "color": "blue"},
        {"title": "Topology", "description": "...", "color": "purple"},
        {"title": "Mathematical Finance", "description": "...", "color": "green"},
        {"title": "Numerical Analysis", "description": "...", "color": "orange"},
    ]

    return render_template(
        "index.html",
        featured_courses=enumerate(featured_courses, 1),
        specialized_courses=specialized_courses,
        area={
            "title": "What Our Students Say",
            "description": "...",
            "comments": testimonials,
        },
        myitems=myitems,
    )


@app.route("/courses")
def get_courses():
    todos = list(courses_col.find())
    for todo in todos:
        todo["_id"] = str(todo["_id"])
    return todos


@app.route("/initial")
def reset_courses():
    chapters_col.delete_many({})
    return redirect(url_for("index"))


@app.route("/syllabus/<key>")
def syllabus(key):
    props = chapters_col.find_one({"key": key})
    if props:
        props["_id"] = str(props["_id"])
    return render_template("syllabus.html", props=props, myitems=myitems)


@app.route("/course/<key>")
def course(key):
    info = courses_col.find_one({"key": key})
    if not info:
        return redirect(url_for("add_form", nbr="new"))
    info["_id"] = str(info["_id"])
    info.setdefault("highlights", "")
    info["chapter"] = next(
        (title for k, title in myitems if k == info["chapter"]), "None"
    )
    return render_template("article.html", props=info, myitems=myitems)


@app.route("/chapters")
def get_chapters():
    todos = list(chapters_col.find())
    for todo in todos:
        todo["_id"] = str(todo["_id"])
    return todos


@app.route("/add/<nbr>", methods=["GET", "POST"])
def add_form(nbr):
    if request.method == "POST":
        ch = request.form.get("chapter", "")
        module = int(request.form.get("module"))
        key = format_key(request.form.get("title", ""))
        titre = request.form.get("title", "").title()
        duree = int(request.form.get("duration", 0))

        save_ch(key, ch, module, titre, duree)
        info = {
            "chapter": ch,
            "content": request.form.get("content", ""),
            "duration": duree,
            "highlights": ",".join(
                e.strip().title()
                for e in request.form.get("highlights", "").split(",")
                if e.strip()
            ),
            "level": request.form.get("level", "").title(),
            "title": titre,
        }
        info["key"] = key
        info["infos"] = {}
        courses_col.insert_one(info)
        return redirect(url_for("add_form", nbr=nbr))

    if nbr != "new":
        return redirect(url_for("edit_form", nbr=nbr))

    info = {
        "nbr": "new",
        "chapter": "",
        "content": "",
        "duration": "",
        "highlights": "",
        "level": "",
        "title": "",
        "fn": "add_form",
    }
    return render_template(
        "form.html", info=info, myitems=myitems, title="Add new course"
    )


@app.route("/edit/<nbr>", methods=["GET", "POST"])
def edit_form(nbr):
    if request.method == "POST":
        ch = request.form.get("chapter", "")
        module = int(request.form.get("module"))
        key = format_key(request.form.get("title", ""))
        titre = request.form.get("title", "").title()
        duree = int(request.form.get("duration", 0))

        save_ch(key, ch, module, titre, duree)

        cs = request.form.get("content", "").split("\n")

        content = " ".join(e.strip() for e in cs if e.strip())
        requirements =[e.strip().title() for e in request.form.get("requiremnts", "").split("\n") if e.strip()]
        objectifs =[e.strip().title() for e in request.form.get("objectifs", "").split("\n") if e.strip()]

        info = {
            "chapter": ch,
            "content": content,
            "duration": duree,
            "highlights": ",".join(
                e.strip().title()
                for e in request.form.get("highlights", "").split(",")
                if e.strip()
            ),
            "infos": [
                {"title":"Pré-requis", "icon":"check","cours": requirements},
                {"title":"Compétences visées", "icon":"medal", "cours": objectifs}
            ],
            "level": request.form.get("level", "").title(),
            "title": titre,
            "key": key,
        }
        courses_col.update_one({"_id": ObjectId(nbr)}, {"$set": info})
        return redirect(url_for("course", key=info["key"]))

    info = courses_col.find_one({"_id": ObjectId(nbr)})
    if not info:
        return redirect(url_for("add_form", nbr="new"))
    if not info.get("infos") or not isinstance(info.get("infos"), list):
        info["infos"]=[]
        info["requiremnts"]=""
        info["objectifs"]=""
    else:
        info["requiremnts"] = "\n".join(info["infos"][0]["cours"])
        info["objectifs"] = "\n".join(info["infos"][1]["cours"])

    info.update({"_id": str(info["_id"]), "fn": "edit_form", "nbr": nbr})
    return render_template("form.html", info=info, myitems=myitems, title="Edit course")


@app.route("/del/<nbr>")
def del_form():
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=7000, host="0.0.0.0")
