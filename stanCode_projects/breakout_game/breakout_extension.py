"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

File: breakout_extension.py
Name: Una
----------------------
Play the breakout game.
"""

from campy.gui.events.timer import pause
from breakoutgraphics_extension import BreakoutGraphics
from breakoutgraphics_extension import SelectMode
from breakoutgraphics_extension import RandomMode

FRAME_RATE = 10         # 100 frames per second
NUM_LIVES = 3			# Number of attempts


def main():
    mode = SelectMode()
    while True:
        if mode.mode == mode.classic_board:
            graphics = BreakoutGraphics()
            break
        elif mode.mode == mode.random_board:
            brick_rows = random_mode_rows()
            brick_cols = random_mode_cols()
            graphics = BreakoutGraphics(brick_rows=brick_rows, brick_cols=brick_cols)
            break
        else:
            pause(FRAME_RATE)

    dx = graphics.get_dx()                          # Initial dx is 0
    dy = graphics.get_dy()
    lives = NUM_LIVES
    graphics.add_lives_board(lives)

    # Add the animation loop here!
    while True:
        if lives > 0 and graphics.brick_num != 0:
            if graphics.click:
                if dx == 0:                         # Get different start direction every click
                    dx = graphics.get_dx()
                graphics.ball.move(dx, dy)
                graphics.ball_object()
                if graphics.get_object is None and graphics.ball.y + graphics.ball.height > graphics.paddle.y:
                    graphics.ball_reset()
                    lives -= 1
                    graphics.change_lives_board(lives)
                    dx = 0                          # Set dx to 0 to enter first loop
                if graphics.get_object is not None:
                    graphics.get_object = None
                    dy = -dy
                if graphics.ball.x <= 0 or graphics.ball.x + graphics.ball.width >= graphics.window.width:
                    dx = -dx
                if graphics.ball.y <= 0 or graphics.ball.y + graphics.ball.height >= graphics.window.height:
                    dy = -dy
            pause(FRAME_RATE)
        else:
            break


def random_mode_rows():
    random_mode = RandomMode()
    random_mode.brick_rows()
    while True:
        if random_mode.click:
            random_mode.brick_rows_change()
            pause(FRAME_RATE)
        else:
            pause(FRAME_RATE)
            break
    pause(500)
    random_mode.remove()
    return random_mode.brick_rows_num


def random_mode_cols():
    random_mode = RandomMode()
    random_mode.click = True
    random_mode.brick_cols()
    while True:
        if random_mode.click:
            random_mode.brick_cols_change()
            pause(FRAME_RATE)
        else:
            pause(FRAME_RATE)
            break
    return random_mode.brick_cols_num


if __name__ == '__main__':
    main()
