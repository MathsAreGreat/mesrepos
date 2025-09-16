from massar.user import User
import os
import pickle
import base64

username = os.environ["MASSAR_ID"]
password = os.environ["MASSAR_PASS"]


def img_dwn(student):
    k = student.id
    img_file = f"/home/mohamed/Pictures/Massar/{k}.png"
    img_src = student.image
    if not os.path.exists(img_file) and ".png" not in img_src:
        print(k, "=>", student.name)
        imgdata = img_src.split(",")[-1]
        imgdata = base64.b64decode(imgdata)
        with open(img_file, 'wb') as f:
            f.write(imgdata)


def set_pics(lang):
    fpname = f'{lang.title()}_Moha.pk'
    if not os.path.exists(fpname):
        user = User(username, password).set_language("ar").scrap_students()
        with open(fpname, "wb") as e:
            pickle.dump(user, e)
    else:
        with open(fpname, 'rb') as e:
            user: User = pickle.load(e)
    sections = user.by_sections.values()
    for section in sections:
        students = section.students.values()
        for student in students:
            img_dwn(student)
    return sections


def fetch_students(lang):
    sections = set_pics(lang)
    students = []
    for section in sections:
        students += section.students.values()
    for student in sorted(students, key=lambda e: e.birthday):
        print(student)
    return 1


lang = "ar"
fetch_students(lang)
