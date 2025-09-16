from time import sleep

from functions import data_update

nb = 0
while True:
    data_update(nb)
    sleep(1)
    nb += 1
    nb %= 100
    # if nb < 1:
    #     break
