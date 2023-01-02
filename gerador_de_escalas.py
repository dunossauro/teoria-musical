from collections import deque

from rich.console import Console
from rich.table import Table
from typer import Argument, Option, run

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


class Scale:
    def __init__(self, notes, chords, tonic='C'):
        self.notes = Notes(notes, tonic).notes
        self._chords = chords

    @property
    def chords(self):
        result = []

        for note, degree in zip(self.notes, self._chords):
            note: str = note

            if degree.isupper():
                ...

            else:
                note = note + 'm'

            if '°' in degree:
                note = note + '°'

            result.append(note)

        return result



scales = {
    'major': {
        'notes': (0, 2, 4, 5, 7, 9, 11),
        'chords': ('I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii°'),
        'progressions': (
            ('I', 'IV', 'V'),
            ('ii', 'V', 'I'),
            ('I', 'V', 'vi', 'IV'),
            ('I', 'iii', 'IV')
        ),
    },
    'minor': {
        'notes': (0, 2, 3, 5, 7, 8, 10),
        'chords': ('i', 'ii°', 'III', 'iv', 'v', 'VI', 'VII'),
        'progressions': (
            ('i', 'iv', 'v'),
            ('i', 'VI', 'VII'),
            ('i', 'v', 'VI')
        )
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
    chords: bool = Option(False)
):
    _scale = scales[scale]
    table = create_table(scale, tonic, _scale['chords'])

    match tonic, chords:
        case 'all', False:
            for _tonic in NOTES:
                table.add_row(*Notes(_scale['notes'], _tonic).notes)

        case 'all', True:
            for _tonic in NOTES:
                table.add_row(
                    *Scale(_scale['notes'], _scale['chords'], _tonic).chords
                )

        case _, False:
            table.add_row(*Notes(_scale['notes'], tonic).notes)

        case _, True:
            table.add_row(*Scale(_scale['notes'], _scale['chords'], tonic).chords)


    console.print(table)
    from random import choice
    console.print(
        f'Tente: {choice(_scale["progressions"])}'
    )


run(main)
