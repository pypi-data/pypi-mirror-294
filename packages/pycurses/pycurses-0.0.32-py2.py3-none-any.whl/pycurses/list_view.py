
import curses
from pycurses.window import Window
from pycurses.utils.general import log

class ListView(Window):

    def __init__(self, headers=None, row_height=1, parent=None, colors=None, defaultchar=' ', defaultattr=0):
        super().__init__(parent=parent, colors=colors, defaultchar=' ', defaultattr=defaultattr)
        self.row_height = row_height
        self.current_index = 0
        self.horizontal_line = '-'
        self.vertical_line = '|'
        self.header_mod = curses.A_UNDERLINE
        self.selected_mod = curses.A_UNDERLINE
        self.set_header_style("Green", "Black")
        self.set_selected_style("Yellow", "Black")
        self.row_data = []
        if not headers:
            self.headers = []
        else:
            self.headers = headers
        self.update_row_data()

    def set_header_style(self, background, foreground):
        self.header_mod = self.colors.get_color_id(background, foreground)

    def set_selected_style(self, background, foreground):
        self.selected_mod = self.colors.get_color_id(background, foreground)


    def get_row_data(self, row_index):
        rows = self.row_data
        if row_index >= 0 and row_index < len(rows):
            return rows[row_index]
        return None

    def update_row_data(self):
        rows = self.regenerate_rows()
        self.row_data = rows

    def regenerate_rows(self):
        rows = [
                ['dog', 2, 3920, ' dsf', 2131],
                ['dog', 2, 3920, ' dsf', 2131],
                ['tacos', 99, 20, 'jsomdsf', 213123423],
                ['burger', 98, 201, 'wordup', 3423],
                ['dog', 2, 3920, ' dsf', 2131],
                ['tacos', 99, 20, ' somdsf', 213123423],
                ['burger', 98, 201, 'wordup', 3423],
                ['dog', 2, 3920, ' dsf', 2131],
                ['dog', 2, 3920, ' dsf', 2131],
                ['tacos', 99, 20, ' somdsf', 213123423],
                ['burger', 98, 201, 'wordup', 3423],
                ['tacos', 99, 20, ' somdsf', 213123423],
                ['burger', 98, 201, 'wordup', 3423],
                ['burger', 98, 201, 'wordup', 3424],
                ['tacos', 99, 20, ' somdsf', 213123423],
                ['burger', 98, 201, 'wordup', 3423],
                ['dog', 2, 3920, ' dsf', 2131],
                ['tacos', 99, 20, ' somdsf', 213123423],
                ['burger', 98, 201, 'wordup', 3423],
                ['dog', 2, 3920, ' dsf', 2131],
                ['dog', 2, 3920, ' dsf', 2131],
                ['tacos', 99, 20, ' somdsf', 213123423],
                ['burger', 98, 201, 'wordup', 3423],
                ['tacos', 99, 20, ' somdsf', 213123423],
                ['pen', 98, 201, 'wordup', 3424],
                ['end', 98, 201, 'wordup', 3424],
               ]
        return rows


    def get_first_rows(self):
        output = []
        if self.title:
            output.append(None)
        if self.headers:
            output.append([str(d).strip() for d in self.headers])
        return output

    def transform_rows_to_strings(self, data):
        output = []
        for row in data:
            output.append([str(d).strip() for d in row])
        return output

    def get_current_rows(self):

        #TODO Optimize this
        data_rows = []
        upper_lim = self.height
        if self.headers:
            upper_lim -= 1
        if self.title:
            upper_lim -= 1

        if len(self.row_data) < upper_lim:
            return self.transform_rows_to_strings(self.row_data)

        start_index = self.get_start_index()

        i = -1
        while i < upper_lim:
            i += 1
        #for i in range(upper_lim):
            ind = start_index + i
            data = self.get_row_data(ind)
            if data:
                data_rows.append([str(d).strip() if d is not None else '' for d in data])

        return data_rows

    def get_maxs(self, row_data):
        if self.headers:
            row_data.append(self.headers)
        maxs = []
        num_fields = max([len(r) for r in row_data])
        maxs = [1 for i in range(num_fields)]
        for i in range(num_fields):
            for row in row_data:
                if i < len(row):
                    length = len(str(row[i]).strip())
                    if length > maxs[i]:
                        maxs[i] = length
        log("Maxes: {}".format(maxs))
        return maxs

    def get_start_index(self):
        shift_amount = (self.height // 2)
        total_height = self.width
        if self.title:
            shift_amount -= 1
            total_height -= 1
        if self.headers:
            shift_amount -= 1
            total_height -= 1

        start_ind = self.current_index - (shift_amount + 1)
        if start_ind < 0:
            return 0

        end_location = start_ind + self.height
        num_rows = len(self.row_data)
        if end_location >= num_rows:
            return num_rows - (self.height - 2)
        return start_ind


    def make_str_row(self, maxs, row_data):
        if row_data is None:
            return ' ' * self.width
        line = ''
        bonus_data = self.width - sum(maxs) - (len(maxs) - 1)
        num_cols = len(maxs)

        bonuses = [0 for i in range(num_cols)]
        if bonus_data > 0:
            bonuses = [bonus_data // len(maxs) for i in range(num_cols)]
            for i in range((bonus_data % num_cols)):
                bonuses[i] += 1

        for i in range(len(maxs)):
            item = str(row_data[i]).strip()
            diff = maxs[i] - len(item)
            if diff > 0:
                line += ' ' * diff
            if bonuses[i] > 0:
                line += ' ' * bonuses[i]
            line += item
            if i != len(row_data) - 1:
                line += '|'
        return line

    def refresh(self, stdscr, force=False, seen_dict=None):
        initial_rows = self.get_first_rows()
        rows = self.get_current_rows()
        if not rows:
            super().refresh(stdscr, force=force, seen_dict=seen_dict)
            return
        if not seen_dict:
            seen_dict = {}

        maxs = self.get_maxs(rows)

        header_rows = [self.make_str_row(maxs, d) for d in initial_rows]

        header_ind = 1 if self.title else 0
        num_starters = len(header_rows)
        start_index = self.get_start_index()

        for i in range(self.height):
            mod = curses.A_UNDERLINE
            if i < num_starters:
                if i == header_ind:
                    mod = self.header_mod
                    str_row = header_rows[header_ind]
                    for j in range(self.width):
                        coords = (i, j)
                        if not seen_dict.get(coords, False):
                            self.update_value(i, j, str_row[j], mod)
                continue
            ind = start_index + i - num_starters

            if ind >= len(self.row_data):
                for j in range(self.width):
                    self.update_value(i, j, ' ', 0)
            else:
                row_data = self.get_row_data(ind)
                if not row_data and i == header_ind:
                    str_row = header_rows[header_ind]
                else:
                    str_row = self.make_str_row(maxs, row_data)
                if ind == self.current_index:
                    mod = self.selected_mod
                #str_row = str_rows[i]
                for j in range(self.width):
                    self.update_value(i, j, str_row[j], mod)

        super().refresh(stdscr, force=force, seen_dict=seen_dict)

    def set_current_index(self, new_index):
        if new_index > -1 and new_index < len(self.row_data):
            self.current_index = new_index

    def add_to_index(self, amount):
        self.set_current_index(self.current_index + amount)

    def move_index_down(self, amount=1):
        self.add_to_index(abs(amount))

    def move_index_up(self, amount=-1):
        self.add_to_index(-1 * abs(amount))

    def get_selected_record(self):
        return self.get_row_data(self.current_index)




