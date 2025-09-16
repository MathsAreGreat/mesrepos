import chardet
from pathlib import Path
parent = Path("/home/mohamed/Downloads/aaja-nachle-2007-english-yify-345839")


def str2nb(st, sc=0, ms=0):
    st, dc = st.strip().split(",")
    dc = ms*100+int(dc)
    h, m, s = st.split(":")
    seconds = int(h)*3600+int(m)*60+int(s) + sc
    h, seconds = divmod(seconds, 3600)
    m, s = divmod(seconds, 60)
    return f"{h:02d}:{m:02d}:{s:02d},{dc}"


def gad(d, *add):
    return " --> ".join(str2nb(st, *add) for st in d.split("-->"))


for f in sorted(parent.glob("*.srt")):
    print(f)
    with open(f, 'rb') as file:
        # Use chardet to automatically detect the file encoding
        result = chardet.detect(file.read())
        detected_encoding = result['encoding']
    try:
        with open(f, "r", encoding=detected_encoding) as z:
            srt = z.read()
    except UnicodeDecodeError as e:
        print("Error decoding", f, "with detected encoding",
              detected_encoding, ":", e)
    break
datas = srt.split("\n\n")
# for i, data in enumerate(datas):
#     nb, d, *s = data.split("\n")
#     d = gad(d, 0)
#     datas[i] = "\n".join([nb, d, *s])

# with open(f, "w") as e:
#     e.write("\n\n".join(datas))
print(datas)
