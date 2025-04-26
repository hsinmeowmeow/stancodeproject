"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

File: breakout.py
Name: Una
----------------------
Play the breakout game.
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics

FRAME_RATE = 10         # 100 frames per second
NUM_LIVES = 3			# Number of attempts


def main():
    graphics = BreakoutGraphics()
    dx = graphics.get_dx()                              # Initial dx is 0
    dy = graphics.get_dy()
    lives = NUM_LIVES

    # Add the animation loop here!
    while True:
        if lives > 0 and graphics.brick_num != 0:
            if graphics.click:
                if dx == 0:                             # Get different start direction every click
                    dx = graphics.get_dx()
                graphics.ball.move(dx, dy)
                pause(FRAME_RATE)
                graphics.ball_object()
                if graphics.get_object is None and graphics.ball.y + graphics.ball.height > graphics.paddle.y:
                    graphics.ball_reset()
                    lives -= 1
                    dx = 0                             # Set dx to 0 to enter first loop
                if graphics.get_object is not None:
                    graphics.get_object = None
                    dy = -dy
                if graphics.ball.x <= 0 or graphics.ball.x + graphics.ball.width >= graphics.window.width:
                    dx = -dx
                if graphics.ball.y <= 0 or graphics.ball.y + graphics.ball.height >= graphics.window.height:
                    dy = -dy
            else:
                pause(FRAME_RATE)
        else:
            break


if __name__ == '__main__':
    main()
