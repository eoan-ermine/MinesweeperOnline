class Group:
    def __init__(self, name: str):
        self._name = name
        self.objects: list = []

    @property
    def name(self) -> str:
        return self._name
    
    def add(self, obj):
        self.objects.append(obj)

    def draw(self, screen):
        for obj in self.objects:
            obj.draw(screen)

    def collidepoint(self, point):
        for obj in self.objects:
            if obj.rect.collidepoint(*point):
                return obj
        return None

    def invoke(self, method):
        for obj in self.objects:
            method(obj)

    def __iter__(self):
        return iter(self.objects)
