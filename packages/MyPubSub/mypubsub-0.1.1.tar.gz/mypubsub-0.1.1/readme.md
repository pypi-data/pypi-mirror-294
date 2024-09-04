# MyPubSub

MyPubSub is a Python library implementing the publish-subscribe pattern. It provides a simple and effective way to manage event-driven communication between different parts of an application. This project also demonstrates the use of the Singleton pattern to ensure that only one instance of the PubSub system exists.

## Features

- **Publish-Subscribe Pattern**: Facilitate event-based communication where publishers send messages and subscribers receive them.
- **Singleton Pattern**: Ensures only a single instance of the PubSub system exists throughout the application.
- **Flexible Event Management**: Allows for dynamic subscription and unsubscription of events.

## Installation

To use the MyPubSub library, you need to install the required dependencies. You can install them using `pip`:

```bash
pip install .
```

## Dependencies

- Python 3.8 or higher
- `pylint` (for code quality checks)
- `pytest` (for testing)

## Usage

Here’s a basic example of using the MyPubSub class:

```python
from mypubsub import MyPubSub

# Get the singleton instance of MyPubSub
pubsub = MyPubSub.get_instance()

# Define a callback function for subscribers
def handle_message(message):
    print(f"Received message: {message}")

# Subscribe to an event
pubsub.subscribe('event_topic', handle_message)

# Publish a message to the event
pubsub.publish('event_topic', 'Hello, World!')

# Unsubscribe from the event
pubsub.unsubscribe('event_topic', handle_message)

# Reset the singleton instance (useful for testing)
MyPubSub.reset_instance()
```


## Testing

To run tests, ensure pytest is installed:

```bash
pip install pytest
```

Then execute the tests with:

```bash
pytest
```

## Contributing

Contributions are welcome! To contribute, fork the repository, create a new branch, and submit a pull request. Ensure that your changes include appropriate tests.
