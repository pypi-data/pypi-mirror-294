from pycurses.window import Window
from pycurses.layout import Layout
from pycurses.mainwindow import MainWindow
from pycurses.list_view import ListView
from pycurses.utils import keys
from pycurses.popup import Popup, InputPopup

class TestWindow(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class TestApp(MainWindow):

    def __init__(self):
        super().__init__([])
        self.base_layout = Layout(colors=self.colors, defaultchar='.', defaultattr=0)
        self.left = Window(colors=self.colors, defaultchar='L', defaultattr=0)
        self.left.set_name('Left Window')
        self.right_layout = Layout(horizontal=False, colors=self.colors, defaultchar='.', defaultattr=0)
        self.right_layout.set_name('Right Layout')
        self.right = Window(colors=self.colors, defaultchar='.', defaultattr=0)
        self.right.set_min_height(8)
        self.right.set_name('Right Top')

        self.right_bottom  = ListView(headers=['word', 'another', 'third', 'a', 'b'], colors=self.colors, defaultchar='*', defaultattr=0)
        self.right_bottom.set_title('Right Bottom')

        self.right_layout.add_child(self.right, weight=2)
        self.right_layout.add_child(self.right_bottom, weight=5)
        self.base_layout.add_child(self.left, weight=2)
        self.base_layout.add_child(self.right_layout, weight=1)
        self.base_layout.set_title('VQC')
        self.add_child(self.base_layout)
        self.set_title('VQC')

    def process_char(self, char):
        if char == ord('j'):
            self.right_bottom.move_index_down()
        if char == ord('k'):
            self.right_bottom.move_index_up()
        if char == keys.ENTER:
            selected_record = self.right_bottom.get_selected_record()
            raise Exception(selected_record)
        if char == ord('/'):
            def input_confirm(text):
                raise Exception(text)
            def cancel():
                pass
            new_popup = InputPopup("Warning!!", "I'm not sure what's going on here but I don't like it", input_confirm, cancel, parent=self, colors=self.colors)
            self.add_popup(new_popup)

if __name__ == '__main__':
    TestApp().loop()
