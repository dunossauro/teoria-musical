from collections import deque

from rich.console import Console
from rich.table import Table
from typer import Argument, run

console = Console()
NOTES = 'C C# D D# E F F# G G# A A# B'.split()


class Scale:
    def __init__(self, scale):
        self.scale = scale

    def __getitem__(self, pos):
        return self.scale[pos]


class Notes:
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


scales = {
    'major': Scale((0, 2, 4, 5, 7, 9, 11, 0)),
    'minor': Scale((0, 2, 3, 5, 7, 8, 10, 0)),
}


def create_table(scale, tonic):
    if tonic != 'all':
        table = Table(title=f'Escala {scale} de {tonic}', show_lines=True)
    else:
        table = Table(title=f'Escala {scale}', show_lines=True)

    table.add_column('Iº Tônica', justify='center')
    table.add_column('IIº - T', justify='center')
    table.add_column('IIIº - T', justify='center')
    table.add_column('IVº - ST', justify='center')
    table.add_column('Vº - T', justify='center')
    table.add_column('VIº - T', justify='center')
    table.add_column('VIIº - T', justify='center')
    table.add_column('Iº - T', justify='center')

    return table


def main(scale: str = Argument('major'), tonic: str = Argument('all')):
    table = create_table(scale, tonic)

    match scale, tonic:
        case 'major', 'all':
            _scale: Scale = scales['major']
            for _tonic in NOTES:
                table.add_row(*Notes(_scale, _tonic).notes)
        case 'minor', 'all':
            _scale: Scale = scales['minor']
            for _tonic in NOTES:
                table.add_row(*Notes(_scale, _tonic).notes)
        case _, _:
            table.add_row(*Notes(scales[scale], tonic).notes)

    console.print(table)


run(main)
