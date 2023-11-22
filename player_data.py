import os

def save_player_name(name):
    filename = 'player_name.txt'
    with open(filename, 'w') as file:
        file.write(name)

def load_player_name():
    filename = 'player_name.txt'
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return file.read().strip()
    else:
        return None