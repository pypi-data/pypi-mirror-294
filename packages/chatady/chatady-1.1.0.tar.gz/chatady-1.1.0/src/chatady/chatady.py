import requests
import json

class ChatADy:
    def __init__(self, publisher_id, key, options=None):
        if options is None:
            options = {}
        self.publisher_id = publisher_id
        self.key = key
        self.options = {'environment': 'production', 'noDelay': True, 'timeout': 1000}
        self.options.update(options)
        self.hostname = 'backend.chatady.com'
        self.port = 443
        self.prepath = '/api/v1'

    def get_contents(self, chat_id, options=None):
        if options is None:
            options = {'humansex': None, 'botsex': None}
        query = '?'
        if options.get('humansex'):
            query += f"humansex={options['humansex']}&"
        if options.get('botsex'):
            query += f"botsex={options['botsex']}"

        path = f"{self.prepath}/{'contents' if self.options['environment'] == 'production' else 'test-contents'}/{self.publisher_id}/{chat_id}{query}"
        url = f"https://{self.hostname}:{self.port}{path}"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': self.key
        }
        response = requests.get(url, headers=headers, timeout=self.options['timeout'])
        return response.text

    def new_chat(self, chat_id, entry, human, content=None):
        post_data = json.dumps({'human': human, 'entry': entry, 'content': content})
        path = f"{self.prepath}/{'chats' if self.options['environment'] == 'production' else 'test-chats'}/{self.publisher_id}/{chat_id}"
        url = f"https://{self.hostname}:{self.port}{path}"
        headers = {
            'Content-Type': 'application/json',
            'Content-Length': str(len(post_data)),
            'Authorization': self.key
        }
        response = requests.post(url, headers=headers, data=post_data, timeout=self.options['timeout'])
        return response.text