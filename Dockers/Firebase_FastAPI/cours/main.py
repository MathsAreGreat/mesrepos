from datetime import datetime
import json
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from firebase_admin import credentials, db, initialize_app
from random import shuffle
import re
import uuid
from starlette.responses import Response

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
# Firebase Init
cred = credentials.Certificate("firebase_config.json")
initialize_app(
    cred, {"databaseURL": "https://schooling-80540-default-rtdb.firebaseio.com/"}
)
ref = db.reference("/")

# Templates
templates = Jinja2Templates(directory="templates")

# Colors
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


# Utils
def generate(nb):
    datas = "azertyuiopmlkjhgfdsqwxcvbn"
    datas += datas.upper() + "1234567890"
    datas = list(datas) * nb
    shuffle(datas)
    return "".join(datas[:nb])


def listify(str_, nb=1):
    return [
        e.strip().title() if nb else e.strip() for e in str_.split("\n") if e.strip()
    ]


@app.middleware("http")
async def no_cache_middleware(request, call_next):
    response: Response = await call_next(request)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


# Routes
@app.get("/", response_class=HTMLResponse)
@app.get("/home", response_class=HTMLResponse)
async def index(request: Request):
    courses = ref.child("courses").get() or {}
    chapters = ref.child("chapters").get() or {}
    shuffle(colors)
    featured_courses = [
        {
            **v,
            "key": k,
            "color": colors[(i-1) % len(colors)],
            "level": chapters[v["chapter"]]["level"],
            "nbs": [e for e in list(f'=={i}') if e!= "="]
        }
        for i,(k, v) in enumerate(courses.items(), start=1)
    ]
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "Home Page",
            "featured_courses": featured_courses,
            "chapters": chapters,
        },
    )


@app.get("/courses")
async def get_courses():
    return ref.child("courses").get() or {}

@app.get("/initial")
async def init_todo(request: Request):
    try:
        with open("Students.json", "r") as fl:
            todos = json.load(fl)
        ref.child("students").update(todos)
        with open("s_chps.json", "r") as fl:
            todos = json.load(fl)
        ref.child("chapters").update(todos)
        with open("s_cours.json", "r") as fl:
            todos = json.load(fl)
        ref.child("courses").update(todos)
        return RedirectResponse(request.url_for("index"))
    except:
        return {"msg": "Failed to add the new item"}, 500
    

@app.get("/chapters")
async def get_chapters():
    return ref.child("chapters").get() or {}


@app.get("/article/{key}", response_class=HTMLResponse)
async def article(request: Request, key: str):
    chapters = ref.child("chapters").get() or {}
    info = ref.child("courses").child(key).get()
    info["key"] = key
    ch = chapters[info["chapter"]]
    info["chapter"] = ch["name"]
    info["level"] = ch["level"]
    return templates.TemplateResponse(
        "article.html", {"request": request, "props": info}
    )


@app.get("/uform/{key}", response_class=HTMLResponse)
async def form(request: Request, key: str):
    chs = ref.child("chapters").get() or {}
    chapters = sorted([(k, v["name"]) for k, v in chs.items()], key=lambda e: e[-1])
    if key == "new":
        key = generate(20)
        info = {
            "highlights": [],
            "requiremnts": [],
            "objectifs": [],
            "key": key,
            "level": "",
        }
    else:
        info = ref.child("courses").child(key).get() | {"key": key}
        ch = info["chapter"]
        info["level"] = chs[ch]["level"]
    return templates.TemplateResponse(
        "form.html",
        {"request": request, "title": "Add page", "info": info, "chapters": chapters},
    )


@app.post("/edit/{key}")
async def edit_form(
    request: Request,
    key: str,
    title: str = Form(...),
    desc: str = Form(...),
    level: str = Form(...),
    chapter: str = Form(""),
    highlights: str = Form(""),
    requiremnts: str = Form(""),
    objectifs: str = Form(""),
    content: str = Form(""),
    duration: int = Form(0),
):
    tr = title.title()
    desc = desc.title()
    level = level.title()
    ckey = chapter or generate(10)
    
    if not chapter:
        ref.child("chapters").child(ckey).set({"name": tr})
    ref.child("chapters").child(ckey).update({"level": level})

    data = {
        "chapter": ckey,
        "title": tr,
        "desc": desc,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "duration": duration,
        "highlights": listify(highlights),
        "requiremnts": listify(requiremnts),
        "objectifs": listify(objectifs),
        "content": "\n".join(listify(content, 0)),
    }
    ref.child("courses").child(key).update(data)
    return RedirectResponse(request.url_for("article", key=key), status_code=302)
