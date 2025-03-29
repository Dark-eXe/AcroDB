class ChatCache():
    """Class for caching... <translation_response>: <exec_result>"""
    def __init__(self):
        self.cache_sequence = []
        self.cache_response = {}
        self.CACHE_LIMIT = 10

    def addPair(self, response: str, result: any) -> None:
        if len(self.cache_sequence) >= self.CACHE_LIMIT:
            del self.cache_response[self.cache_sequence.pop(0)]
        self.cache_sequence.append(response)
        self.cache_response[response] = result