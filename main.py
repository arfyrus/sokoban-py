import random
import numpy
import tomllib

class Object:
    def __init__(self, symbol, colour):
        self.symbol = symbol
        self.colour = colour

    def __str__(self):
        return f"{self.colour}{self.symbol}\x1b[0m"

with open ("config.toml", mode = "rb") as fp:
    config = tomllib.load(fp)

(HEIGHT, WIDTH) = (config['height'], config['width'])

SPACE = Object(config['space']['symbol']['neutral'], config['space']['colour']['neutral'].replace("\\x1b", "\x1b"))
OBSTACLE = Object(config['obstacle']['symbol']['neutral'], config['obstacle']['colour']['neutral'].replace("\\x1b", "\x1b"))
PLAYER = Object(config['player']['symbol']['neutral'], config['player']['colour']['neutral'].replace("\\x1b", "\x1b"))
TARGET = Object(config['target']['symbol']['neutral'], config['target']['colour']['neutral'].replace("\\x1b", "\x1b"))

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

def print_grid(status = 'D'):
    sync()
    match status:
        case 'W':
            print(config['edge']['win'].replace("\\x1b", "\x1b"), end='')
        case 'L':
            print(config['edge']['loss'].replace("\\x1b", "\x1b"), end='')
        case _:
            print(config['edge']['neutral'].replace("\\x1b", "\x1b"), end='')

    print('+-' + '-' * WIDTH + '-+')
    for y in range(HEIGHT):
        print('| ', end='')
        for x in range(WIDTH):
            print('\x1b[0m', end='')
            print(grid[index((x, y))], end='')
        match status:
            case 'W':
                print(config['edge']['win'].replace("\\x1b", "\x1b"), end='')
            case 'L':
                print(config['edge']['loss'].replace("\\x1b", "\x1b"), end='')
            case _:
                print(config['edge']['neutral'].replace("\\x1b", "\x1b"), end='')
        print(' |')
    print('+-' + '-' * WIDTH + '-+')
    print('\x1b[0m', end='')

def valid_move(pos):
    (x, y) = pos
    return x >= 0 and x < WIDTH and y >= 0 and y < HEIGHT

if __name__ == "__main__":
    while (game):
        print_grid()
        moves = input("Move (h/j/k/l): ")
        for move in moves:
            sync()
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
                    SPACE = Object(config['space']['symbol']['win'], config['space']['colour']['win'].replace("\\x1b", "\x1b"))
                    OBSTACLE = Object(config['obstacle']['symbol']['win'], config['obstacle']['colour']['win'].replace("\\x1b", "\x1b"))
                    PLAYER = Object(config['player']['symbol']['win'], config['player']['colour']['win'].replace("\\x1b", "\x1b"))
                    TARGET = Object(config['target']['symbol']['win'], config['target']['colour']['win'].replace("\\x1b", "\x1b"))
                    print_grid('W')
                    print("You win!")
                    break
            else:
                player += change_vec

            if obstacle[0] in (0, WIDTH - 1) and obstacle[1] in (0, HEIGHT - 1):
                # TODO:
                # Also lose if the obstacle is on an edge where the target isn't since it's impossible to remove from that side.
                game = False
                SPACE = Object(config['space']['symbol']['loss'], config['space']['colour']['loss'].replace("\\x1b", "\x1b"))
                OBSTACLE = Object(config['obstacle']['symbol']['loss'], config['obstacle']['colour']['loss'].replace("\\x1b", "\x1b"))
                PLAYER = Object(config['player']['symbol']['loss'], config['player']['colour']['loss'].replace("\\x1b", "\x1b"))
                TARGET = Object(config['target']['symbol']['loss'], config['target']['colour']['loss'].replace("\\x1b", "\x1b"))
                print_grid('L')
                print("You're stuck!")
                break
