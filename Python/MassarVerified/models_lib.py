import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from random import choice
from time import time
from typing import List
from uuid import uuid4
from zipfile import ZIP_DEFLATED, ZipFile

from lxml import etree

nmspc = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
ns = {"_": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

for p in Path("./").glob("tmp_*"):
    st = str(p)
    shutil.rmtree(st)

jsfie = "datas.json"
with open(jsfie, "r", encoding="utf-8") as e:
    comments = json.load(e)

jsfie = "students.json"
with open(jsfie, "r", encoding="utf-8") as e:
    infos = json.load(e)


def remarque(note):
    if float(note) == 0.0:
        return "Absence !!"
    points = [16, 15, 14, 13, 12, 11, 9, 8, 5, 0]
    for p in points:
        if note >= p:
            rq = choice(comments[f"{p}"])
            return rq


def gad(fn):
    table = MassarTable(fn)
    for student in table.students:
        marks = student.marks
        avg = sum(float(e) for e in marks) / 3
        # avg = float(marks[0])
        rmrq = remarque(avg)
        student.remark(rmrq)
    table.save()
    return 1


def get_files(pt):
    files = []
    for f in Path(pt).glob("*.xlsx"):
        if "updated" in f.stem:
            f.unlink()
        else:
            files.append(f)
    return files


def goo(pt="Files"):
    t = time()
    datas = 0
    print("Starting ..")
    files = get_files(pt)
    datas = []
    for f in files:
        c = gad(f)
        datas.append(c)
    e = time() - t

    print(len(datas), f"items in {e} seconds !")


@dataclass
class StudentRow:
    row: int
    nbr: str
    N: str
    name: str
    date: str
    marks: List[float]
    _remark: str = ""

    def remark(self, rmrk):
        self._remark = rmrk

    def __str__(self) -> str:
        return f"{self.N} : {self.name:<20} : {str(self.marks)}"


class MassarTable:
    def __init__(
        self,
        filename,
        nstudent_letter="C",
        name_letter="D",
        date_letter="F",
        marks_letters=["G", "I", "K"],
        remark_letter="M",
        start_index=18,
        offset=0,
        sheet_path="xl/worksheets/sheet1.xml",
        shared_strings_path="xl/sharedStrings.xml",
        tmp_path=Path(f"tmp_{uuid4()}"),
    ) -> None:
        self._tmp_path = tmp_path
        self._filename = filename
        self._nstudent_letter = nstudent_letter
        self._name_letter = name_letter
        self._date_letter = date_letter
        self._marks_letters = marks_letters
        self._remark_letters = remark_letter
        self._start_index = start_index
        self._sheet_path = sheet_path
        self.offset = offset
        self._shared_strings_path = shared_strings_path
        self._shared_strings = []
        self._classe = ""

        ZipFile(filename).extractall(self._tmp_path)

        fn = self._tmp_path / sheet_path
        with fn.open(encoding="utf8") as f:
            main_xml = f.read()

        self._main_xml_declaration = re.search(r"<\?.+?\?>", main_xml)[0]
        fn = self._tmp_path / shared_strings_path
        with fn.open(encoding="utf8") as f:
            shared_strings_xml = f.read()

        self._shared_strings_declaration = re.search(r"<\?.+?\?>", shared_strings_xml)[
            0
        ]
        self._main_sheet: etree.ElementBase = etree.fromstring(main_xml.encode("utf8"))
        self._shared_strings_xml: etree.ElementBase = etree.fromstring(
            shared_strings_xml.encode("utf8")
        )
        self._shared_strings = [
            v.text for v in self._shared_strings_xml.findall(".//_:t", namespaces=ns)
        ]
        self.students: List[StudentRow] = []
        self.Nstudent_map = {}

        self._cells = {
            c.attrib["r"]: c for c in self._main_sheet.findall(".//_:c", namespaces=ns)
        }

        row = start_index

        # Select the class
        cl = self.get_cell("I9")
        print(cl)
        self._classe = cl

        slet = f"{nstudent_letter}{row}"
        for _ in range(100):
            nlet = f"{name_letter}{row}"
            NBR = self.get_cell(slet)
            if not NBR:
                continue
            name = self.get_cell(nlet)
            student_notes = [self.get_cell(let + str(row)) for let in marks_letters]
            if infos.get(NBR):
                info = infos[NBR]
                student_notes = [float(v) for k, v in info.items() if "mark" in k]

            student = StudentRow(
                row,
                NBR,
                row,
                name,
                self.get_cell(f"{date_letter}{row}"),
                student_notes,
                self._cells[f"{remark_letter}{row}"].text,
            )
            self.students.append(student)
            self.Nstudent_map[student.N] = student
            row += 1
            slet = f"{nstudent_letter}{row}"

    def get_cell(self, row_name, nb=1):
        cell = self._cells[row_name]
        if nb == 0:
            return cell
        children = cell.getchildren()
        if not children:
            return None
        return children[0].text

    def save(self):
        length = len(self._shared_strings_xml.findall(".//_:si", namespaces=ns))
        strs = {}
        for student in self.students:
            for c, m in zip(self._marks_letters, student.marks):
                cell = f"{c}{student.row}"
                mark_node = self.get_cell(cell, 0)
                for child in mark_node.getchildren():
                    mark_node.remove(child)
                value = etree.SubElement(mark_node, f"{nmspc}v")
                value.text = str(m)
                mark_node.append(value)
                if student._remark not in strs:
                    si = etree.SubElement(self._shared_strings_xml, f"{nmspc}si")
                    si_t = etree.SubElement(si, f"{nmspc}t")
                    si_t.text = student._remark
                    si.append(si_t)
                    strs[student._remark] = length
                    length += 1
                cell = f"{self._remark_letters}{student.row}"
                rmrk_node = self.get_cell(cell, 0)
                for child in rmrk_node.getchildren():
                    rmrk_node.remove(child)
                value = etree.SubElement(rmrk_node, f"{nmspc}v")
                value.text = str(strs[student._remark])
                rmrk_node.append(value)
                rmrk_node.attrib["t"] = "s"

        with (self._tmp_path / self._sheet_path).open("w", encoding="utf8") as f:
            f.write(
                f"{self._main_xml_declaration}\n{
                    etree.tostring(
                        self._main_sheet, encoding='utf8', xml_declaration=False
                    ).decode('utf8')
                }"
            )
        with (self._tmp_path / self._shared_strings_path).open(
            "w", encoding="utf8"
        ) as f:
            f.write(
                f"{self._shared_strings_declaration}\n{
                    etree.tostring(
                        self._shared_strings_xml, encoding='utf8', xml_declaration=False
                    ).decode('utf8')
                }"
            )

        fs = list(self._filename.parts)
        fs[-2] = "Updates"
        Path(*fs[:-1]).mkdir(parents=True, exist_ok=True)
        fname = Path(*fs)

        with ZipFile(str(fname), "w", compression=ZIP_DEFLATED) as zip_f:
            for file_path in self._tmp_path.rglob("*"):
                zip_f.write(file_path, file_path.relative_to(self._tmp_path))
        shutil.rmtree(self._tmp_path)


table = MassarTable("Files/export_notesCC_1APIC-4_0019.xlsx")
for i, student in enumerate(table.students, start=1):
    print(i, student.nbr, ":")
    for i, mark in enumerate(student.marks, start=1):
        print("Mark", i, ":", mark)
    print()

# print(table._shared_strings)
