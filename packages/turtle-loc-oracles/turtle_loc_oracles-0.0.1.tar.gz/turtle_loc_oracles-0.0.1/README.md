# Turtle Locomotion Oracles

This Python package contains oracles of the movement of turtle limbs during locomotion (e.g., swimming /)
Some oracles are based on real-world observations of turtle locomotion, while others are based on theoretical/template models.

## Installation

Installation is very easy:

Either just clone the repository and install the package (in ediatble mode) using pip.

```bash
pip install -e .
```

or install the package directly from PyPI:

```bash
pip install turtle-loc-oracles
```

## Usage



## Provided Oracles

### Joint-space Oracles

#### Cornelia Turtle Robot Joint Space Trajectory

This oracle provides a joint-space trajectory developed for the Cornelia turtle robot by (van der Geest et al., 2023).
Please refer to the original paper for more information: https://doi.org/10.1038/s41598-023-37904-5

> van der Geest, N., Garcia, L., Borret, F., Nates, R., & Gonzalez, A. (2023).
Soft-robotic green sea turtle (Chelonia mydas) developed to replace animal experimentation provides new insight
into their propulsive strategies. Scientific Reports, 13(1), 11983.

and cite it if you use this oracle in your research.

```bibtex
@article{van2023soft,
  title={Soft-robotic green sea turtle (Chelonia mydas) developed to replace animal experimentation provides new insight into their propulsive strategies},
  author={van der Geest, Nick and Garcia, Lorenzo and Borret, Fraser and Nates, Roy and Gonzalez, Alberto},
  journal={Scientific Reports},
  volume={13},
  number={1},
  pages={11983},
  year={2023},
  publisher={Nature Publishing Group UK London}
}
```

### Task-space Oracles

#### Green Sea Turtle Swimming Task Space Trajectory

This oracle provides a task-space trajectory that was fitted to video recordings of the swimming of Green sea turtles (van der Geest et al., 2022).
Please refer to the original paper for more information: https://doi.org/10.1038/s41598-022-21459-y

> van der Geest, N., Garcia, L., Nates, R., & Godoy, D. A. (2022).
New insight into the swimming kinematics of wild Green sea turtles (Chelonia mydas).
Scientific Reports, 12(1), 18151.

and cite it if you use this oracle in your research.

```bibtex
@article{van2022new,
  title={New insight into the swimming kinematics of wild Green sea turtles (Chelonia mydas)},
  author={van der Geest, Nick and Garcia, Lorenzo and Nates, Roy and Godoy, Daniel A},
  journal={Scientific Reports},
  volume={12},
  number={1},
  pages={18151},
  year={2022},
  publisher={Nature Publishing Group UK London}
}
```
