from docxtpl import DocxTemplate
from concurrent.futures import ThreadPoolExecutor
import os
import shutil
# os.chdir("/home/mohamed/Documents/Files/Best")

references = {
    "default": {
        'school': 'ثانوية الزراوي التأهيلية',
        'director': 'إبراهيم باط'
    },
    "converts": {
        "s1": "الدورة الأولى",
        "s2": "الدورة الثانية",
        "e1": "الفرض الأول",
        "e2": "الفرض الثاني",
        "e3": "الفرض الثالث",
        "c1": "السنة الأولى إعدادي",
        "c2": "السنة الثانية إعدادي",
        "c3": "السنة الثالثة إعدادي"
    }
}


def save(info):
    p = info['gender']
    context = info['context']
    name = f"{context['name']} ({context['key']})"
    cnv = references["converts"]
    sem, classe, exam = [cnv[e] for e in context["key"].split('-')]
    out = f"Backups/{context['school']}/{classe}/{sem}/{exam}"
    temp = f"temp/{context['school']}/{classe}/{sem}/{exam}"
    pdfile = f"{out}/{context['name']}.pdf"
    if os.path.exists(pdfile):
        print(f"{name}.pdf already exists !")
        return 0
    context["exam"] = exam
    context["level"] = classe
    context["semestre"] = sem
    generatDoc = "Generated"
    os.makedirs("Logs", exist_ok=True)
    os.makedirs(generatDoc, exist_ok=True)
    os.makedirs(out, exist_ok=True)
    os.makedirs(temp, exist_ok=True)
    docfile = f"{temp}/{name}.docx"
    if not os.path.exists(docfile):
        doc = DocxTemplate(f"/home/mohamed/Documents/Files/Best/{p}.docx")
        msg = f'Rendering {p}.docx ..'
        print(f'{msg:<30}', end="\r")
        doc.render(context)
        msg = f'Saving {name}.docx ..'
        print(f'{msg:<30}', end="\r")
        doc.save(docfile)
    cmd = f"libreoffice --convert-to pdf '{
        docfile}' --outdir '{generatDoc}' >> 'Logs/{name}.log'"
    msg = f'Saving {name}.pdf ..'
    print(f'{msg:<30}', end="\r")
    os.system(cmd)
    shutil.copyfile(
        f"{generatDoc}/{name}.pdf",
        pdfile
    )
    print(f'{name}.pdf is saved with success !')
    return 1


def getDatas(infos):
    datas = []
    for key, vals in infos.items():
        for gr, eleves in vals.items():
            for eleve in eleves:
                context = {}
                context["key"] = key
                context["name"] = eleve
                context.update(references["default"])
                data = {
                    "gender": gr,
                    "context": context
                }
                datas.append(data)
    with ThreadPoolExecutor(1) as executor:
        executor.map(save, datas)
    shutil.rmtree("temp", ignore_errors=True)
    return datas


if __name__ == "__main__":
    os.chdir("/home/mohamed/Documents/Files/تقارير")
    name = "Heurs Supp"
    docfile = f"{name}.odt"
    generatDoc = f"{name}.pdf"
    cmd = f"libreoffice --convert-to pdf '{docfile}' >> '{name}.log'"
    msg = f'Saving {name}.pdf ..'
    print(f'{msg:<30}', end="\r")
    os.system(cmd)
