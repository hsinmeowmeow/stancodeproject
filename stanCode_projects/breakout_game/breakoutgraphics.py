"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao.

File: breakoutgraphics.py
Name: Una
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5  # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40  # Width of a brick (in pixels)
BRICK_HEIGHT = 15  # Height of a brick (in pixels)
BRICK_ROWS = 10  # Number of rows of bricks
BRICK_COLS = 10  # Number of columns of bricks
BRICK_OFFSET = 50  # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 10  # Radius of the ball (in pixels)
PADDLE_WIDTH = 75  # Width of the paddle (in pixels)
PADDLE_HEIGHT = 15  # Height of the paddle (in pixels)
PADDLE_OFFSET = 50  # Vertical offset of the paddle from the window bottom (in pixels)
INITIAL_Y_SPEED = 7  # Initial vertical speed for the ball
MAX_X_SPEED = 5  # Maximum initial horizontal speed for the ball


class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH, paddle_height=PADDLE_HEIGHT,
                 paddle_offset=PADDLE_OFFSET, brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS, brick_width=BRICK_WIDTH,
                 brick_height=BRICK_HEIGHT, brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, title='Breakout'):

        self.click = False
        self.get_object = None

        # Create a graphical window, with some extra space
        self.window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        self.window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=self.window_width, height=self.window_height, title=title)

        # Create a paddle
        self.paddle_offset = PADDLE_OFFSET
        self.paddle_width = PADDLE_WIDTH
        self.paddle = GRect(paddle_width, paddle_height)
        self.paddle.filled = True
        self.paddle.fill_color = 'black'
        self.window.add(self.paddle, x=(self.window_width - paddle_width) // 2, y=self.window_height - paddle_offset)

        # Center a filled ball in the graphical window
        self.ball_radius = BALL_RADIUS
        self.ball = GOval(ball_radius * 2, ball_radius * 2)
        self.ball.filled = True
        self.ball.fill_color = 'black'
        self.window.add(self.ball, x=self.window_width // 2 - ball_radius, y=self.window_height // 2 - ball_radius)

        # Default initial velocity for the ball
        self.__dx = 0
        self.__dy = INITIAL_Y_SPEED

        # Initialize our mouse listeners
        onmouseclicked(self.ball_move)
        onmousemoved(self.paddle_move)

        # Draw bricks
        self.brick_num = 0
        for i in range(0, brick_rows):
            brick_x = 0
            brick_color = 'red'
            if 1 < i < 4:
                brick_color = 'orange'
            elif 3 < i < 6:
                brick_color = 'yellow'
            elif 5 < i < 8:
                brick_color = 'green'
            elif 7 < i < 10:
                brick_color = 'blue'
            for j in range(0, brick_cols):
                self.brick = GRect(brick_width, brick_height)
                self.brick.filled = True
                self.brick.fill_color = brick_color
                self.window.add(self.brick, x=brick_x, y=brick_offset)
                brick_x += brick_width + brick_spacing
                self.brick_num += 1
            brick_offset += brick_height + brick_spacing

    def paddle_move(self, mouse):
        self.window.remove(self.paddle)
        if mouse.x < self.window.width - self.paddle_width:
            self.window.add(self.paddle, x=mouse.x, y=self.window.height - self.paddle_offset)
        else:
            self.window.add(self.paddle, x=self.window.width - self.paddle_width,
                            y=self.window.height - self.paddle_offset)

    def ball_move(self, mouse):
        self.click = True
        self.__dx = random.randint(1, MAX_X_SPEED)
        if random.random() > 0.5:
            self.__dx = -self.__dx

    def get_dx(self):
        return self.__dx

    def get_dy(self):
        return self.__dy

    def ball_object(self):
        # If the touch point is not None then stop checking the other touch points
        for i in range(self.ball.x, self.ball.x+self.ball_radius*3, self.ball_radius*2):
            for j in range(self.ball.y, self.ball.y+self.ball_radius*3, self.ball_radius*2):
                if self.get_object is None:
                    if self.window.get_object_at(i, j) is not None:
                        self.get_object = self.window.get_object_at(i, j)
        if self.get_object is not None and self.get_object != self.paddle:
            self.window.remove(self.get_object)
            self.brick_num -= 1
        return self.get_object

    def ball_reset(self):
        self.window.remove(self.ball)
        self.window.add(self.ball, x=self.window_width // 2 - self.ball_radius,
                        y=self.window_height // 2 - self.ball_radius)
        self.click = False
