class Profile:
    def __init__(self, name):
        self.name = name
        self.chat_history = []
        self.pre_chat_mood = None
        self.post_chat_mood = None

    def to_dict(self):
        return {
            'name': self.name,
            'chat_history': self.chat_history,
            'pre_chat_mood': self.pre_chat_mood,
            'post_chat_mood': self.post_chat_mood
        }