from argparse import ArgumentParser, Namespace

import pytest

from corider.config import Config, Configs, Strategy, namespace


def test_empty():
    parser = ArgumentParser(add_help=True)
    parser.add_argument("--dummy", default=42, type=int)

    c = Configs()

    new_parser = c.add_argparse_args(parser)

    assert parser.parse_known_args() == new_parser.parse_known_args()


def test_add():
    parser = ArgumentParser(add_help=True)
    parser.add_argument("--dummy", default=42, type=int)

    c = Configs()
    c.add(
        name="new_arg",
        type=str,
        default="the new black",
        strategy="constant",
        description="Just a test",
    )

    old_args = parser.parse_known_args()[0]

    c.add_argparse_args(parser)  # Mutates parser
    new_args = parser.parse_known_args()[0]

    assert old_args != new_args
    assert new_args == Namespace(dummy=42, new_arg="the new black")


def test_sub():
    c1 = Configs()
    c1.add("one", type=int, default=1)
    c1.add("two", type=int, default=2)

    c2 = Configs()
    c2.add("one", type=int, default=1)

    c3 = c1 - c2
    assert c3.names == ["two"]


def test_names():
    c = Configs()
    c.add(
        name="new_arg",
        type=str,
        default="the new black",
        strategy="constant",
        description="Just a test",
    )
    c.add(
        name="another",
        type=int,
        default=42,
        strategy="constant",
        description="Just a test",
    )
    assert c.names == ["new_arg", "another"]


def test__add__():
    c1 = Configs().add(
        name="one",
        type=int,
        default=1,
        strategy="constant",
        description="",
    )

    c2 = Configs().add(
        name="two",
        type=int,
        default=2,
        strategy="constant",
        description="",
    )

    # __add__
    c3 = c1 + c2
    assert c3.names == ["one", "two"]

    # __iadd__
    c4 = Configs()
    assert c4.names == []
    c4 += c1
    assert c4.names == ["one"]
    c4 += c2
    assert c4.names == ["one", "two"]

    # __radd__
    c5: Configs = sum([c1, c2])  # type: ignore
    assert c5.names == ["one", "two"]


def test_tune_config():
    c = Configs()
    c.add(
        name="one",
        type=int,
        default=1,
        strategy="constant",
        description="",
    )
    c.add(
        name="two",
        type=int,
        default=2,
        strategy="choice",
        description="",
        choices=[2, 20],
    )
    c.add(
        name="three",
        type=int,
        default=3,
        strategy="uniform",
        description="",
        choices=[3, 30],
    )
    c.add(
        name="four",
        type=int,
        default=4,
        strategy="loguniform",
        description="",
        choices=[4, 40],
    )

    with pytest.raises(ValueError):
        c.add(
            name="five",
            type=int,
            default=5,
            strategy="illegal",
            description="",
            choices=[5, 50],
        )

    tune_config = c.tune_config()

    assert "one" not in tune_config
    assert "two" in tune_config
    assert "three" in tune_config
    assert "four" in tune_config


def test_add_argparse_args():
    c = Configs()
    c.add(
        name="one",
        type=int,
        default=1,
        strategy="constant",
        description="",
    )
    c.add(
        name="two",
        type=int,
        default=2,
        strategy="choice",
        description="",
        choices=[2, 20],
    )
    c.add(
        name="three",
        type=int,
        default=3,
        strategy="uniform",
        description="",
        choices=[3, 30],
    )
    c.add(
        name="four",
        type=int,
        default=4,
        strategy="loguniform",
        description="",
        choices=[4, 40],
    )

    parser = c.add_argparse_args(ArgumentParser())
    args = parser.parse_known_args()[0]

    # All args are parsed
    assert args == Namespace(one=1, two=2, three=3, four=4)


def test_tune_add_argparse_args():
    c = Configs()
    c.add(
        name="one",
        type=int,
        default=1,
        strategy="constant",
        description="",
    )
    c.add(
        name="two",
        type=int,
        default=2,
        strategy="choice",
        description="",
        choices=[2, 20],
    )
    c.add(
        name="three",
        type=int,
        default=3,
        strategy="uniform",
        description="",
        choices=[3, 30],
    )
    c.add(
        name="four",
        type=int,
        default=4,
        strategy="loguniform",
        description="",
        choices=[4, 40],
    )

    parser = c.add_tune_argparse_args(ArgumentParser())
    args = parser.parse_known_args()[0]

    # Only configs which had Strategy != constant
    assert args == Namespace(one=1)


def test_from_argument_parse():
    parser = ArgumentParser(add_help=True)
    parser.add_argument(
        "--dummy", default=42, choices=[13, 42, 1337], type=int, help="Description"
    )

    c = Configs.from_argument_parser(parser)
    assert c.values == {
        "dummy": Config(
            name="dummy",
            alias=None,
            type=int,
            default=42,
            choices=[13, 42, 1337],
            strategy=Strategy.CONSTANT,
            description="Description",
        )
    }


def test_from_file():

    target = {
        "dropout": Config(
            name="dropout",
            alias=None,
            type=float,
            default=None,
            choices=[0.0, 0.1, 0.2, 0.3, 0.4],
            strategy=Strategy.CHOICE,
            description="",
        ),
        "learning_rate": Config(
            name="learning_rate",
            alias=None,
            type=float,
            default=None,
            choices=[0.01, 0.5],
            strategy=Strategy.LOGUNIFORM,
            description="",
        ),
        "weight_decay": Config(
            name="weight_decay",
            alias=None,
            type=float,
            default=None,
            choices=[1e-06, 0.001],
            strategy=Strategy.LOGUNIFORM,
            description="",
        ),
    }

    c_yaml = Configs.from_file("./tests/example_hparams_space.yaml")
    assert c_yaml.values == target

    c_json = Configs.from_file("./tests/example_hparams_space.json")
    assert c_json.values == target


def test_default_values():
    c = Configs()
    c.add(
        name="one",
        type=int,
        default=1,
        strategy="constant",
        description="",
    )
    c.add(
        name="two",
        type=int,
        default=2,
        strategy="choice",
        description="",
        choices=[2, 20],
    )
    c.add(
        name="three",
        type=int,
        default=3,
        strategy="uniform",
        description="",
        choices=[3, 30],
    )

    assert c.default_values() == namespace({"one": 1, "two": 2, "three": 3})
