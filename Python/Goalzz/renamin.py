from datetime import datetime

dt = 1693141200


def datatime(dt, gmt=1):
    timestamp = dt+gmt*3600
    date = datetime.utcfromtimestamp(timestamp)
    la_date = date.strftime('%H:%M:%S')
    lheur = date.strftime('%H:%M:%S')
    return la_date, lheur
