from collections import deque

from rich.console import Console
from rich.table import Table
from typer import Argument, run

console = Console()
NOTES = 'C C# D D# E F F# G G# A A# B'.split()


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
    'major': {
        'notes': (0, 2, 4, 5, 7, 9, 11),
        'chords': ('I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii°')
    },
    'minor': {
        'notes': (0, 2, 3, 5, 7, 8, 10),
        'chords': ('i', 'ii°', 'III', 'iv', 'v', 'VI', 'VII'),
    }
}


def create_table(scale, tonic, chords):
    if tonic != 'all':
        table = Table(title=f'Escala {scale} de {tonic}', show_lines=True)
    else:
        table = Table(title=f'Escala {scale}', show_lines=True)

    for chord in chords:
        table.add_column(chord, justify='center')

    return table


def main(
        scale: str = Argument('major'),
        tonic: str = Argument('all'),
):
    _scale = scales[scale]
    table = create_table(scale, tonic, _scale['chords'])

    if tonic == 'all':
        for _tonic in NOTES:
            table.add_row(*Notes(_scale['notes'], _tonic).notes)
    else:
        table.add_row(*Notes(_scale['notes'], tonic).notes)

    console.print(table)


run(main)
