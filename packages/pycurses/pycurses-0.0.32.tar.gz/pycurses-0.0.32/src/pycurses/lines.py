
import random
import math

def space_elements(list1, list2):
    result = []
    interval = len(list2) // (len(list1) + 1)
    if len(list2) == len(list1):
        for i in range(len(list1) + len(list2)):
            if i % 2:
                result.append(list1.pop(0))
            else:
                result.append(list2.pop(0))
        return result

    for i, el in enumerate(list2):
        result.append(el)
        if i % interval == interval - 1 and list1:
            result.append(list1.pop(0))
    return result

def split_into_even_chunks(chunks, amount):
    if chunks == 0:
        return [amount]
    output = [0 for i in range(chunks)]
    for i in range(amount):
        output[i % len(output)] += 1

    base = output[0]
    split_ind = 0

    if set(output) == {base}:
        return output

    while output[split_ind] == base:
        split_ind += 1

    larger_numbers = output[:split_ind]
    smaller_numbers = output[split_ind:]

    if len(larger_numbers) > len(smaller_numbers):
        elements = space_elements(smaller_numbers, larger_numbers)
        assert sum(elements) == amount
        return elements
    else:
        elements = space_elements(larger_numbers, smaller_numbers)
        assert sum(elements) == amount
        return elements

def identify_character(ver_diff, hor_diff):
    if ver_diff == 0:
        return '-'
    if hor_diff == 0:
        return '|'
    slope = ver_diff / hor_diff
    #if abs(slope) < 0.3:
    if abs(slope) < 0.5:
        return '-'

    if slope > 0:
        return '\\'
    else:
        return '/'

def draw_line(start, end, include_ends=False):

    output = []
    def put_letter(row, col, letter):
        output.append((row, col, letter))

    if start[1] > end[1]:
        tmp = end
        end = start
        start = tmp
    put_letter(start[0], start[1], 'S' if include_ends else 's')
    put_letter(end[0], end[1], 'E' if include_ends else 'e')

    if start[0] == end[0]:
        end_mod = 1 if include_ends else 0
        start_col = start[1] + 1
        end_col = end[1]
        if include_ends:
            start_col -= 1
            end_col += 1
        for col in range(start_col, end_col):
            put_letter(start[0], col, '-')
        return output
    if start[1] == end[1]:
        end_mod = 1 if include_ends else 0
        start_row = start[0] + 1
        end_row = end[0]
        if include_ends:
            start_row -= 1
            end_row += 1
        for row in range(start_row, end_row):
            put_letter(row, start[1], '|')
        return output

    hor_diff = end[1] - start[1]
    ver_diff = end[0] - start[0]
    char = identify_character(ver_diff, hor_diff)
    slope = ver_diff / hor_diff

    if abs(hor_diff) >= abs(ver_diff):
        chunks = split_into_even_chunks(abs(ver_diff), abs(hor_diff))
        row = start[0]
        col = start[1]
        row_add = 1
        if ver_diff < 0:
            row_add = -1

        for chunk_ind in range(abs(ver_diff)):
            chunk = chunks[chunk_ind]
            for i in range(chunk):
                tmpchar = char
                if char == '-' and i == chunk-1:
                    if slope > 0:
                        tmpchar = '_'
                    else:
                        tmpchar = '"'
                if char == '-' and i == 0:
                    if slope > 0:
                        tmpchar = '"'
                    else:
                        tmpchar = '_'
                put_letter(row, col, tmpchar)
                col += 1
            row += row_add
        put_letter(row, col, char)

    else:
        chunks = split_into_even_chunks(abs(hor_diff), abs(ver_diff))
        row = start[0]
        col = start[1]

        row_add = 1
        if ver_diff < 0:
            row_add = -1
        for chunk_ind in range(abs(hor_diff)):
            chunk = chunks[chunk_ind]
            for i in range(chunk):
                tmpchar = char
                put_letter(row, col, tmpchar)
                row += row_add
            col += 1
        put_letter(row, col, char)

    put_letter(start[0], start[1], 'S' if include_ends else 's')
    put_letter(end[0], end[1], 'E' if include_ends else 'e')
    return output

def draw_line_series(points, connect=False):
    output = []
    for ind in range(len(points) - 1):
        a = points[ind]
        b = points[ind+1]
        output.extend(draw_line(a, b))
    if connect:
        output.extend(draw_line(points[0], points[-1]))
    return output

