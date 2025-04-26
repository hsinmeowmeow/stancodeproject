"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao.

File: breakoutgraphics_extension.py
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
WINDOW = GWindow(width=445, height=635, title='Select Mode') # Window for select mode


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

        # Create a score board
        self.score_board = GLabel('Bricks Left: ' + str(self.brick_num), x=0, y=self.window_height)
        self.score_board.font = '-20'
        self.window.add(self.score_board)

    def add_lives_board(self, lives):
        self.lives_board = GLabel('Lives Left: ' + str(lives), x=self.window_width-135, y=self.window_height)
        self.lives_board.font = '-20'
        self.window.add(self.lives_board)

    def change_lives_board(self, lives):
        self.lives_board.text = 'Lives Left: ' + str(lives)

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
            self.score_board.text = 'Bricks Left: ' + str(self.brick_num)
        return self.get_object

    def ball_reset(self):
        self.window.remove(self.ball)
        self.window.add(self.ball, x=self.window_width // 2 - self.ball_radius,
                        y=self.window_height // 2 - self.ball_radius)
        self.click = False


class SelectMode:

    def __init__(self):

        self.mode = None

        # Create a graphical window
        self.game_start = GLabel('Game Start!')
        self.game_start.font = '-40'
        WINDOW.add(self.game_start, x=(WINDOW.width-self.game_start.width)/2, y=130)

        # Create classic option
        self.classic_board = GRect(25, 25)
        self.classic_mode = GLabel('Classic Mode')
        self.classic_mode.font = '-25'
        self.classic_mode.color = 'black'
        WINDOW.add(self.classic_mode, x=(WINDOW.width - self.classic_mode.width) / 2,
                        y=420)
        WINDOW.add(self.classic_board, x=self.classic_mode.x - self.classic_board.width-3,
                        y=self.classic_mode.y-self.classic_mode.height-3)

        # Create random option
        self.random_board = GRect(25, 25)
        self.random_mode = GLabel('Random Mode')
        self.random_mode.font = '-25'
        self.random_mode.color = 'black'
        WINDOW.add(self.random_mode, x=(WINDOW.width - self.random_mode.width) / 2,
                        y=480)
        WINDOW.add(self.random_board, x=self.random_mode.x - self.random_board.width - 3,
                        y=self.random_mode.y - self.random_mode.height - 3)

        onmouseclicked(self.click_select)

    def click_select(self, mouse):
        if WINDOW.get_object_at(mouse.x, mouse.y) == self.random_board \
                or WINDOW.get_object_at(mouse.x, mouse.y) == self.classic_board:
            self.mode = WINDOW.get_object_at(mouse.x, mouse.y)
            return self.mode


class RandomMode:

    def __init__(self):
        WINDOW.clear()
        self.click_to_stop = GLabel('Click to stop')
        self.click_to_stop.font = '-40'
        WINDOW.add(self.click_to_stop, x=(WINDOW.width-self.click_to_stop.width)/2, y=130)

        self.brick_rows_num = random.randint(5, 12)
        self.brick_rows_sign = GLabel('Brick rows: ' + str(self.brick_rows_num))
        self.brick_rows_sign.font = '-40'

        onmouseclicked(self.return_variable)
        self.click = True

    def brick_rows(self):
        WINDOW.add(self.brick_rows_sign, x=(WINDOW.width - self.brick_rows_sign.width) / 2, y=300)

    def brick_rows_change(self):
        self.brick_rows_num = random.randint(5, 12)
        self.brick_rows_sign.text = 'Brick rows: ' + str(self.brick_rows_num)
        WINDOW.add(self.brick_rows_sign, x=(WINDOW.width - self.brick_rows_sign.width) / 2, y=300)

    def remove(self):
        WINDOW.remove(self.brick_rows_sign)

    def brick_cols(self):
        self.click = True
        self.brick_cols_num = random.randint(10, 30)
        self.brick_cols_sign = GLabel('Brick cols: ' + str(self.brick_cols_num))
        self.brick_cols_sign.font = '-40'
        WINDOW.add(self.brick_cols_sign, x=(WINDOW.width - self.brick_cols_sign.width) / 2, y=300)

    def brick_cols_change(self):
        self.brick_cols_num = random.randint(10, 30)
        self.brick_cols_sign.text = 'Brick cols: ' + str(self.brick_cols_num)
        WINDOW.add(self.brick_cols_sign, x=(WINDOW.width - self.brick_cols_sign.width) / 2, y=300)

    def return_variable(self, mouse):
        self.click = False
        return self.brick_rows_num
        return self.brick_cols_num


