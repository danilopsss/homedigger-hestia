import logging
from argparse import ArgumentParser
from .arguments import args_list
from .argument_definer import ArgumentDefiner


logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


arg_parser = ArgumentParser(
    prog="hdhestia",
    description="""
        A simple command line tool that allows us to consume from
        any registered queue.
        The purpose of this tool Is only to perform the consumption
        and store the data according to It's parameteres and queue
        defined topic.
    """,
    epilog="Have fun!",
    add_help=True,
    allow_abbrev=True,
    exit_on_error=True,
)

for arg in args_list:
    arg_parser.add_argument(*arg.args, **arg.kwargs, action="store")

args = arg_parser.parse_args()

consumer = ArgumentDefiner(args=args)
consumer.start_broker_consumer()
