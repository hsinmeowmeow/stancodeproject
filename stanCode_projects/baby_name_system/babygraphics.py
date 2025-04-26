"""
File: babygraphics.py
Name: Una
--------------------------------
SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.
--------------------------------
Create the line graphics to show the change of the popularity of baby names by year.
"""

import tkinter
import babynames
import babygraphicsgui as gui

FILENAMES = [
    'data/full/baby-1900.txt', 'data/full/baby-1910.txt',
    'data/full/baby-1920.txt', 'data/full/baby-1930.txt',
    'data/full/baby-1940.txt', 'data/full/baby-1950.txt',
    'data/full/baby-1960.txt', 'data/full/baby-1970.txt',
    'data/full/baby-1980.txt', 'data/full/baby-1990.txt',
    'data/full/baby-2000.txt', 'data/full/baby-2010.txt',
    'data/full/baby-2020.txt'
]
CANVAS_WIDTH = 1080
CANVAS_HEIGHT = 600
YEARS = [1900, 1910, 1920, 1930, 1940, 1950,
         1960, 1970, 1980, 1990, 2000, 2010, 2020]
GRAPH_MARGIN_SIZE = 20
COLORS = ['red', 'purple', 'green', 'blue']
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index where the current year is in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                            with the current year.
    """
    return GRAPH_MARGIN_SIZE+((width-GRAPH_MARGIN_SIZE*2)/(len(YEARS))*year_index)


def draw_fixed_lines(canvas):
    """
    Draws the fixed background lines on the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
    """
    canvas.delete('all')            # delete all existing lines from the canvas

    # ----- Write your code below this line ----- #
    # Draw the upmost and bottom line
    canvas.create_line(GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE, CANVAS_WIDTH-GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE,
                       width=LINE_WIDTH)
    canvas.create_line(GRAPH_MARGIN_SIZE, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE, CANVAS_WIDTH-GRAPH_MARGIN_SIZE,
                       CANVAS_HEIGHT-GRAPH_MARGIN_SIZE, width=LINE_WIDTH)
    year_index = 0                  # the index where the current year is in the YEARS list
    for year in YEARS:
        canvas.create_line(get_x_coordinate(CANVAS_WIDTH, year_index), 0, get_x_coordinate(CANVAS_WIDTH, year_index),
                           CANVAS_HEIGHT, width=LINE_WIDTH)
        canvas.create_text(get_x_coordinate(CANVAS_WIDTH, year_index)+TEXT_DX, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE,
                           text=year, anchor=tkinter.NW)
        year_index += 1


def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)        # draw the fixed background grid

    # ----- Write your code below this line ----- #
    name_index = 0                  # the index where the current name is in the lookup_names list
    for name in lookup_names:
        color = COLORS[name_index % len(COLORS)]
        for i in range(len(YEARS)):
            # Calculate the y coordinate of the beginning point of the line
            if str(YEARS[i]) in name_data[name]:
                rank = int(name_data[name][str(YEARS[i])])
                rank_y = GRAPH_MARGIN_SIZE + ((CANVAS_HEIGHT - GRAPH_MARGIN_SIZE * 2) / (MAX_RANK - 1) * (rank - 1))
                rank_shown = rank
            else:
                rank_y = CANVAS_HEIGHT - GRAPH_MARGIN_SIZE
                rank_shown = '*'
            # Calculate the y coordinate of the end point of the line
            if i+1 < len(YEARS):    # not exceed the range of list
                if str(YEARS[i + 1]) in name_data[name]:
                    next_rank = int(name_data[name][str(YEARS[i + 1])])
                    next_rank_y = GRAPH_MARGIN_SIZE + (
                        (CANVAS_HEIGHT - GRAPH_MARGIN_SIZE * 2) / (MAX_RANK - 1) * (next_rank - 1))
                else:
                    next_rank_y = CANVAS_HEIGHT - GRAPH_MARGIN_SIZE
                canvas.create_line(get_x_coordinate(CANVAS_WIDTH, i), rank_y, get_x_coordinate(CANVAS_WIDTH, i+1),
                                   next_rank_y, width=LINE_WIDTH, fill=color)
            canvas.create_text(get_x_coordinate(CANVAS_WIDTH, i)+TEXT_DX, rank_y, text=name+' '+str(rank_shown),
                               anchor=tkinter.SW, fill=color)
        name_index += 1


# main() code is provided, feel free to read through it but DO NOT MODIFY
def main():
    # Load data
    name_data = babynames.read_files(FILENAMES)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names)

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == '__main__':
    main()
