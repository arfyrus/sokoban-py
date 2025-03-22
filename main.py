import random
import numpy

class Object:
    def __init__(self, symbol, colour):
        self.symbol = symbol
        self.colour = colour

    def __str__(self):
        return f"{self.colour}{self.symbol}\x1b[0m"

(HEIGHT, WIDTH) = (10, 20)
SPACE = Object('*', '\x1b[2m')
OBSTACLE = Object('%', '\x1b[1;33m')
PLAYER = Object('@', '\x1b[1;36m')
TARGET = Object('X', '\x1b[1;35m')

player = numpy.array([0, 0])
obstacle = numpy.array([random.randint(1, WIDTH - 2), random.randint(1, HEIGHT - 2)])
# target = numpy.array([WIDTH - 1, HEIGHT - 1])
target = numpy.array([random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)])
game = True
grid = ['$' for _ in range(WIDTH * HEIGHT)]

index = lambda vec: vec[0] + vec[1] * WIDTH

def sync():
    global grid
    grid = [SPACE for _ in range(WIDTH * HEIGHT)]
    grid[index(target)] = TARGET
    grid[index(player)] = PLAYER
    grid[index(obstacle)] = OBSTACLE

def print_grid(win = True):
    sync()
    if not game:
        if win:
            print('\x1b[32m', end='')
        else:
            print('\x1b[31m', end='')
    print('+-' + '-' * WIDTH + '-+')
    for y in range(HEIGHT):
        print('| ', end='')
        for x in range(WIDTH):
            print('\x1b[0m', end='')
            print(grid[index((x, y))], end='')
        if not game:
            if win:
                print('\x1b[32m', end='')
            else:
                print('\x1b[31m', end='')
        print(' |')
    print('+-' + '-' * WIDTH + '-+')
    print('\x1b[0m', end='')

def valid_move(pos):
    (x, y) = pos
    return x >= 0 and x < WIDTH and y >= 0 and y < HEIGHT

if __name__ == "__main__":
    while (game):
        print_grid()
        moves = input("move (h/j/k/l): ")
        for move in moves:
            sync()
            # if not game:
            #     break
            change_vec = numpy.array([0, 0])

            if not move in 'hjkl':
                game = False
                break
            elif move == 'h' and player[0] > 0:
                change_vec = numpy.array([-1, +0])
            elif move == 'j' and player[1] < HEIGHT - 1:
                change_vec = numpy.array([+0, +1])
            elif move == 'k' and player[1] > 0:
                change_vec = numpy.array([+0, -1])
            elif move == 'l' and player[0] < WIDTH - 1:
                change_vec = numpy.array([+1, +0])
            else:
                continue

            if grid[index(player + change_vec)] == TARGET:
                continue
            if grid[index(player + change_vec)] == OBSTACLE:
                if not valid_move(obstacle + change_vec):
                    continue
                player += change_vec
                obstacle += change_vec
                if grid[index(obstacle)] == TARGET:
                    game = False
                    OBSTACLE = Object('$', '\x1b[1;32m')
                    SPACE = Object(' ', '')
            else:
                player += change_vec

            if obstacle[0] in (0, WIDTH - 1) and obstacle[1] in (0, HEIGHT - 1):
                game = False
                OBSTACLE = Object('%', '\x1b[1;31m')
                SPACE = Object(' ', '')
                print_grid(False)
                print("You're stuck!")
                break

            if not game:
                print_grid()
                print("You win!")
