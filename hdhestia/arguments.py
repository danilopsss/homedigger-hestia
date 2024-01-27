"""
This module defines the arguments used in the application.
The arguments are tuples stored in a list.

Example:
- -b, --broker: The available broker to connect to. Must be one of ["rabbitmq", "kafka"].

NOTE: The sintax is the same of the ArgumentParser.add_argument method.
"""

from collections import namedtuple


ArgumentStruct = namedtuple("ArgumentStruct", ["args", "kwargs"])

args_list = [
    ArgumentStruct(
        ("-b", "--broker"),
        {
            "choices": ["rabbitmq", "kafka"],
            "required": True,
            "help": "The available broker to connect to.",
        },
    ),
    ArgumentStruct(
        ("-q", "--queue"),
        {
            "type": str,
            "required": False,
            "help": "Applicable only for RabbitMQ. The queue to connect to.",
        },
    ),
    ArgumentStruct(
        ("-t", "--topic"),
        {
            "type": str,
            "required": False,
            "help": "Applicable only for Kafka. The topic to connect to.",
        },
    ),
]
