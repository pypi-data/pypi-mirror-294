# FoxDotChord

[![Documentation](https://img.shields.io/badge/docs-latest-1769AA?color=%234051b5)](https://foxdotchord.readthedocs.io)
[![License](https://img.shields.io/pypi/l/FoxDotChord?label=License&color=%234051b5)](https://spdx.org/licenses/)

[![Supported Python versions](https://img.shields.io/pypi/pyversions/FoxDotChord.svg?logo=python&label=Python&color=%2373DC8C)](https://pypi.python.org/pypi/FoxDotChord/)
[![PyPI version](https://img.shields.io/pypi/v/FoxDotChord.svg?logo=pypi&label=PyPI&color=%2373DC8C)](https://pypi.org/project/FoxDotChord/)
[![Downloads](https://img.shields.io/pypi/dm/FoxDotChord?logo=pypi&label=Downloads&color=%2373DC8C)](https://pypi.org/project/FoxDotChord/)

[![Issue Tracker](https://img.shields.io/badge/Issue-Tracker-1769AA?color=%234B78E6)](https://codeberg.org/taconi/FoxDotChord/issues)
[![Contributing](https://img.shields.io/badge/Contributing-welcome-1769AA?color=%234B78E6)](https://foxdotchord.readthedocs.io/contributing)
[![Built with Material for MkDocs](https://img.shields.io/badge/Material_for_MkDocs-526CFE?logo=MaterialForMkDocs&logoColor=white)](https://squidfunk.github.io/mkdocs-material/)

---

Chords for use in [renardo](https://renardo.org) or [FoxDot](https://foxdot.org).

## Instalation

Use the package manager you prefer

```sh
pip install FoxDotChord
```

## How to use?

```python
from FoxDotChord import PChord as c

c0 = c['C, Am7, Dm, Em']
t0 >> keys(
    c0.every(3, 'bubble'),
    dur=PDur(3, 8)
)

b0 >> sawbass(c0, amp=1, pan=[0, 1, -1, 0])

d0 >> play('x-o({-=}[--])')
```

```python
from FoxDotChord import PChord as c

Clock.bpm = 180

d1 >> play('(C(ES))   ')

har = c['F#6, Dm7/9, Bm5/7']
c1 >> swell(
    var(har, [4, 8, 4]),
    dur=PDur(5, 9)*2,
    oct=var([4, 5], 16),
    amp=1.5,
)

d2 >> play('pn u', amp=2)
```

## Contribute

See the [Contributor Guide](https://foxdotchord.readthedocs.io/contributing).
