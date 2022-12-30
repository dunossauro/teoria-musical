from collections import deque

from rich.console import Console
from rich.table import Table
from typer import Argument, run

NOTES = 'C C# D D# E F F# G G# A A# B'.split()


class _Scale:
    def __init__(self, scale):
        self.scale = scale

    def __getitem__(self, pos):
        return self.scale[pos]


class _Notes:
    def __init__(self, scale, tonic):
        self.scale = scale
        self.tonic = tonic
        self._notes = self.build_scale()

    @property
    def notes(self):
        return tuple(self._notes[pos] for pos in self.scale)

    def build_scale(self):
        d = deque(NOTES)
        d.rotate(-NOTES.index(self.tonic))
        return tuple(d)


scales = {'major': _Scale((0, 2, 4, 5, 7, 9, 11, 0))}


def main(_tonic: str = Argument('all')):
    table = Table(title=f'Escala maior de {_tonic}', show_lines=True)

    table.add_column('Iº Tônica', justify='center')
    table.add_column('IIº - T', justify='center')
    table.add_column('IIIº - T', justify='center')
    table.add_column('IVº - ST', justify='center')
    table.add_column('Vº - T', justify='center')
    table.add_column('VIº - T', justify='center')
    table.add_column('VIIº - T', justify='center')
    table.add_column('Iº - T', justify='center')

    if _tonic == 'all':
        for tonic in NOTES:
            table.add_row(
                *_Notes(_Scale((0, 2, 4, 5, 7, 9, 11, 0)), tonic).notes
            )
    else:
        table.add_row(*_Notes(_Scale((0, 2, 4, 5, 7, 9, 11, 0)), _tonic).notes)

    console = Console()
    console.print(table)


run(main)
