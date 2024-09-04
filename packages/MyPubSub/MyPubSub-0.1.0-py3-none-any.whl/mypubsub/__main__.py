"""Main File
"""
from mypubsub import MyPubSub

def print_message(message: str) -> None:
    """Print Message

    Args:
        message (str): Incoming message
    """
    print(message)

def main() -> None:
    """Main Function
    """
    print("Called from main()")
    p = MyPubSub()
    p.subscribe('topic1', print_message)

if __name__ == "__main__":
    print("Called from __main__.py")
    main()
