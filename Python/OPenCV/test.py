from glob import glob
import os

for f in glob("/home/mohamed/Downloads/Library/Cima4u/Seasons/Friends/*/*mp4"):
    doc, _, name = f.rsplit("/", 2)
    fn = f"{doc}/{name}"
    os.rename(f, fn)
