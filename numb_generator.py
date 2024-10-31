class increment_counter:

    def __init__(self):
        self._value = 0

    def new_value(self):
        self._value += 1
        return self._value
    def delete_value(self):
        if self._value > 0:
            self._value -= 1
        return self._value

    def get_value(self):
        return self._value

    def set_value(self,x):
        self._value = x
        return self._value