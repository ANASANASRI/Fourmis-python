import numpy as np

def langton_ant(steps):
    # Définition de la grille et des couleurs
    grid_size = 100
    grid = np.zeros((grid_size, grid_size), dtype=int)
    white, black = 0, 1

    # Définition de la direction de départ de la fourmi et de sa position
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    direction = 0
    row, col = grid_size // 2, grid_size // 2

    for step in range(steps):
        # Changement de direction
        current_color = grid[row][col]
        direction = (direction + 1) % 4 if current_color == white else (direction - 1 + 4) % 4

        # Changement de couleur
        grid[row][col] = black if current_color == white else white

        # Déplacement de la fourmi
        row += directions[direction][0]
        col += directions[direction][1]

    return grid
