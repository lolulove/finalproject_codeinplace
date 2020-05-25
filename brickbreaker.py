"""
File: brickbreaker.py
----------------
Brick Breaker is a game which the player must smash a wall of bricks
 by deflecting a bouncing ball with a paddle.
The paddle moves horizontally and is controlled with the computer's mouse
or the touch of a finger (in the case of touchscreen).
It is required to smash all the bricks to win while the bouncing ball is
not allowed to touch the button wall more than twice.
If bouncing ball hits the button wall more than twice, its GAME OVER !!!
"""

import tkinter
import time


# How big is the playing area?
CANVAS_WIDTH = 600      # Width of drawing canvas in pixels
CANVAS_HEIGHT = 800     # Height of drawing canvas in pixels

# Constants for the bricks
N_ROWS = 10              # How many rows of bricks are there?
N_COLS = 10             # How many columns of bricks are there?
SPACING = 5             # How much space is there between each brick?
BRICK_START_Y = 50      # The y coordinate of the top-most brick
BRICK_HEIGHT = 20       # How many pixels high is each brick
BRICK_WIDTH = (CANVAS_WIDTH - (N_COLS+1) * SPACING) / N_COLS

# Constants for the ball and paddle
BALL_SIZE = 40
PADDLE_Y = CANVAS_HEIGHT - 40
PADDLE_WIDTH = 80


def main():
    # create the canvas with specified constant values
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Brick Breaker')
    # create the ball on the canvas
    ball = make_ball(canvas)
    # creates a value for y coordinate that is below the brick
    y = N_ROWS * (BRICK_HEIGHT + SPACING)
    # moves the ball to below the brick level
    canvas.move(ball, 0, y)
    # create the ball on the canvas
    paddle = make_paddle(canvas)
    # creates bricks
    create_brick(canvas)

    # ball displacement/movement values
    dx = 10
    dy = 7
    # initiates the number of playing turns
    turns = 3
    # initiates the counter to check playing turns
    start_rounds = 0

    # using initiated playing turns value for game control
    while turns >= start_rounds:
        # tracking the mouse
        mouse_x = canvas.winfo_pointerx()
        # translating mouse movement to paddle displacements
        canvas.moveto(paddle, mouse_x, PADDLE_Y)
        # ball movement by set displacement values
        canvas.move(ball, dx, dy)

        # tracks the ball hitting the side wall
        # and changing the directions respectively
        if hit_left_wall(canvas, ball) or hit_right_wall(canvas, ball):
            dx *= -1

        # tracks the ball hitting the button wall
        # changing the directions and increment playing turns
        if hit_bottom_wall(canvas, ball):
            start_rounds += 1
            # print("Round number: ", start_rounds)
            dy *= -1

        # tracks the ball hitting the top wall
        # and changes the directions
        if hit_top_wall(canvas, ball):
            dy *= -1

        # tracks the ball hitting the paddle
        # and changes the directions
        if paddle in collision(canvas, ball):
            dy *= -1

        # identifies the brick(s) in collision
        # deletes the brick(s) in collision
        # changing the directions
        for item in brick_count(canvas):
            if item in collision(canvas, ball):
                canvas.delete(item)
                dy *= -1

        # checks the remaining number the brick(s)
        # if remaining number equals zero,
        # print defined message, update canvas,
        # sleeps for a while and breaks the loop
        if len(brick_count(canvas)) == 0:
            message = "You win !!!"
            feedback(canvas, message, 2)
            canvas.update()
            time.sleep(50 / 50.)
            break

        # checks the playing turns value
        # if value equals 3,
        # print defined message, update canvas,
        # sleeps for a while and breaks the loop
        if turns == start_rounds:
            message = "Game Over !!!"
            feedback(canvas, message, 1)
            canvas.update()
            time.sleep(50 / 50.)
            break

        # redraw canvas
        canvas.update()
        # pause
        time.sleep(1 / 50.)


def create_brick(canvas):
    # create the bricks with specified constant values
    for row in range(N_ROWS):
        for col in range(N_COLS):
            draw_brick(canvas, row, col)


def feedback(canvas, message, num):
    # create the feedback message with specified formats
    # use specified constant values to determine
    # where to print the message
    x = (N_COLS * (BRICK_WIDTH + SPACING))/2
    y = N_ROWS * (BRICK_HEIGHT + SPACING) + 100
    if num == 1:
        message_color = 'red'
    else:
        message_color = 'green'
    canvas.create_text(x, y, text=message, fill=message_color, font=('verdana', 36))


def brick_count(canvas):
    # identifies all elements on the canvas
    # removes handle id of ball and paddle
    # returns a tuple of handle id(s) of the brick(s)
    item_handles_list = canvas.find_all()
    item_handles_list = item_handles_list[2:]
    return item_handles_list


def make_ball(canvas):
    # use specified constant values in making the ball
    return canvas.create_oval(0, 0, BALL_SIZE, BALL_SIZE, fill='black', outline='blue')


def make_paddle(canvas):
    # use specified constant values in making the paddle
    return canvas.create_rectangle(0, PADDLE_Y, PADDLE_WIDTH, CANVAS_HEIGHT - 20, fill='black')


def draw_brick(canvas, row, col):
    # use specified constant values in making the bricks
    # use a defined color list to change brick color
    x = col * (BRICK_WIDTH + SPACING)
    y = row * (BRICK_HEIGHT + SPACING)
    color_list = ['red', 'red', 'orange', 'orange', 'yellow', 'yellow', 'green', 'green', 'cyan', 'cyan', 'blue']

    if row > len(color_list) - 1:
        choice = 1
    else:
        choice = row

    canvas.create_rectangle(x, y, x + BRICK_WIDTH, y + BRICK_HEIGHT, fill=color_list[choice], outline='blue')


def get_top_y(canvas, object):
    '''
    This friendly method returns the y coordinate of the top of an object.
    Recall that canvas.coords(object) returns a list of the object 
    bounding box: [x_1, y_1, x_2, y_2]. The element at index 1 is the top-y
    '''
    return canvas.coords(object)[1]


def get_left_x(canvas, object):
    '''
    This friendly method returns the x coordinate of the left of an object.
    Recall that canvas.coords(object) returns a list of the object 
    bounding box: [x_1, y_1, x_2, y_2]. The element at index 0 is the left-x
    '''
    return canvas.coords(object)[0]


def hit_left_wall(canvas, object):
    '''
    This friendly method check if object hits the left wall comparing the
    x coordinate of the left of an object (left-x value) against zero and
    returns a boolean value.
    Since canvas.coords(object) returns a list of the object
    bounding box: [x_1, y_1, x_2, y_2]. The element at index 0 is the left-x
    '''
    return canvas.coords(object)[0] <= 0


def hit_top_wall(canvas, object):
    '''
        This friendly method check if object hits the top wall comparing the
        y coordinate of the top of an object (top-y value) against zero and
        returns a boolean value.
        Since canvas.coords(object) returns a list of the object bounding
        box: [x_1, y_1, x_2, y_2]. The element at index 1 is the top-y
    '''
    return canvas.coords(object)[1] <= 0


def hit_right_wall(canvas, object):
    ''''
    This friendly method check if object hits the right wall comparing the
    x coordinate of the right of an object (right-x value) against canvas width
    and returns a boolean value.
    Since canvas.coords(object) returns a list of the object bounding box:
    [x_1, y_1, x_2, y_2]. The element at index 2 is the right-x
    '''
    return canvas.coords(object)[2] >= CANVAS_WIDTH


def hit_bottom_wall(canvas, object):
    '''
        This friendly method check if object hits the bottom wall comparing the
        y coordinate of the bottom of an object (bottom-y value) against canvas
        height and returns a boolean value.
        Since canvas.coords(object) returns a list of the object bounding
        box: [x_1, y_1, x_2, y_2]. The element at index 3 is the bottom-y
    '''
    return canvas.coords(object)[3] >= CANVAS_HEIGHT


def collision(canvas, object):
    # gets the location of the ball as a list of coordinates
    # the list has four elements
    # gets all handle id(s) of objects in collision
    # returns a list of handle id(s) of objects in collision
    ball_coords = canvas.coords(object)
    x_1 = ball_coords[0]
    y_1 = ball_coords[1]
    x_2 = ball_coords[2]
    y_2 = ball_coords[3]
    colliding_list = canvas.find_overlapping(x_1, y_1, x_2, y_2)
    return colliding_list


def make_canvas(width, height, title):
    """
    DO NOT MODIFY
    Creates and returns a drawing canvas
    of the given int size with a blue border,
    ready for drawing.
    """
    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    top.title(title)
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1)
    canvas.pack()
    return canvas


if __name__ == '__main__':
    main()
