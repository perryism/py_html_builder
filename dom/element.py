class Element:
    def __init__(self, tag, cls=[], **attrs):
        self.tag = tag
        self.attributes = attrs or {}

        if type(cls) is str:
           cls = [cls]
        self.attributes["class"] = cls
        self.children = []

    def render(self):
        return f"""
<{self.tag} {self.render_attributes()}>
{self.render_children()}
</{self.tag}>
""".strip()

    def add(self, c):
        self.children.append(c)
        return self

    def create(self, n, cls):
        e = Element(n, cls)
        self.add(e)
        return e

    def render_children(self):
        return "\n".join([ c.render() for c in self.children ])

    def render_attributes(self):
        parts = []
        for k, v in self.attributes.items():
            if type(v) is list:
                v = " ".join(v)
            parts.append(f"{k}=\"{v}\"")

        return " ".join(parts)
