import os
import hashlib


def mdfy(f):
    return hashlib.md5(open(f, "rb").read()).hexdigest() + str(os.stat(f).st_size)

def grab(s_path):
    for c, _, files in os.walk(s_path):
        for f in files:
            _,ex=os.path.splitext(f)
            if ex == "" or ex == ".jpg1":
                org=os.path.join(c,f)
                if f[-1]=="1":
                    to=org+".jpg"
                if f[-1]=="2":
                    to=org+".jpeg"
                if f[-1]=="4":
                    to=org+".mp4"
                os.rename(org,to)
                print(">",f)

def hrab(s_path):
    for c, _, files in os.walk(s_path):
        for f in files:
            hash,ex=os.path.splitext(f)
            if ex != "":
                org=os.path.join(c,f)
                if ex == ".jpg":
                    to=os.path.join(c,hash+"1")
                if ex == ".jpeg":
                    to=os.path.join(c,hash+"2")
                if ex == ".mp4":
                    to=os.path.join(c,hash+"4")
                os.rename(org,to)
                print(">",f)
                
s_path = ".DCIMs"

grab(s_path)