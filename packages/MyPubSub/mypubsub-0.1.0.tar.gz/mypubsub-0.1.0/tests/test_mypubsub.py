# test_pubsub.py
import pytest
from mypubsub import MyPubSub

@pytest.fixture
def mypubsub():
    """Fixture to create a PubSub instance."""
    return MyPubSub()

def test_subscribe_and_publish(mypubsub):
    messages = []

    def callback(msg):
        messages.append(msg)

    mypubsub.subscribe("test_topic", callback)
    mypubsub.publish("test_topic", "Hello, World!")

    assert len(messages) == 1
    assert messages[0] == "Hello, World!"

def test_unsubscribe(mypubsub):
    messages = []

    def callback(msg):
        messages.append(msg)

    mypubsub.subscribe("test_topic", callback)
    mypubsub.publish("test_topic", "Hello, World!")
    mypubsub.unsubscribe("test_topic", callback)
    mypubsub.publish("test_topic", "This should not be received")

    assert len(messages) == 1
    assert messages[0] == "Hello, World!"

def test_publish_no_subscribers(mypubsub):
    # Ensure publishing to a topic with no subscribers doesn't raise errors
    try:
        mypubsub.publish("non_existent_topic", "No subscribers here")
    except Exception as e:
        pytest.fail(f"Publish raised an exception unexpectedly: {e}")

def test_multiple_subscribers(mypubsub):
    messages_a = []
    messages_b = []

    def callback_a(msg):
        messages_a.append(msg)

    def callback_b(msg):
        messages_b.append(msg)

    mypubsub.subscribe("test_topic", callback_a)
    mypubsub.subscribe("test_topic", callback_b)
    mypubsub.publish("test_topic", "Message for both")

    assert len(messages_a) == 1
    assert messages_a[0] == "Message for both"
    assert len(messages_b) == 1
    assert messages_b[0] == "Message for both"
