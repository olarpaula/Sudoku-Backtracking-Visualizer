import pygame

pygame.font.init()

screen = pygame.display.set_mode((500, 550))
pygame.display.set_caption("Sudoku Solver Visualizer")

fonts = [pygame.font.SysFont("comicsans", 40), pygame.font.SysFont("comicsans", 30)]

run = True
solve_board = 0
board_solved = False
draw_box_flag = True

FIREBRICK = (178, 34, 34)
PINK = (255, 192, 203)
INDIANRED = (205, 92, 92)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# positions in the board
square_idx = 500 / 9
x = 0
y = 0

# default sudoku board
board  =[
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]

# function that draws the board with values and colors the occupied cells
def draw_board():
    screen.fill(WHITE)
    # fill the board occupied cells with color pink and current values
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                pygame.draw.rect(screen, PINK, pygame.Rect(i * square_idx, j * square_idx, square_idx + 1, square_idx + 1))
                draw_number(board[i][j], i, j)

    for i in range(10):
        width = 3
        endPoint = i * square_idx
        if i % 3 == 0:
            width *=  2

        # draw horizontal and vertical lines
        pygame.draw.line(screen, INDIANRED, (0, endPoint), (500, endPoint), width)
        pygame.draw.line(screen, INDIANRED, (endPoint, 0), (endPoint, 500), width)

# function that draws a number position(x, y) in the board
def draw_number(number, x=None, y=None):
    text = fonts[0].render(str(number), True, BLACK)
    screen.blit(text, (x * square_idx + 15, y * square_idx + 15))

# function that highlights the current cell in the board
def draw_box(pos):
    pygame.draw.rect(screen, FIREBRICK, pygame.Rect(pos[0]*square_idx, pos[1]*square_idx, square_idx+1, square_idx+1), 5)  # width = 5

# function that displays messages about game status
def draw_information(solved):
    info = ["Press Enter to view solution solving ;)", "Solving...", "Solved! :D"]

    if solved == 0:
        text = fonts[1].render(info[0], True, BLACK)
        pos = (65, 517)

    elif solved == 1:
        text = fonts[1].render(info[1], True, BLACK)
        pos = (200, 517)

    else:
        text = fonts[1].render(info[2], True, BLACK)
        pos = (190, 517)

    screen.blit(text, pos)

# function that transforms mouse coordinates in board coordinates
def get_coordinates(pos):
    global x, y
    x = pos[0] // square_idx
    y = pos[1] // square_idx

# function that checks if a number can be placed in a certain position in the board
def is_valid_position(board, val, pos):
    # check row and col
    for i in range(9):
        if board[pos[0]][i] == val or board[i][pos[1]] == val:
            return False

    # check box
    box_x = pos[0]//3
    box_y = pos[1]//3

    for i in range(box_x*3, box_x*3+3):
        for j in range(box_y*3, box_y*3+3):
            if board[i][j] == val:
                return False

    return True

# function that finds empty cells in the board
def find_empty_cell(board):
    for i in range(9):
        for j in range(9):
            if board[j][i] == 0:
                return (j, i)

    return None

# function that autosolves the board
def solve(board):
    find_empty = find_empty_cell(board)
    if not find_empty:
        return True
    else:
        pos = find_empty

    pygame.event.pump()
    for i in range(1, 10):
        if is_valid_position(board, i, pos):
            board[pos[0]][pos[1]] = i

            draw_board()
            draw_box(pos)
            draw_information(1)
            pygame.display.update()
            pygame.time.delay(50)

            if solve(board):
                return True

            board[pos[0]][pos[1]] = 0

            draw_board()
            draw_box(pos)
            draw_information(1)
            pygame.display.update()
            pygame.time.delay(50)

    return False

# the loop that keeps the program working
while run:
    val = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            get_coordinates(pos)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                val = 1

            if event.key == pygame.K_2:
                val = 2

            if event.key == pygame.K_3:
                val = 3

            if event.key == pygame.K_4:
                val = 4

            if event.key == pygame.K_5:
                val = 5

            if event.key == pygame.K_6:
                val = 6

            if event.key == pygame.K_7:
                val = 7

            if event.key == pygame.K_8:
                val = 8

            if event.key == pygame.K_9:
                val = 9

            if event.key == pygame.K_RETURN:
                solve_board = 1

            if event.key == pygame.K_RIGHT:
                if(x < 8):
                    x += 1

            if event.key == pygame.K_DOWN:
                if(y < 8):
                    y += 1

            if event.key == pygame.K_LEFT:
                if(x > 0):
                    x -= 1

            if event.key == pygame.K_UP:
                if(y > 0):
                    y -= 1

    if solve_board == 1:
        if solve(board) == True:
            board_solved = 1

    if val != 0:
        draw_number(val, x, y)
        pos = (x, y)
        if is_valid_position(board, val, pos) == True:
            board[pos[0]][pos[1]] = val
        else:
            board[pos[0]][pos[1]] = 0

    if board_solved == 1:
        draw_box_flag = False

    draw_board()
    if draw_box_flag:
        pos = (x, y)
        draw_box(pos)

    if board_solved:
        draw_information(2)
    else:
        draw_information(0)

    pygame.display.update()

pygame.quit()

