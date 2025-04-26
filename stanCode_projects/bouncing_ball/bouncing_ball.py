"""
File: bouncing_ball.py
Name: Una
-------------------------
TODO: Simulate the process of a ball falling down.
"""

from campy.graphics.gobjects import GOval
from campy.graphics.gwindow import GWindow
from campy.gui.events.timer import pause
from campy.gui.events.mouse import onmouseclicked

VX = 3
DELAY = 50
GRAVITY = 1
SIZE = 20
REDUCE = 0.9
START_X = 30
START_Y = 40
circle = GOval(SIZE, SIZE)
drop = True
window = GWindow(800, 500, title='bouncing_ball.py')


def main():
    """
    This program simulates a bouncing ball at (START_X, START_Y)
    that has VX as x velocity and 0 as y velocity. Each bounce reduces
    y velocity to REDUCE of itself.
    """
    window.add(circle, x=START_X, y=START_Y)
    onmouseclicked(ball_action)


def ball_action(mouse):
    global drop
    if drop:
        drop = False
        window.remove(circle)
        move_y = START_Y
        move_x = START_X
        falling_speed = 0
        reach_bottom = 0                                        # how many times of ball exceeding the window
        while reach_bottom < 3:
            while True:                                         # balls fall down
                move_x += VX
                move_y += GRAVITY + falling_speed
                falling_speed += GRAVITY
                if move_y + SIZE < 500:                         # balls not reach the bottom
                    window.add(circle, x=move_x, y=move_y)
                    pause(DELAY)
                    window.remove(circle)
                else:
                    move_y = 500 - SIZE                         # balls reaches the bottom
                    window.add(circle, x=move_x, y=500 - SIZE)
                    pause(DELAY)
                    window.remove(circle)
                    break
            falling_speed *= REDUCE
            while True:                                         # ball bounces back
                move_x += VX
                move_y -= GRAVITY + falling_speed
                falling_speed -= GRAVITY
                window.add(circle, x=move_x, y=move_y)
                pause(DELAY)
                window.remove(circle)
                if move_x >= 800:                               # ball exceeds the window
                    reach_bottom += 1
                if falling_speed < 0:
                    break
        window.add(circle, x=START_X, y=START_Y)
        drop = True


if __name__ == "__main__":
    main()
