from tools import getDatas

infos = {
    f's{s+1}-c{c+1}-e{e+1}': {
        'female': [
            '',
            '',
        ],
        'male': ['']
    }
    for s in range(2)
    for c in range(3)
    for e in range(3)
}

getDatas(infos)
