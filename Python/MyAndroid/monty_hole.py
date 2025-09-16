import random

def monty_hall_game(switch):
    doors = ['car', 'goat', 'goat']
    random.shuffle(doors)

    choice = random.randint(0, 2)

    for i, door in enumerate(doors):
        if door == 'goat' and i != choice:
            revealed_goat = i
            break

    if switch:
        for i, door in enumerate(doors):
            if i != choice and i != revealed_goat:
                choice = i
                break

    return doors[choice] == 'car'

def simulate(n, switch):
    wins = sum(monty_hall_game(switch) for _ in range(n))
    return wins / n

n = 100000
print(f"Switching: {simulate(n, True):.2%}")
print(f"Not switching: {simulate(n, False):.2%}")