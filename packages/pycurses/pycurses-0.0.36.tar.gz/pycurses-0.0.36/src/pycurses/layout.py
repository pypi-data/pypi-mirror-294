
import curses
from pycurses.window import Window
from pycurses.utils.general import log

class Layout(Window):

    def __init__(self, horizontal=True, parent=None, colors=None, defaultchar='.', defaultattr=0):
        super().__init__(parent=parent, colors=colors, defaultchar=defaultchar, defaultattr=defaultattr)
        self.weights = []
        self.horizontal = horizontal

    def set_all_changed(self):
        for child in self.children:
            child.set_all_changed()

    def max_height(self):
        if not self.children:
            return None
        mx_heights = [v.max_height() for v in self.children if v.max_height()]
        if mx_heights:
            return min(mx_heights)
        return None

    def min_height(self):
        if not self.children:
            return None
        mn_heights = [v.min_height() for v in self.children if v.min_height()]
        if mn_heights:
            return max(mn_heights)
        return None

    def max_width(self):
        if not self.children:
            return None
        mx_widths = [v.max_width() for v in self.children if v.max_width()]
        if mx_widths:
            return min(mx_widths)
        return None

    def min_width(self):
        if not self.children:
            return None
        mn_widths = [v.min_width() for v in self.children if v.min_width()]
        if mn_widths:
            return max(mn_widths)
        return None

    def add_child(self, child:Window, **kwargs):
        super().add_child(child)
        if kwargs.get('weight', False):
            self.weights.append(int(kwargs['weight']))
        else:
            self.weights.append(1)
        self.resize(self.width, self.height)

    def get_real_weights(self, full_size):
        total_weight = sum(self.weights)
        if total_weight == 0:
            return []
        base_val = full_size // total_weight
        output_sizes = []
        for w in self.weights:
            output_sizes.append(w * base_val)

        total_size = sum(output_sizes)
        if total_size < full_size:
            diff = full_size - total_size
            for i in range(diff):
                output_sizes[i % len(output_sizes)] += 1

        return output_sizes

    def remove_child(self, child):
        child_index = self.children.index(child)
        super().remove_child(child)

    def get_changed(self):
        changed = []
        for child in self.children:
            changed = changed + child.get_changed()
        return changed

    def resize(self, width, height):
        old_width = self.width
        old_height = self.height
        new_width = width
        new_height = height

        max_vals = new_width if self.horizontal else new_height

        super().resize(new_width, new_height)
        sizes = self.get_real_weights(max_vals)
        if not self.children:
            return

        if len(self.children) == 1:
            self.children[0].resize(new_width, new_height)
            self.set_all_changed()
            return

        if self.horizontal:
            maxes = [x.max_width() for x in self.children]
            mins = [x.min_width() for x in self.children]
        else:
            maxes = [x.max_height() for x in self.children]
            mins = [x.min_height() for x in self.children]

        mv = new_width if self.horizontal else new_height

        t = False
        if self.name == 'Right Layout':
            t = True

        def Log(x):
            if t:
                log(x)


        Log("-"*40)
        raw_sizes = sizes
        fixeds = []
        Log("Sizes Begin: {}".format(sizes))
        if self.horizontal:
            for i in range(len(sizes)):
                size = sizes[i]
                child = self.children[i]
                max_w = child.max_width()
                min_w = child.min_width()
                if min_w and size < min_w:
                    sizes[i] = min_w
                    fixeds.append(i)
                if max_w and size > max_w:
                    sizes[i] = max_w
                    fixeds.append(i)

        else:
            for i in range(len(sizes)):
                size = sizes[i]
                child = self.children[i]
                max_h = child.max_height()
                min_h = child.min_height()
                if min_h and size < min_h:
                    Log("Too Big")
                    sizes[i] = min_h
                    fixeds.append(i)
                if max_h and size > max_h:
                    Log("Too Big")
                    sizes[i] = max_h
                    fixeds.append(i)
        Log("Sizes End: {}".format(sizes))

        total_size = sum(sizes)
        max_val = new_height
        if self.horizontal:
            max_val = new_width
        diff = max_val - total_size

        if diff > 0:
            i = -1
            while sum(sizes) < max_val:
                i += 1
                mod = i % len(sizes)
                if mod in fixeds:
                    if i > 100:
                        break
                    continue
                else:
                    sizes[mod] += 1

        elif diff < 0:
            i = -1
            while sum(sizes) > max_val:
                i += 1
                mod = i % len(sizes)
                if mod in fixeds:
                    if i > 100:
                        break
                    continue
                else:
                    sizes[mod] -= 1

        Log("Sizes Before Draw: {}".format(sizes))

        current_val = 0
        if self.horizontal:
            for i in range(len(self.children)):
                size = sizes[i]
                child = self.children[i]
                child.resize(size, new_height)
                child.set_pos(current_val, 0)
                current_val += size
        else:
            for i in range(len(self.children)):
                size = sizes[i]
                child = self.children[i]
                child.resize(new_width, size)
                child.set_pos(0, current_val)
                current_val += size

        self.set_all_changed()






