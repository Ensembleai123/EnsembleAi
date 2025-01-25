
class Tool:
    def use(self, *args, **kwargs):
        raise NotImplementedError("Each tool must implement the 'use' method.")
