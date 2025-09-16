from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, db  # or firestore
import uuid

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate("firebase_config.json")
firebase_admin.initialize_app(
    cred,
    {
        "databaseURL": "https://schooling-80540-default-rtdb.firebaseio.com/"  # Replace with your DB URL
    },
)

# Reference
ref = db.reference("/")


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
def index():
    return render_template("index.html")


@app.route("/students")
def students():
    data = ref.child("students").get() or {}
    return render_template("students.html", students=data)


@app.route("/student/<id>")
def view_student(id):
    student = ref.child("students").child(id).get()
    if student:
        return render_template("student_detail.html", student=student, id=id)
    return "Student not found", 404


@app.route("/teachers")
def teachers():
    data = ref.child("teachers").get() or {}
    return render_template("teachers.html", teachers=data)


@app.route("/add_student", methods=["POST"])
def add_student():
    name = request.form["name"].title()
    profession = request.form["profession"]
    y, m, d = request.form["date"].split("-")
    student_id = str(uuid.uuid4())
    ref.child("students").child(student_id).set(
        {
            "name": name,
            "profession": profession,
            "date": {"jour": d, "mois": m, "annee": y},
        }
    )
    return redirect(url_for("students"))


@app.route("/add_teacher", methods=["POST"])
def add_teacher():
    name = request.form["name"]
    subject = request.form["subject"]
    teacher_id = str(uuid.uuid4())
    ref.child("teachers").child(teacher_id).set({"name": name, "subject": subject})
    return redirect(url_for("teachers"))


@app.route("/update_student/<id>", methods=["GET", "POST"])
def update_student(id):
    if request.method == "POST":
        name = request.form["name"].title()
        profession = request.form["profession"].title()
        y, m, d = request.form["date"].split("-")
        student_ref = ref.child("students").child(id)
        if student_ref.get():
            student_ref.set(
                {
                    "name": name,
                    "profession": profession,
                    "date": {"jour": d, "mois": m, "annee": y},
                }
            )
        return redirect(url_for("students"))
    student = ref.child("students").child(id).get()
    if student.get("date"):
        student["date"] = "-".join(
            [student["date"]["annee"], student["date"]["mois"], student["date"]["jour"]]
        )
    else:
        student["date"] = ""
    return render_template("student_update.html", student=student, id=id)


@app.route("/delete_student/<id>")
def delete_student(id):
    ref.child("students").child(id).delete()
    return redirect(url_for("students"))


@app.route("/delete_teacher/<id>")
def delete_teacher(id):
    ref.child("teachers").child(id).delete()
    return redirect(url_for("teachers"))


if __name__ == "__main__":
    app.run(debug=True, port=7000, host="0.0.0.0")
