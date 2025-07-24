#!/usr/bin/env python3
# Created by Dominic Hopfe

import os
import keyboard  # Requires 'pip install keyboard'
import time
import random

# Grid dimensions
rows = 6
cols = 15

# Start in the middle
x = cols // 2
y = rows // 2

# Enemy positions (random but not overlapping player)
def random_position(exclude=[]):
    while True:
        pos = (random.randint(0, cols - 1), random.randint(0, rows - 1))
        if pos not in exclude:
            return pos

enemy1 = random_position(exclude=[(x, y)])
enemy2 = random_position(exclude=[(x, y), enemy1])
enemy3 = random_position(exclude=[(x, y), enemy1, enemy2])
enemy4 = random_position(exclude=[(x, y), enemy1, enemy2, enemy3])

def clear_screen():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except:
        pass

def draw_grid():
    print("Use W/A/S/D to move, Q to quit.\n")
    for i in range(rows):
        row = ''
        for j in range(cols):
            if i == y and j == x:
                row += '0'  # Player
            elif (j, i) == enemy1 or (j, i) == enemy2 or (j, i) == enemy3 or (j, i) == enemy4:
                row += 'E'  # Enemies
            else:
                row += '-'
        print(row)

def wrap_position(x, y):
    return x % cols, y % rows

def move_toward_player(enemy_pos):
    ex, ey = enemy_pos
    dx = dy = 0

    # Determine shortest path using wraparound logic
    dx_raw = (x - ex)
    dy_raw = (y - ey)

    if abs(dx_raw) > cols // 2:
        dx = -1 if dx_raw > 0 else 1
    elif dx_raw != 0:
        dx = 1 if dx_raw > 0 else -1

    if abs(dy_raw) > rows // 2:
        dy = -1 if dy_raw > 0 else 1
    elif dy_raw != 0:
        dy = 1 if dy_raw > 0 else -1

    # Randomly prioritize x or y axis
    if random.choice([True, False]):
        new_pos = wrap_position(ex + dx, ey)
    else:
        new_pos = wrap_position(ex, ey + dy)

    return new_pos

# Initial display
clear_screen()
draw_grid()

while True:
    moved = False
    if keyboard.is_pressed('w'):
        y -= 1
        moved = True
    elif keyboard.is_pressed('s'):
        y += 1
        moved = True
    elif keyboard.is_pressed('a'):
        x -= 1
        moved = True
    elif keyboard.is_pressed('d'):
        x += 1
        moved = True
    elif keyboard.is_pressed('q'):
        print("\nExiting...")
        break

    if moved:
        # Wrap player position
        x, y = wrap_position(x, y)

        # Move enemies toward player (with wrap)
        enemy1 = move_toward_player(enemy1)
        enemy2 = move_toward_player(enemy2)
        enemy3 = move_toward_player(enemy3)
        enemy4 = move_toward_player(enemy4)

        clear_screen()
        draw_grid()

    # Check for collision
    if (x, y) == enemy1 or (x, y) == enemy2 or (x, y) == enemy3 or (x, y) == enemy4:
        print("\nYou were caught by an enemy! Game Over.")
        break

    time.sleep(0.1)
