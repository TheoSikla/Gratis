class Vertex:
    """Creates a Vertex object that has a name."""

    def __init__(self, name):
        """
        :param name: The name of the vertex object
        """
        self.name = str(name)

    def __str__(self):
        return self.name
