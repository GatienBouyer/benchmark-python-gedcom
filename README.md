# Benchmark of Python Gedcom parsers and traversers

Compare the efficiency of the data structure chosen by different Python packages.

Are measured:
- the parsing time of large gedcom file
- the time taken to find ascendants and descendants

## Packages tested

/!\ Conflict: **python-gedcom** and **gedcompy** both are under `import gedcom` /!\

- [fastgedcom](https://github.com/GatienBouyer/fastgedcom)
- [python-gedcom](https://github.com/joeyaurel/python-gedcom)
- [ged4py](https://github.com/andy-z/ged4py)
- [pygedcom](https://github.com/TOPetit/pygedcom)
- [gedcompy](https://github.com/amandasaurus/gedcompy)

## How to run benchmarks

- `python -m benchmarks.fastgedcom`
- `python -m benchmarks.python_gedcom`
- and so on...

The results are printed in stdout.

## Results

Results may vary between OS and Python versions.
