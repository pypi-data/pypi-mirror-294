# cifkit

![Integration Tests](https://github.com/bobleesj/cifkit/actions/workflows/python-run-pytest.yml/badge.svg)
[![codecov](https://codecov.io/gh/bobleesj/cifkit/graph/badge.svg?token=AN2YAC337A)](https://codecov.io/gh/bobleesj/cifkit)
![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)
![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)
![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)
[![PyPi version](https://img.shields.io/pypi/v/cifkit.svg)](https://pypi.python.org/pypi/cifkit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/bobleesj/cifkit/blob/main/LICENSE)

<!-- Open Codelab with a new tab -->

[![Open Google Codelab](https://img.shields.io/badge/Google%20Colab-Open-blue.svg)](https://colab.research.google.com/drive/1mZLFWyYblc2gxRqjP7CejZcUNGbQBzwo#scrollTo=DlB6ZTVaOMpq)

The documentation is available here: https://bobleesj.github.io/cifkit

![Logo light mode](assets/img/logo-black.png#gh-light-mode-only "cifkit logo light")
![Logo dark mode](assets/img/logo-color.png#gh-dark-mode-only "cifkit logo dark")

`cifkit` is designed to provide a set of well-organized and fully-tested utility
functions for handling large datasets, on the order of tens of thousands, of
`.cif` files.

> The current codebase and documentation are actively being improved as of July
> 8, 2024.

## Motivation

In high-throughput analysis using `.cif` files, the research project has
identified the folowing needs:

- **Preprocess files at once:** `.cif` files parsed from databases often contain
  ill-formatted files. We need a tool to standardize, preprocess, and filter out
  bad files. We also need to copy, move, and sort `.cif` files based on specific
  attributes.

- **Visualize coordination geometry:** We are interested in determining the
  coordination geometry and the best site in the supercell for analysis in a
  high-throughput manner. We need to identify the best site for each site label.
- **Visualize distribution of files:** We want to easily identify and categorize
  a distribution of underlying `.cif` files based on supercell size, tags,
  coordination numbers, elements, etc.

## Quotes

Here is a quote illustrating how `cifkit` addresses one of the challenges
mentioned above.

> "I am building an X-Ray diffraction analysis (XRD) pattern visualization
> script for my lab using `pymatgen`. I feel like `cifkit` integrated really
> well into my existing stable of libraries, while surpassing some alternatives
> in preprocessing and parsing. For example, it was often unclear at what stage
> an error occurred—whether during pre-processing with `CifParser`, or XRD plot
> generation with `diffraction.core` in `pymatgen`. The pre-processing logic in
> `cifkit` was communicated clearly, both in documentation and in actual
> outputs, allowing me to catch errors in my data before it was used in my
> visualizations. I now use `cifkit` by default for processing CIFs before they
> pass through the rest of my pipeline." - Alex Vtorov

## Overview

Designed for individuals with minimal programming experience, `cifkit` provides
two primary objects: `Cif` and `CifEnsemble`.

### Cif

**`Cif`** is initialized with a `.cif` file path. It parses the `.cif` file,
generates supercells, and computes nearest neighbors. It also determines
coordination numbers using four different methods and generates polyhedrons for
each site.

```python
from cifkit import Cif
from cifkit import Example

# Initalize with the example file provided
cif = Cif(Example.Er10Co9In20_file_path)

# Print attributes
print("File name:", cif.file_name)
print("Formula:", cif.formula)
print("Unique element:", cif.unique_elements)
```

### CifEnsemble

**`CifEnsemble`** is initialized with a folder path containing `.cif` files. It
identifies unique attributes, such as space groups and elements, across the
`.cif` files, moves and copies files based on these attributes. It generates
histograms for all attributes.

```python
from cifkit import CifEnsemble
from cifkit import Example

# Initialize
ensemble = CifEnsemble(Example.ErCoIn_folder_path)

# Get unique attributes
ensemble.unique_formulas
ensemble.unique_structures
ensemble.unique_elements
ensemble.unique_space_group_names
ensemble.unique_space_group_numbers
ensemble.unique_tags
ensemble.minimum_distances
ensemble_test.supercell_atom_counts
```

## Tutorial and documentation

You may use example `.cif` files that can be easily imported, and you can visit
the documentation page [here](https://bobleesj.github.io/cifkit/).

## Installation

To install

```bash
pip install cifkit
```

You may need to download other dependencies:

```bash
pip install cifkit pyvista gemmi
```

`gemmi` is used for parsing `.cif` files. `pyvista` is used for plotting
polyhedrons.

Please check the `pyproject.toml` file for the full list of dependencies.

## Testing

To run test locally.

```python
# Install all dependencies in editable mode
pip install -e .

# Run test
pytest
```

## Visuals

### Polyhedron

You can visualize the polyhedron generated from each atomic site based on the
coordination number geometry. In our research, the goal is to map the structure
and coordination number with the physical property.

```python
from cifkit import Cif

# Example usage
cif = Cif("your_cif_file_path")
site_labels = cif.site_labels

# Loop through each site
for label in site_labels:
    # Dipslay each polyhedron, a file saved for each
    cif.plot_polyhedron(label, is_displayed=True)
```

![Polyhedron generation](assets/img/ErCoIn_polyhedron.png)

### Histograms

You can use `CifEnsemble` to visualize distributions of file counts based on
specific attributes, etc. Learn all features from the documentation provided
[here](https://bobleesj.github.io/cifkit/).

By formulas:

![Histogram](assets/img/histogram-formula.png)

By structures:

![Histogram](assets/img/histogram-structure.png)

## Open-source projects using cifkit

- CIF Bond Analyzer (CBA) - extract and visualize bonding patterns -
  [DOI](https://doi.org/10.1016/j.jallcom.2023.173241) |
  [GitHub](https://github.com/bobleesj/cif-bond-analyzer)
- CIF Cleaner - move, copy .cif files based on attributes -
  [GitHub](https://github.com/bobleesj/cif-cleaner)
- Structure Analyzer/Featurizer (SAF) - extract physics-based features from .cif
  files - [GitHub](https://github.com/bobleesj/structure-analyzer-featurizer)

## How to ask for help

`cifkit` is also designed for experimental materials scientists and chemists.

- If you have any issues or questions, please feel free to reach out or
  [leave an issue](https://github.com/bobleesj/cifkit/issues).

## How to contribute

Here is how you can contribute to the `cifkit` project if you found it helpful:

- Star the repository on GitHub and recommend it to your colleagues who might
  find `cifkit` helpful as well.
  [![Star GitHub repository](https://img.shields.io/github/stars/bobleesj/cifkit.svg?style=social)](https://github.com/bobleesj/cifkit/stargazers)
- Fork the repository and consider contributing changes via a pull request.
  [![Fork GitHub repository](https://img.shields.io/github/forks/bobleesj/cifkit?style=social)](https://github.com/bobleesj/cifkit/network/members)
- If you have any suggestions or need further clarification on how to use
  `cifkit`, please feel free to reach out to Sangjoon Bob Lee
  ([@bobleesj](https://github.com/bobleesj)).

## Contributors

`cifkit` has been greatly enhanced thanks to the contributions from a diverse
group of researchers:

- Anton Oliynyk: original ideation with `.cif` files
- Alex Vtorov: tool recommendation for polyhedron visualization
- Danila Shiryaev: testing as beta user
- Fabian Zills ([@PythonFZ](https://github.com/PythonFZ)): suggested tooling
  improvements
- Emil Jaffal ([@EmilJaffal](https://github.com/EmilJaffal)): initial testing
  and bug report
- Nikhil Kumar Barua: initial testing and bug report
- Nishant Yadav ([@sethisiddha1998](https://github.com/sethisiddha1998)):
  initial testing and bug report
- Siddha Sankalpa Sethi ([@runzsh](https://github.com/runzsh)): initial testing
  and bug report in initial testing and initial testing and bug report

We welcome all forms of contributions from the community. Your ideas and
improvements are valued and appreciated.

## Citation

Please consider citing `cifkit` if it has been useful for your research:

- cifkit – Python package for high-throughput .cif analysis,
  https://doi.org/10.5281/zenodo.12784259
