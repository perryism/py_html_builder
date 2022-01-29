from dom import Element, Html, Head, Div

class BootstrapLink(Element):
    def __init__(self):
        super().__init__("link")
        self.attributes["href"] = "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"
        self.attributes["rel"] ="stylesheet"
        self.attributes["integrity"] ="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3"
        self.attributes["crossorigin"] = "anonymous"

class BootstrapTemplate:
    def __init__(self):
        #innerbody
        self.body = Element("main")
        self.outerbody = Element("body", "bg-light").add(Div("container").add(self.body))
        self.head = Head().add(BootstrapLink())

    def render(self):
        html = Html()
        html.add(self.head).add(self.outerbody)
        return html.render()
