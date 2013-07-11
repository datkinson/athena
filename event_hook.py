#See http://stackoverflow.com/a/1094423/1969638
class event_hook:
    """Observer pattern
    
    Subscribe and unsubscribe to this object with += and -= respectively"""
    def __init__(self):
        self.__handlers = []

    def __iadd__(self, handler):
        self.__handlers.append(handler)
        return self

    def __isub__(self, handler):
        self.__handlers.remove(handler)
        return self

    def fire(self, *args, **keywargs):
        """Fire each event handler"""
        for handler in self.__handlers:
            handler(*args, **keywargs)

    def remove_all(self):
        """Remove all event handlers"""
        self.__handlers[:] = []
                