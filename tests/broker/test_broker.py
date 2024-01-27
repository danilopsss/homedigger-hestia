from hdmailman import MailMan
from unittest.mock import patch


@patch("pika.adapters.blocking_connection.BlockingConnection")
@patch("pika.adapters.utils.connection_workflow.AMQPConnectionWorkflow._try_next_resolved_address")
@patch("pika.adapters.utils.selector_ioloop_adapter._AddressResolver._resolve")
def test_class_instantiation(one, _, conn):
    mailman = MailMan("rabbitmq")
    mailman.rabbitmq
    assert one.called
