from .element import Element
from .common import Text, Div, H4

def to_camel_case(text):
    s = text.replace("-", " ").replace("_", " ")
    s = s.split()
    if len(text) == 0:
        return text
    return s[0] + ''.join(i.capitalize() for i in s[1:])

class FormControl(Element):
    def __init__(self, name):
        self.name = name


class Label(Element):
    def __init__(self, name):
        super().__init__("label", "form-label")
        self.children = [ Text(name) ]
        self.name = name

    def render(self):
        return f"""
<label for="{to_camel_case(self.name)}" class="form-label">{self.name}</label>
"""

class TextInput(FormControl):
    def render(self):
        return f"""
<input type="text" class="form-control" id="{to_camel_case(self.name)}" name="{to_camel_case(self.name)}" placeholder="" value="" required="">
""".strip()


class FormColBuilder:
    def __init__(self, width, n_col):
        self.n_col = n_col
        if self.n_col == 1:
            def cls_gen():
                yield f"col-{width}"
        elif self.n_col == 2:
            w = 6
            def cls_gen():
                for i in [w, w]:
                    yield f"col-sm-{i}"
        elif self.n_col == 3:
            def cls_gen():
                for i in [5,4,3]:
                    yield f"col-md-{i}"

        self.cls_gen = cls_gen()

    def build(self):
        return FormCol("div", next(self.cls_gen))

class FormCol(Element):
    @staticmethod
    def builder(children, width):
        n = len(children)
        return FormColBuilder(width, n)


class FormRow(Element):
    def __init__(self, width):
        super().__init__("div", "row")
        self.width = width

    def add(self, c, width=None):
        self.children.append(c)
        return self

    def render(self):
        form_col_builder = FormCol.builder(self.children, self.width)

        html = []
        for c in self.children:
            form_col = form_col_builder.build()
            if isinstance(c,  FormControl):
                form_col.add(Label(c.name))
            form_col.add(c)
            html.append(form_col.render())

        return "\n".join(html)


class Dropdown(FormControl):
    def __init__(self, name, options):
        super().__init__(name)
        self.options = options

    def render(self):
        select = Element("select", "form-select")
        for o in self.options:
            select.add(Element("option").add(Text(o)))

        return select.render()

class Button(Element):
    def __init__(self, text, cls):
        super().__init__("button", cls, type="submit")
        self.add(Text(text))


class Radio(Element):
    def __init__(self, name, checked=False, required=False):

        booleanize = lambda x: "true" if x else "false"
        #ID??
        super().__init__("input", "form-check-input", name=name, type="radio", checked=booleanize(checked), required=booleanize(required))

class RadioList:
    def __init__(self, name, options):
        self.name = name
        self.options = options

    def render(self):
        div = Div("my-2")
        div.add(H4(self.name))
        for o in self.options:
            form_check = Div("form-check")
            form_check.add(Label(to_camel_case(o)))
            form_check.add(Radio(to_camel_case(self.name)))
            div.add(form_check)

        return div.render()

import yaml
class Form(Element):
    def build_element(node):
        if node["type"] == "text":
            return TextInput(node["name"])
        elif node["type"] == "dropdown":
            return Dropdown(node["name"], node["options"])
        elif node["type"] == "hr":
            return Element("hr", "my-4")
        elif node["type"] == "button":
            return Button(node["text"], "w-100 btn btn-primary btn-lg")
        elif node["type"] == "radio":
            return RadioList(node["name"], node["options"])

    @classmethod
    def from_file(cls, file):
        with open(file, "r") as f:
            return cls.from_yaml(yaml.load(f.read()))

    @staticmethod
    def from_yaml(yaml):
        form = yaml["form"]
        container = Div("row g-5").add(Div(f"col-lg-{form['size']}"))
        f = Form()
        title = H4(form["title"], "mb-3")
        container.add(title).add(f)

        #g-3 is spacing between rows
        div = f.create("div", "row g-3")

        for row in form["rows"]:
            r = FormRow(form["width"])
            for c in row:
                r.add(Form.build_element(c))

            div.add(r)

        return container

    def __init__(self, action = "", method="GET"):
        super().__init__("form")
        self.attributes["method"] = "GET"
