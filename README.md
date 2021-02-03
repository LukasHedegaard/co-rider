# Co-Rider
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/LukasHedegaard/co-rider/branch/main/graph/badge.svg?token=F15SVESDQZ)](https://codecov.io/gh/LukasHedegaard/co-rider)

Tiny configuration library tailored for Deep Learning project and the [Ride](https://github.com/LukasHedegaard/ride) library. 

```bash
pip install corider
```

## Organising configurations and arguments for Deep Learning projects
Keeping track of, merging and exposing configurations as arguments can be cumbersome and introduces a lot of boiler-plate code.
This tiny library aims to introduce a configuration structure, that will fit many Deep Learning projects.

A basic configuration is defined as follows:
```python
from corider import Configs

c1 = Configs()
c1.add(
    name="learning_rate",
    type=int,
    default=2,
    strategy="loguniform",
    description="Learning rate for optimizer",
    choices=(1e-8, 1),
)
c1.add(
    name="optimizer",
    type=str,
    default="sgd",
    strategy="constant",
    description="Optimizer to use.",
    choices=["sgd", "adam"],
)
```

## Argparse
_Co-Rider_ is fully compartible with `argparse` and can both load and dump argparse configurations:
```python
# argparse_example.py
from argparse import ArgumentParser
from corider import Configs

parser = ArgumentParser(add_help=True)
parser.add_argument(
    "--defined_with_argparse",
    default=42,
    choices=(42, 1337),
    type=int,
    help="Nonsensical parameter defined for demo purposes.",
)

c2 = Configs.from_argument_parser(parser)

c2.add(
    name="defined_with_corider",
    type=int,
    default="lit",
    description="Another parameter for demo purposes",
    choices=["lit", "woke"],
)

new_parser = c2.add_argparse_args(ArgumentParser(add_help=True))

args = new_parser.parse_args()

# Do somethin with the args
```

Use from shell as usual:
```bash
$ python argparse_example.py --help
usage: argparse_example.py [-h] [--defined_with_argparse {42,1337}]
                           [--defined_with_corider {lit,woke}]

optional arguments:
  -h, --help            show this help message and exit
  --defined_with_argparse {42,1337}
                        Nonsensical parameter defined for demo purpose.
                        (Default: 42)
  --defined_with_corider {lit,woke}
                        Another parameter for demo purpose (Default: lit)
```

## Ray Tune
By now you may have wodered about the `strategy` parameter. 
This parameter is intended for hyperparameter optimizers to indicate which sampling strategy to employ during hyperparameter search. 

Four strategies are available:
- `"constant"`: Parameter is not searchable and must be selected elsewhere, e.g. using `argparse`
- `"choice"`: Choose randomly from a list/set/tuple/range of parameters, e.g. `["lit", "woke"]`
- `"uniform"`: Pick values at random from an interval, e.g. `(0, 10)`
- `"loguniform"`: Pick values in a log uniform manner, e.g. `(1e-8, 1)`


For now, an automatic export to [Ray[Tune]](https://github.com/ray-project/ray) is included, which can be used as follows:
```python
from ray import tune

# Configs which had strategy "constant" can be added as argparse args
parser = c.add_tune_argparse_args(ArgumentParser())
args = parser.parse_args()

# Other parameters are exported in a Tune-compatible format
tune_config = c.tune_config()

# Run search
analysis = tune.run(
    your_training_function,
    config=tune_config,
    ... # Other tune.run parameters
)
```


## Argument addition and subtracktion
_Co-Rider_ can add and subtract configs as needed:
```python
c1 = ...  # As defined above (has: "learning_rate", "optimizer")

c2 = ...  # As defined above (has: "defined_with_argparse", "defined_with_corider")

c3 = Configs()
c3.add(
    name="learning_rate",  # Also defined in c1
    type=int,
    default=2,
    strategy="loguniform",
    description="Learning rate for optimizer",
    choices=(1e-8, 1),
)

# Has: "optimizer," "defined_with_argparse", "defined_with_corider"
c4 = c1 + c2 - c3  
```

## Load configuration from file
A configuration can be loaded from either `.yaml` or `.json` formatted files:
```yaml
# example_conf.yaml
dropout:
  type: float
  strategy: choice
  choices: [0.0, 0.1, 0.2, 0.3, 0.4]
learning_rate:
  type: float
  strategy: loguniform
  choices: [0.01, 0.5]
weight_decay:
  type: float
  strategy: loguniform
  choices: [0.000001, 0.001]
```

```python
c = Configs.from_file("example_conf.yaml")
```
