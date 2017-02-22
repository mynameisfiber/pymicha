# PyMicha: Things Micha Uses

> I reuse a lot of scripts... here's a simple way to have them all in one place
> -Micha

## Install

To make things more portable, external dependencies are only installed if the
corresponding extra is sent in. Currently supported extras are:

- `keras`: Tools for keras
- `plot`: Plotting Tools
- `prob_ds`: Probabilistic Datastructures
- `extra`: Extra external installs that I find useful
- `full`: All the above

The full install can be done with:

```
$ pip3.5 install -e git+https://github.com/mynameisfiber/pymicha.git#egg=pymicha[full]
```
