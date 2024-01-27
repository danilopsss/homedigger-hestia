from argparse import ArgumentParser
from hdhestia.arguments import args_list


def test_arguments():
    parser = ArgumentParser()
    for arg_struct in args_list:
        args, kwargs = arg_struct
        parser.add_argument(*args, **kwargs)

    assert len(parser._actions) - 1 == len(args_list)
