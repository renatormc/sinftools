import win32com.client as win32

alignments = {
    'center': 1,
    'right': 2,
    'distribute': 4,
    'justify': 3,
    'justify-hi': 7,
    'justify-low': 8,
    'justify-med': 5,
    'left': 0,
    'thai-justify': 9
}


class FontWeight:
    @staticmethod
    def bold(range):
        range.Font.Bold = True

    @staticmethod
    def italic(range):
        range.Font.Italic = True

    @staticmethod
    def underline(range):
        range.Font.Underline = True

    @staticmethod
    def clear(range):
        range.Font.Bold = False
        range.Font.Italic = False
        range.Font.Underline = False


def alignment(range, el):
    if el.tag == 'table':
        range.Rows.Alignment = alignments[el.attrib['alignment']]
    else:
        range.Paragraphs.Alignment = alignments[el.attrib['alignment']]


def font_name(range, name):
    range.Font.Name = name


def font_size(range, size):
    range.Font.Size = int(size)


def font_color(range, hex_color):
    # inverter azul e vermelho
    hex_color = "{}{}{}".format(hex_color[4:], hex_color[2:4], hex_color[:2])
    range.Font.TextColor.RGB = int(hex_color, 16)
