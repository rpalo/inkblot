from collections import deque
import re


float_ = re.compile(r"^-?[0-9]+(\.[0-9]+)?$")
int_ = re.compile(r"^-?[0-9]+$")


class Lines(deque):
    def next_is_level(self, level):
        if not self:
            return False
        actual = len(self[0]) - len(self[0].lstrip())
        return level == actual

    def next_is_list(self):
        if not self:
            return False
        return self[0].lstrip().startswith("-")


def loads(text):
    lines = Lines(line.rstrip() for line in text.splitlines())
    return parse_dict(lines)


def is_int(text):
    return int_.match(text) is not None


def is_float(text):
    return float_.match(text) is not None


TAB_WIDTH = 2


def parse_dict(lines, level=0):
    result = dict()

    while lines and lines.next_is_level(level):
        line = lines.popleft().lstrip()
        if ":" not in line:
            raise ValueError(f"Malformed dict: {line}")

        key, _, value = line.partition(":")
        result[key] = parse_value(value.lstrip(), lines, level)

    return result

def parse_value(value, lines, level):
    if not value and lines.next_is_list():
        return parse_list(lines, level + TAB_WIDTH)
    if not value:
        return parse_dict(lines, level + TAB_WIDTH )
    if is_int(value):
        return int(value)
    if is_float(value):
        return float(value)
    return value.strip('"')


def parse_list(lines, level):
    result = []
    while lines.next_is_list() and lines.next_is_level(level):
        line = lines.popleft().strip("- ")
        if ":" in line:
            lines.appendleft(" " * (level + TAB_WIDTH) + line)
            result.append(parse_dict(lines, level + TAB_WIDTH))
        elif is_int(line):
            result.append(int(line))
        elif is_float(line):
            result.append(float(line))
        else:
            result.append(line.strip('"'))

    return result
