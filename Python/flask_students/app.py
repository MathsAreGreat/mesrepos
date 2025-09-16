import json
import os

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
DATA_FILE = "students.json"


def load_students():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    nbr = 0
    for key, v in data.items():
        name = " ".join(e for e in v["full_name"].split(" ") if e)
        name = name.replace("- ", "-")
        name = name.replace("Id ", "Id-").lower()
        for k in ["el", "ait"]:
            name = name.replace(f"{k} ", f"{k}-")
        name = name.strip().title()
        if name != v["full_name"]:
            nbr += 1
            v["full_name"] = name
            data[key] = v
    if nbr:
        save_students(data)

    return data


def save_students(students):
    with open(DATA_FILE, "w") as f:
        json.dump(students, f, indent=4)


@app.route("/")
def index():
    students = load_students()
    students = {
        k: v
        for k, v in students.items()
        if v["mark3"] < 1 and v.get("classe") and "1APIC3" in v["classe"]
    }

    return render_template("index.html", students=students.values())


@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        new_student = {
            "ID_number": request.form["id"],
            "full_name": request.form["name"],
            "mark1": int(request.form.get("mark1", 0)),
            "mark2": int(request.form.get("mark2", 0)),
            "mark3": int(request.form.get("mark3", 0)),
        }
        students = load_students()
        students[new_student["ID_number"]] = new_student
        save_students(students)
        return redirect(url_for("index"))
    return render_template("add.html")


@app.route("/update/<student_id>", methods=["GET", "POST"])
def update_student(student_id):
    students = load_students()
    student = next((s for s in students.values() if s["ID_number"] == student_id), None)
    if not student:
        return "Student not found", 404

    if request.method == "POST":
        for i in range(3):
            student[f"mark{i+1}"] = float(request.form[f"mark{i+1}"])
        save_students(students)
        return redirect(url_for("index"))

    return render_template("update.html", student=student)


if __name__ == "__main__":
    app.run(debug=True)
