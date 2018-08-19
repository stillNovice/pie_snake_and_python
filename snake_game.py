import curses
import locale
import random

screen = curses.initscr()

curses.start_color()

curses.curs_set(0)	# set the cursor to 0, so that it doesn't appear on the screen

screenHeight, screenWidth = screen.getmaxyx()
beginY = beginX = 0
newWindow = curses.newwin(screenHeight, screenWidth, beginY, beginX)

newWindow.keypad(1)
newWindow.timeout(100)

snake_x = screenWidth // 4
snake_y = screenHeight // 2

snake = [
    [snake_y, snake_x],
    [snake_y, snake_x - 1],
    [snake_y, snake_x - 2]
]

food = [screenHeight // 2, screenWidth // 2]

newWindow.addch(food[0], food[1], curses.ACS_PI)

key = curses.KEY_RIGHT
score = 0
while True:
    next_key = newWindow.getch()
    
    # when the user want to go back from the head, its not possible
    if key == curses.KEY_RIGHT and next_key == curses.KEY_LEFT:
        continue

    if key == curses.KEY_LEFT and next_key == curses.KEY_RIGHT:
        continue

    if key == curses.KEY_DOWN and next_key == curses.KEY_UP:
        continue

    if key == curses.KEY_UP and next_key == curses.KEY_DOWN:
        continue

    key = key if next_key == -1 else next_key

    if snake[0][0] in [0, screenHeight, screenHeight - 1] or snake[0][1] in [0, screenWidth, screenWidth - 1] or snake[0] in snake[1:]:
        newWindow.clear()
        
        spaces = ''
        for i in range(0, (screenWidth // 2) - 13):
            spaces += ' '

        newWindow.addstr(screenHeight // 2, (screenWidth // 2) - 10, 'Your Score is: ' + str(score) + '\n' + spaces + 'PRESS ANY KEY TO EXIT\n')

        break

    new_head_of_snake = [snake[0][0], snake[0][1]]

    if key == curses.KEY_DOWN:
        new_head_of_snake[0] += 1

    if key == curses.KEY_UP:
        new_head_of_snake[0] -= 1

    if key == curses.KEY_LEFT:
        new_head_of_snake[1] -= 1

    if key == curses.KEY_RIGHT:
        new_head_of_snake[1] += 1

    snake.insert(0, new_head_of_snake)

    if snake[0] == food:
        score += 1
        food = None

        while food is None:
            new_food = [
                random.randint(1, screenHeight - 1),
                random.randint(1, screenWidth - 1)
            ]

            food = new_food if new_food not in snake else None

        newWindow.addch(food[0], food[1], curses.ACS_PI)
    else:
        tail = snake.pop()
        newWindow.addch(tail[0], tail[1], ' ')

    newWindow.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)

while True:
    key = newWindow.getch()
    if key != -1:
        curses.endwin()
        quit()
