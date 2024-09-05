# ChatADy Package for Python

The `ChatADy` package is a Python wrapper for the ChatADy API, facilitating easy interaction with ChatADy's services from Python applications. It provides methods to retrieve contents and initiate new chats.

## Installation

To install ChatADy, run this command in your terminal:

```bash
pip install chatady
```

This is the preferred method to install ChatADy, as it will always install the most recent stable release.

If you don't have [pip](https://pip.pypa.io) installed, this [Python installation guide](http://docs.python-guide.org/en/latest/starting/installation/) can guide you through the process.

## Usage

To use the `ChatADy` package, you first need to import the `ChatADy` class from the package and then initialize it with your publisher ID and key.

### Quick Start

Here's a quick example to get you started:

```python
from chatady.chatady import ChatADy

# Initialize the ChatADy client
client = ChatADy('your_publisher_id', 'your_api_key')

# Send in messages
response = client.new_chat('unique_id_identifying_conversation', 'your_entry_message', 'boolean_human_or_bot')
print(response)

# Get ad contents
response = client.get_contents('unique_id_identifying_conversation')
print(response)
```

### Initializing the Client

To interact with the API, you need to create an instance of `ChatADy`:

```python
client = ChatADy('your_publisher_id', 'your_api_key')
```

You can also pass additional options as a dictionary to configure the client further:

```python
options = {'environment': 'production', 'noDelay': True, 'timeout': 1000}
client = ChatADy('your_publisher_id', 'your_api_key', options)
```

### Retrieving Ad Contents

To retrieve contents, use the `get_contents` method with the chat ID. You can also specify options for better targeting:

```python
response = client.get_contents('unique_id_identifying_conversation', {'humansex': 'male', 'botsex': 'female'})
print(response)
```

### Sending in a New Message

To start a new chat, use the `new_chat` method with the chat ID, entry message, and human identifier:

```python
response = client.new_chat('unique_id_identifying_conversation', 'Hello, ChatADy!', 'boolean_human_or_bot')
print(response)
```

## Support

For issues, questions, or contributions, please open an issue on the GitHub repository.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
