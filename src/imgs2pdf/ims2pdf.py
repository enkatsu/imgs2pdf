import itertools
import os
import sys
from pathlib import Path

import click
from reportlab.lib import pagesizes
from reportlab.pdfgen import canvas

ARG_SIZE_ERROR_MSG = 'The -size option accepts paper sizes such as A4 and B3, or comma-separated data such as 640,480.'


class Spinner:
    def __init__(self):
        self.bars = itertools.cycle(['-', '/', '|', '\\'])
        self.dots1 = itertools.cycle(['⣷', '⣯', '⣟', '⡿', '⢿', '⣻', '⣽', '⣾'])
        self.dots2 = itertools.cycle(['⣷⣿', '⣿⣾', '⣿⣷', '⣿⣯', '⣿⣟', '⣿⡿', '⣿⢿', '⡿⣿', '⢿⣿', '⣻⣿', '⣽⣿', '⣾⣿'])

    def next_bar(self):
        return next(self.bars)

    def next_dots1(self):
        return next(self.dots1)

    def next_dots2(self):
        return next(self.dots2)


def size_option2tuple(size):
    """
    Convert --size option string to tuple.
    :param size: A4, B3 and 640,480.
    :type size: str
    :return: Paper size tuple.
    :rtype: tuple
    """
    s = size.split(',')
    if len(s) == 2:
        return s
    elif len(s) == 1:
        papersize = s[0]
        if papersize in dir(pagesizes):
            return pagesizes.landscape(eval(f'pagesizes.{papersize}'))
        raise click.BadParameter(ARG_SIZE_ERROR_MSG)
    else:
        raise click.BadParameter(ARG_SIZE_ERROR_MSG)


def init_canvas(src, papersize, title, author, subject):
    """
    Initialize canvas.Canvas.
    :param pdf: Source canvas.Canvas.
    :type pdf: canvas.Canvas
    :param papersize: Paper size.
    :type papersize: tuple
    :param title: PDF title.
    :type title: str
    :param author: PDF author.
    :type author: str
    :param subject: PDF subject.
    :type subject: str
    :return: Initialized canvas.
    :rtype: canvas.Canvas
    """
    src.setPageSize(papersize)
    src.setAuthor(author)
    src.setTitle(title)
    src.setSubject(subject)
    return src


@click.command()
@click.option('--in', '-i', 'input_path', default='./', help='Path of the directory containing the image.')
@click.option('--out', '-o', 'output_path', default='out.pdf', help='Name of PDF to output.')
@click.option('--extension', '-e', default='png', help='Image file extension.')
@click.option('--papersize', '-p', default='A4', help='Paper size, e.g. A4, B3 and 640,480.')
@click.option('--title', '-t', default='No title', help='Name of document.')
@click.option('--author', '-a', default='', help='Author of the document.')
@click.option('--subject', '-s', default='', help='The subject of the document.')
def export(input_path, output_path, extension, papersize, title, author, subject):
    """
    :param input_path: Path of the directory containing the image.
    :type input_path: str
    :param output_path: Name of PDF to output.
    :type output_path: str
    :param extension: Image file extension.
    :type extension: str
    :param papersize: Paper size, e.g. A4, B3 and 640,480.
    :type papersize: str
    :param title: Name of document.
    :type title: str
    :param author: Author of the document.
    :type author: str
    :param subject: The subject of the document.
    :type subject: str
    :return: None
    :rtype None
    """
    papersize = size_option2tuple(papersize)
    output_path = os.path.join(input_path, output_path) if output_path == 'out.pdf' else output_path
    pattern = f'*.{extension}'
    pl = Path(input_path).glob(pattern)
    pdf = canvas.Canvas(output_path)
    pdf = init_canvas(pdf, papersize, title, author, subject)
    print(f'target:  {input_path}')
    spiner = Spinner()
    for i, p in enumerate(sorted(pl)):
        image_filename = str(p)
        # print(f'\rcurrent: {image_filename}', end='')
        print(f'\r{spiner.next_dots1()}  {image_filename}', end='')
        image_offset_x = 0
        image_offset_y = 0
        pdf.drawImage(
            image_filename,
            0 + image_offset_x, 0 + image_offset_y,
            width=papersize[0], height=papersize[1],
            preserveAspectRatio=True, anchor='c'
        )
        pdf.showPage()
    print(f'\noutput:  {output_path}')
    pdf.save()


if __name__ == '__main__':
    export()
