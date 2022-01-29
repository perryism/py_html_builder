from .element import Element

class Div(Element):
    def __init__(self, cls):
        super().__init__("div", cls)

class Text:
    def __init__(self, txt):
        self.txt = txt

    def render(self):
        return self.txt

class H4(Element):
    def __init__(self, txt, cls=""):
        super().__init__("h4", cls)
        self.add(Text(txt))

class H2(Element):
    def __init__(self, txt, cls=""):
        super().__init__("h2", cls)
        self.add(Text(txt))

class Html(Element):
    def __init__(self):
        super().__init__("html")

class Head(Element):
    def __init__(self):
        super().__init__("head")

class Img(Element):
    def __init__(self, src, clr, **attr):
        super().__init__("img", **attr)
        self.attributes["src"] = src
