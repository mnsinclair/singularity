class Action:
    def __init__(self, name, taker, description, target=None):
        self.name = name  # The name of the action
        self.taker = taker  # The person initiating the action
        # A description of the action. Present tense, e.g. "does an action" OR "does an action to"
        self.description = description
        # The person who is the target of the action. If the action is not to a specific person, this will be None.
        self.target = target

    def __str__(self):
        if self.target:
            return f'{self.taker} {self.description} {self.target}'
        else:
            return f'{self.taker} {self.description}'

    def __repr__(self):
        return self.__str__()
