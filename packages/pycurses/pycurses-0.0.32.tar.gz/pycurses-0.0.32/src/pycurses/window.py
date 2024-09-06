import curses

from pycurses.utils.general import fix_text_to_width, log
from pycurses.colors import CursesColors

class Window:

    class TitleStyle:
        FULL_LEFT = 0
        FULL_CENTER = 1
        FULL_RIGHT = 2
        SMALL_LEFT = 3
        SMALL_CENTER = 4
        SMALL_RIGHT = 5

        @staticmethod
        def is_full(value):
            return value in [Window.TitleStyle.FULL_LEFT, Window.TitleStyle.FULL_CENTER, Window.TitleStyle.FULL_RIGHT]

    """
        col, row = coordinates of the top left position of the window
        height, width = self explanatory
        parent = parent window
    """

    def __init__(self, parent=None, stdscr=None, colors=None, defaultchar=' ', defaultattr=0):
        self.parent = parent
        self.stdscr = stdscr
        if self.parent:
            self.stdscr = self.parent.stdscr
        self.changed = []
        self.children = []
        self.colors = CursesColors()
        self.col = 0
        self.row = 0
        self.height = 1
        self.width = 1
        self.default_char = (defaultchar, defaultattr)
        self.data = [[self.default_char for i in range(self.width)] for j in range(self.height)]
        self.set_all_changed()
        self.to_delete = False
        self.mn_width = None
        self.mn_height = None
        self.mx_width = None
        self.mx_height = None
        self.does_need_loop = False
        self.name = str(self.__class__)
        self.title = ''
        self.title_style = Window.TitleStyle.SMALL_LEFT
        self.title_color = self.colors.get_color_id("Cyan", "Black")

    def set_title(self, title):
        self.title = title
        self.refresh(self.stdscr)

    def set_title_style(self, style:int):
        self.title_style = style

    def set_name(self, new_name):
        self.name = new_name

    def set_max_height(self, h:int):
        self.mx_height = h

    def set_min_height(self, h:int):
        self.mn_height = h

    def set_max_width(self, w:int):
        self.mx_width = w

    def set_min_width(self, w:int):
        self.mn_width = w

    def max_height(self):
        return self.mx_height

    def max_width(self):
        return self.mx_width

    def min_height(self):
        return self.mn_height

    def min_width(self):
        return self.mn_width

    def set_needs_loop(self, loops:bool):
        self.does_need_loop = loops

    def needs_loop(self) -> bool:
        return self.does_need_loop

    def set_pos(self, col, row):
        self.col = col
        self.row = row
        self.set_all_changed()

    def resize(self, width, height):
        log("NEW SIZE")
        log((width, height))
        self.changed = []

        width_diff = width - self.width
        height_diff = height - self.height

        new_data = []
        for row_ind in range(height):
            if row_ind < len(self.data):
                new_row = self.data[row_ind]
            else:
                new_row = []
            for col_ind in range(width):
                if col_ind < len(new_row):
                    continue
                else:
                    new_row.append(self.default_char)
            new_data.append(new_row)
        self.data = new_data

        self.width = width
        self.height = height

        self.refresh(self.stdscr, force=True)

    def delete(self):
        self.to_delete = True

    def set_changed(self, row, col):
        self.changed.append((row, col))

    def get_changed(self):
        return self.changed

    def update_value(self, row, col, value, modifier):
        if row >= 0 and row < len(self.data):
            if col >= 0 and col < len(self.data[row]):
                new_tup = (value, modifier)
                if self.data[row][col] != new_tup:
                    self.data[row][col] = new_tup
                    self.set_changed(row, col)


    def draw_box(self, col, row, height, width, modifier=0,
                    topline='-', bottomline='-', rightline='|', leftline='|',
                    tl='+', tr='+', bl='+', br='+', fill=''):
        for i in range(1, width-1):
            self.update_value(row , col + i, topline, modifier)
            self.update_value(row + height - 1, col + i, bottomline, modifier)

        for i in range(1, height-1):
            self.update_value(row + i, col, leftline, modifier)
            self.update_value(row + i, col + width - 1, rightline, modifier)

        self.update_value(row, col, tl, modifier)
        self.update_value(row, col + width - 1, tr, modifier)
        self.update_value(row + height - 1, col, bl, modifier)
        self.update_value(row + height - 1, col + width - 1, br, modifier)

        if fill:
            for r in range(row+1, row+height - 1):
                for c in range(col+1, col + width - 1):
                    self.update_value(r, c, fill, modifier)

    def draw_button(self, col, row, content, **kwargs):
        body = ' {} '.format(content)
        self.draw_box(col, row, 3, len(body) + 2)
        for i in range(len(body)):
            self.update_value(row+1, col + i + 1, body[i], kwargs.get('modifier', 0))

    def draw_border(self, modifier=0, title="",
                    topline='-', bottomline='-', rightline='|', leftline='|',
                    tl='+', tr='+', bl='+', br='+'):
        self.draw_box(0, 0, self.height, self.width, modifier=modifier,
                        topline=topline, bottomline=bottomline, rightline=rightline,
                        leftline=leftline, tl=tl, tr=tr, bl=bl, br=br)
        if title:
            t = " {} ".format(title)
            for i in range(len(t)):
                self.update_value(0, i + 2, t[i], modifier | curses.A_REVERSE)

    def draw_text(self, text, row, col, mod):
        for i in range(len(text)):
            self.update_value(row, col+i, text[i], mod)

    def draw_text_box(self, text, row, col, height, width, alignment='l', mod=0):
        lines = fix_text_to_width(text, width, alignment=alignment)
        for r in range(min(height, len(lines))):
            line = lines[r]
            for i in range(len(line)):
                self.update_value(row + r, col + i, line[i], mod)

    def set_all_changed(self):
        for child in self.children:
            child.set_all_changed()
        for r in range(self.height):
            for c in range(self.width):
                self.set_changed(r, c)

    def remove_child(self, child):
        row = child.row
        col = child.col
        width = child.width
        height = child.height
        for r in range(height):
            for c in range(width):
                self.set_changed(row + r, col + c)
        self.children.remove(child)
        self.set_active(self)

    def prerefresh(self):
        pass

    def refresh(self, stdscr, force=False, seen_dict=None):
        self.prerefresh()

        for child in self.children:
            if child.to_delete:
                self.remove_child(child)

        if not seen_dict:
            seen_dict = {}

        if force:
            self.set_all_changed()

        if hasattr(self, 'popup_stack') and len(self.popup_stack) > 0:
            popups = getattr(self, 'popup_stack')
            for popup in reversed(popups):
                popup.refresh(stdscr, force=force, seen_dict=seen_dict)
        else:
            for child in reversed(self.children):
                child.refresh(stdscr, force=force, seen_dict=seen_dict)
                child.update_parent_indices(seen_dict)


        for coords in self.get_changed():
            if not seen_dict.get(coords, False):
                val, mod = self.get_value(*coords)
                row, col = self.get_scr_indices(*coords)
                try:
                    stdscr.addch(row, col, ord(val), mod)
                except:
                    pass

        title_vals = self.get_title_vals()
        for col in range(self.width):
            maybe_title_val = title_vals[col]
            coords = (0, col)

            if maybe_title_val or Window.TitleStyle.is_full(self.title_style):
                if not seen_dict.get(coords, False):
                    val, mod = self.get_value(*coords)
                    row, col = self.get_scr_indices(*coords)
                    try:
                        stdscr.addch(row, col, ord(val), mod)
                    except:
                        pass

        self.changed = []

    def get_scr_indices(self, row, col):
        outRow = self.row + row
        outCol = self.col + col
        if self.parent:
            pr, pc = self.parent.get_scr_indices(0, 0)
            outRow += pr
            outCol += pc
        return (outRow, outCol)

    def update_parent_indices(self, seen):
        for row in range(self.height):
            for col in range(self.width):
                ind = self.get_scr_indices(row, col)
                if ind  not in seen:
                    seen[ind] = True

    def get_value(self, row, col):
        if row == 0:
            title_values = self.get_title_vals()
            if col < len(title_values):
                val = title_values[col]
                if val:
                    #raise Exception(i, val)
                    return (val, self.title_color)
                if val is None:
                    if Window.TitleStyle.is_full(self.title_style):
                        return (' ', self.title_color)

        # Needs to include more information; color + modifiers
        if row < len(self.data):
            if col < len(self.data[row]):
                return self.data[row][col]
        return (' ', 0)

    def add_child(self, window, **kwargs):
        if not window.parent:
            window.parent = self
        if not window.colors:
            window.colors = self.colors
        if not window.stdscr:
            window.stdscr = self.stdscr
        self.children.append(window)

    def process_char(self, char):
        pass

    def set_active(self, window):
        if self.parent:
            self.parent.set_active(window)

    def set_cursor(self, row, col):
        self.parent.set_cursor(row, col)

    def has_title(self):
        return bool(self.title)

    def get_title_vals(self):
        if self.title:
            half_width = self.width // 2
            one_half = [None for i in range(half_width - 1)]
            two_half = [None for i in range(-1 + half_width + half_width % 2)]
            title = [' '] + [c for c in self.title] + [' ']
            if self.title_style in [Window.TitleStyle.FULL_LEFT, Window.TitleStyle.SMALL_LEFT]:
                return title + one_half + two_half
            if self.title_style in [Window.TitleStyle.FULL_RIGHT, Window.TitleStyle.SMALL_RIGHT]:
                return one_half + two_half + title
            return one_half + title + two_half
            #return ' ' * half_width + self.title + ' ' * (half_width + self.width % 2)
        else:
            return [None for i in range(self.width)]


