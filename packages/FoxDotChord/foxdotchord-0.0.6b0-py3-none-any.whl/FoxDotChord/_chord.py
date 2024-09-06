"""Chord module."""

import re
from collections.abc import Iterable
from itertools import chain
from typing import List, Union

try:
    from renardo_lib.Patterns import P, PGroup, Pattern
    from renardo_lib.Root import Note, Root
except ModuleNotFoundError:
    try:
        from FoxDot.lib.Patterns import P, PGroup, Pattern
        from FoxDot.lib.Root import Note, Root
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            '\n\tThe FoxDotChord package requires the renardo or FoxDot '
            'package to be installed.\n\tYou can install this with:\n'
            '\t$ pip install renardo  # https://renardo.org\n'
            '\tOR\n'
            '\t$ pip install FoxDot   # https://foxdot.org\n'
        ) from exc

from ._notes import from_chromatic

TNote = Union[int, float, None]


class ChordException(Exception):
    """Chord exception."""


class Chord(PGroup):
    """
    Musical chord to be manipulated by renardo or FoxDot.

    The chord class generates chords that can be used by renardo or FoxDot.

    Examples
    --------
    >>> Chord('C#7/9')
    Chord('C#7/9')

    TODO
    ----
    - [ ] Allow `Scale` that is not `chromatic` [WIP].
        - [X] chromatic
        - [X] major
        - [ ] majorPentatonic
        - [ ] minor
        - [ ] aeolian
        - [ ] minorPentatonic
        - [ ] mixolydian
        - [ ] melodicMinor
        - [ ] melodicMajor
        - [ ] harmonicMinor
        - [ ] harmonicMajor
        - [ ] justMajor
        - [ ] justMinor
        - [ ] dorian
        - [ ] dorian2
        - [ ] diminished
        - [ ] egyptian
        - [ ] yu
        - [ ] zhi
        - [ ] phrygian
        - [ ] prometheus
        - [ ] indian
        - [ ] locrian
        - [ ] locrianMajor
        - [ ] lydian
        - [ ] lydianMinor
        - [ ] custom
        - [ ] hungarianMinor
        - [ ] romanianMinor
        - [ ] chinese
        - [ ] wholeTone
        - [ ] halfWhole
        - [ ] wholeHalf
        - [ ] bebopMaj
        - [ ] bebopDorian
        - [ ] bebopDom
        - [ ] bebopMelMin
        - [ ] blues
        - [ ] minMaj
        - [ ] susb9
        - [ ] lydianAug
        - [ ] lydianDom
        - [ ] melMin5th
        - [ ] halfDim
        - [ ] altered
    - [ ] Adjust to `Root.default`.
    - [ ] Accept chords with inverted bass, like: **(E/G#, Dm7/C)**.
    """

    def __init__(self, chord: str):
        """Initialize a new chord."""
        if hasattr(chord, 'chord'):
            self.chord = chord.chord
        elif isinstance(chord, str) and hasattr(chord, 'strip'):
            self.chord: str = chord.strip()
        else:
            self.chord: str = f'undefined: <{type(chord)}>'

        super().__init__(self.notes)

    def __repr__(self):
        """Chord representation."""
        return f"Chord('{self.chord}')"

    __str__ = __repr__

    def true_copy(self, new_data=None):
        """Copy object."""
        new = self.__class__(self.chord)
        new.__dict__ = self.__dict__.copy()
        if new_data is not None:
            new.data = new_data
        return new

    def _get_note(self, pattern: str, tons: int) -> TNote:
        if not re.search(pattern, self.chord):
            return None

        if self.is_flat:
            tons -= 1
        if self.is_sharp:
            tons += 1
        return from_chromatic(self._tonic + tons)

    @property
    def tone(self) -> int:
        """Indicates whether the tone."""
        return Root.default

    @property
    def is_flat(self) -> bool:
        """
        Indicates whether the chord is flat.

        Examples
        --------
        >>> Chord('Cb').is_flat
        True
        >>> Chord('C#').is_flat
        False

        Returns
        -------
        bool:
            `True` if the chord is flat otherwise `False`.
        """
        return bool(re.search(r'[-b]', self.chord))

    @property
    def is_sharp(self) -> bool:
        """
        Indicates whether the chord is sharp.

        Examples
        --------
        >>> Chord('Cb').is_sharp
        False
        >>> Chord('C#').is_sharp
        True

        Returns
        -------
        bool:
            `True` if the chord is sharp otherwise `False`.
        """
        return bool(re.search(r'[+#]', self.chord))

    @property
    def is_dim(self) -> bool:
        """
        Indicates whether the chord is sharp.

        Examples
        --------
        >>> Chord('D').is_dim
        False
        >>> Chord('D⁰').is_dim
        True
        >>> Chord('D0').is_dim
        True
        >>> Chord('Do').is_dim
        True
        >>> Chord('DO').is_dim
        True
        >>> Chord('Ddim').is_dim
        True

        Returns
        -------
        bool:
            `True` if the chord is diminished otherwise `False`.
        """
        return bool(re.search(r'([⁰0oO]|dim)', self.chord))

    @property
    def is_sus(self) -> bool:
        """Indicates whether the chord is suspended.

        Examples
        --------
        >>> Chord('Eb').is_sus
        False
        >>> Chord('Ebsus').is_sus
        True
        >>> Chord('Ebsus4').is_sus
        True
        >>> Chord('Eb4').is_sus
        False
        >>> Chord('Eb3#').is_sus
        False

        Returns
        -------
        bool:
            `True` if the chord is suspended otherwise `False`.
        """
        return bool(re.search(r'(sus)', self.chord))

    @property
    def is_minor(self) -> Union[bool, None]:
        """Indicates if the chord is minor.

        Examples
        --------
        >>> Chord('E#').is_minor
        False
        >>> Chord('E#m').is_minor
        True
        >>> Chord('E#5').is_minor

        Returns
        -------
        bool:
            `True` if the chord is minor otherwise `False`.
        None:
            If it is a power chord there is no way to know if it is
            minor, because it doesn't have the III of the chord.
        """
        if self.is_power_chord:
            return None
        return bool(re.search(r'^[A-G][b#]?m', self.chord))

    @property
    def is_power_chord(self) -> bool:
        """
        Indicates if the chord is minor.

        Examples
        --------
        >>> Chord('E#').is_power_chord
        False

        >>> Chord('E#5').is_power_chord
        True

        Returns
        -------
        bool:
            `True` if it's a power chord otherwise `False`.

        """
        return bool(re.search(r'^([A-G][b#]?5)$', self.chord))

    @property
    def notes(self) -> List[int]:
        """
        Chord notes.

        Examples
        --------
        >>> Chord('C').notes
        [0, 2, 4]

        Returns
        -------
        list of int:
            List of notes
        """
        degrees = [
            self.tonic,
            self.supertonic,
            self.third,
            self.subdominant,
            self.dominant,
            self.submediant,
            self.maj,
            self.ninth,
            self.eleventh,
            self.thirteenth,
        ]
        return list(filter(lambda d: d is not None, degrees))

    @property
    def _tonic(self) -> int:
        if not (
            result := re.search(r'(^(?P<tone>[A-G]{1}[b#]?))', self.chord)
        ):
            raise ChordException(
                f'Tonic inválid: "{self.chord:.1}" from chord "{self.chord}"',
            )
        return Note(result.group('tone')) + self.tone

    @property
    def tonic(self) -> int:
        """Tonic I.

        Examples
        --------
        >>> Chord('C')
        Chord('C')
        """
        return from_chromatic(self._tonic)

    @property
    def supertonic(self) -> TNote:
        """Supertonic II."""
        if re.search(r'(sus)?2', self.chord):
            return from_chromatic(self._tonic + 2)
        return None

    @property
    def third(self) -> TNote:
        """Third III."""
        if self.is_power_chord or self.is_sus:
            return None

        if self.is_dim or self.is_minor:
            return from_chromatic(self._tonic + 3)
        return from_chromatic(self._tonic + 4)

    @property
    def subdominant(self) -> TNote:
        """Subdominant IV."""
        if (
            re.search(r'(sus)2', self.chord)
            or (
                not re.search(r'4', self.chord)
                and not re.search(r'(sus)(3[\+#]|4)?', self.chord)
            )
        ):
            return None
        return from_chromatic(self._tonic + 5)

    @property
    def dominant(self) -> TNote:
        """Dominant V."""
        if re.search(r'5[\+#]', self.chord):
            return from_chromatic(self._tonic + 8)
        if re.search(r'5[\-b]', self.chord) or self.is_dim:
            return from_chromatic(self._tonic + 6)
        return from_chromatic(self._tonic + 7)

    @property
    def submediant(self) -> TNote:
        """Submediant VI."""
        if re.search(r'6', self.chord):
            return from_chromatic(self._tonic + 9)
        return None

    @property
    def maj(self) -> TNote:
        """Maj VII."""
        if re.search(r'7(M|[Mm]aj)', self.chord):
            return from_chromatic(self._tonic + 11)
        if re.search(r'7', self.chord):
            return from_chromatic(self._tonic + 10)
        return None

    @property
    def ninth(self) -> TNote:
        """Ninth IX."""
        if re.search(r'9[\+\#]', self.chord):
            return from_chromatic(self._tonic + 15)
        if re.search(r'9[\-b]', self.chord):
            return from_chromatic(self._tonic + 13)
        if re.search(r'9', self.chord):
            return from_chromatic(self._tonic + 14)
        return None

    @property
    def eleventh(self) -> TNote:
        """Eleventh XI."""
        if re.search(r'11[\+#]', self.chord):
            return from_chromatic(self._tonic + 18)
        if re.search(r'11[\-b]', self.chord):
            return from_chromatic(self._tonic + 16)
        if re.search(r'11', self.chord):
            return from_chromatic(self._tonic + 17)
        return None

    @property
    def thirteenth(self) -> TNote:
        """Thirteenth XIII."""
        if re.search(r'13[\+#]', self.chord):
            return from_chromatic(self._tonic + 22)
        if re.search(r'13[\-b]', self.chord):
            return from_chromatic(self._tonic + 20)
        if re.search(r'13', self.chord):
            return from_chromatic(self._tonic + 21)
        return None


class __chords__:  # noqa: N801
    """
    Creates a harmonic progression based on a list of chords.

    Parameters
    ----------
    chords : str
        Many chords

    Examples
    --------
    >>> PChord['Am7', 'C(7/9)', 'F7Maj', 'G(4/9/13)']
    P[Chord('Am7'), Chord('C(7/9)'), Chord('F7Maj'), Chord('G(4/9/13)')]

    >>> PChord['Am7,C(7/9),F7Maj,G(4/9/13)']
    P[Chord('Am7'), Chord('C(7/9)'), Chord('F7Maj'), Chord('G(4/9/13)')]

    >>> PChord('Am7', 'C(7/9)', 'F7Maj', 'G(4/9/13)')
    P[Chord('Am7'), Chord('C(7/9)'), Chord('F7Maj'), Chord('G(4/9/13)')]

    >>> PChord('Am7,C(7/9),F7Maj,G(4/9/13)')
    P[Chord('Am7'), Chord('C(7/9)'), Chord('F7Maj'), Chord('G(4/9/13)')]

    Returns
    -------
    (Pattern[Chord]):
        A `Chord` pattern. For more details about the `Pattern` object see the
        [renardo documentation](https://renardo.org/learn/tutorial/06-legacy-foxdot-tutorial/#tutorial-4-using-patterns) or
        [FoxDot documentation](https://foxdot.org/docs/pattern-basics/)

    """

    def __new(self, chords: Union[str, list], *args: Iterable) -> Pattern:
        if isinstance(chords, str):
            chords = chords.split(',')

        chords = [Chord(chord.strip()) for chord in chain(chords, args)]
        return P[chords]

    __getitem__ = __call__ = __new


PChord = __chords__()
