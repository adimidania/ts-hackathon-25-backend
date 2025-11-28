
class ParentAlreadyExists(BaseException):
    """Raised when trying to register a parent that already exists."""
    def __init__(self, message="Parent with this email already exists"):
        self.message = message
        super().__init__(self.message)

class ParentNotFound(BaseException):
    """Raised when a parent with the given email does not exist."""
    def __init__(self, message="Parent with this email does not exist"):
        self.message = message
        super().__init__(self.message)

class IncorrectPassword(BaseException):
    """Raised when the provided password is incorrect."""
    def __init__(self, message="Incorrect password"):
        self.message = message
        super().__init__(self.message)
class StoryNotFound(BaseException):
    """Raised when a story with the given ID does not exist."""
    def __init__(self, message="Story with this ID does not exist"):
        self.message = message
        super().__init__(self.message)