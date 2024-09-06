import os
import sys
import curses
from pycurses.colors import CursesColors
from pycurses.window import Window
from pycurses.popup import Popup
from pycurses.utils.general import log

class MainWindow(Window):

    def __init__(self, args):
        self.scr = curses.initscr()
        curses.start_color()
        self.colors = CursesColors()

        curses.noecho() # Disables showing of what letter was pressed in the terminal at the cursor location
        curses.cbreak()
        height, width = self.size()
        stdscr = curses.newwin(height, width, 0, 0)
        stdscr.keypad(True)
        self.cursor = (0, 0)
        self.active_window = None
        self.popup_stack = []

        super().__init__(colors=self.colors, stdscr=stdscr, defaultchar='x')
        height, width = self.size()
        self.stdscr.resize(height, width)
        self.refresh(self.stdscr, force=True)

    def remove_child(self, child):
        if child in self.popup_stack:
            self.popup_stack.remove(child)
        super().remove_child(child)
        self.refresh(self.stdscr, force=True)

    def set_main_window(self, new_window:Window):
        self.main_window = new_window

    def terminate(self):
        self.stdscr.keypad(False)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        curses.nonl()

    def add_child(self, child):
        super().add_child(child)

    def resize(self, width, height):
        super().resize(width, height)

    def try_process_popup_char(self, char):
        if len(self.popup_stack) > 0:
            self.popup_stack[-1].process_char(char)
            return True
        return False

    def process_char(self, char):
        if len(self.popup_stack) > 0:
            self.popup_stack[-1].process_char(char)
        else:
            super().process_char(char)

    def loop(self):
        height, width = self.size()
        self.stdscr.resize(height, width)
        self.stdscr.refresh()
        if self.children:
            self.children[0].resize(width, height)

        self.refresh(self.stdscr, force=True)
        self.resize(width, height)
        self.refresh(self.stdscr, force=True)
        self.stdscr.refresh()

        #try:
        while True:
            self.refresh(self.stdscr)
            self.stdscr.refresh()
            self.stdscr.move(*self.cursor)
            ch = self.stdscr.getch()
            if ch == curses.KEY_RESIZE:
                height, width = self.size()
                self.stdscr.resize(height, width)
                self.resize(width, height)
                if self.children:
                    self.children[0].resize(width, height)
                continue
            else:
                self.get_active_window().process_char(ch)

        '''
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            log(exc_type)
            log(fname)
            log(exc_tb.tb_lineno)
            self.terminate()
            return 0
        '''

    def size(self):
        return self.scr.getmaxyx()

    def get_active_window(self):
        if self.active_window == None:
            return self
        return self.active_window

    def add_popup(self, popup):
        self.popup_stack.append(popup)
        self.add_child(popup)
        popup.resize(self.width // 2, self.height // 2)
        popup.refresh(self.stdscr, force=True)
        self.set_active(popup)

    def set_active(self, window):
        self.active_window = window

    def refresh(self, stdscr, force=False, seen_dict=None):
        super().refresh(stdscr, force=force, seen_dict=seen_dict)


if __name__ == '__main__':
    args = []
    win = MainWindow(args)
    win.loop()
