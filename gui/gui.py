# gui.py
from browser import document, svg, timer
from core.core import Resource,Converter
import gui.hud as hud

class Node:
    radius = 20

    def __init__(self, converter, pos):
        self.converter = converter
        self.position = pos
        self.circle = svg.circle(cx=0, cy=0, r=self.radius,stroke="black",stroke_width="2",fill="green")
        self.circle.attrs["id"] = self.converter.name
        self.title = svg.text(self.converter.name, x=0, y=-self.radius, z=10, font_size=15,text_anchor="middle")
        x,y = self.position
        self.circle.bind("click", self.clicked)
        self.circle.bind("contextmenu", self.right_clicked)
        self.circle.bind("mouseover", self.mouse_over)
        self.circle.bind("mouseout", self.mouse_out)
        self.connections = []
        self.hidden = True
        self.circle.attrs["visibility"] = "hidden"

    def clicked(self, event):
        hud.Hud.set_active(self)
        return False

    def right_clicked(self, event):
        if self.converter.is_stopped():
            self.converter.start()
        else:
            self.converter.stop()

    def mouse_over(self, event):
        hud.Hud.show_info(self)
        self.circle.attrs['stroke'] = 'orange'
        for line,node in self.connections:
            line.attrs['stroke'] = 'green'

    def mouse_out(self, event):
        hud.Hud.show_info(self)
        self.circle.attrs['stroke'] = 'black'
        for line,node in self.connections:
            line.attrs['stroke'] = 'black'

    def update(self):
        if self.hidden:
            self.hidden = self.converter.still_hidden()
            if self.hidden:
                return
        # self.converter.update()

    def draw(self):
        if not self.hidden:
            self.circle.attrs["visibility"] = "visible"
            # Update
            cx, cy = self.position
            self.circle.attrs["cx"] = cx
            self.circle.attrs["cy"] = cy
            self.title.attrs["x"] = cx
            self.title.attrs["y"] = cy
            self.position = cx, cy
            state = self.converter.state
            if state == Converter.OK:
                color = "green"
            elif state == Converter.STOPPED:
                color = "gray"
            elif state == Converter.NO_INPUT:
                color = "yellow"
            elif state == Converter.MAX_OUTPUT:
                color = "red"
            else:
                color = "blue" # error
            self.circle.attrs["fill"] = color

# Init nodes
nodes = []
panel = document['panel']
sX,sY=100,100
deltaY = 0
deltaX = 100
maxCol = 5
actCol = 0
X = sX
Y = sY
for conv in Converter.converters:
    node = Node(conv,(X,Y))
    nodes.append(node)
    X += deltaX
    actCol += 1
    Y += 20 # hack
    if actCol == maxCol:
        X = sX
        Y += deltaY
        actCol = 0


# Init connections
for node_out in nodes:
    for out_recipe in node_out.converter.makes:
        for node_in in nodes:
            for in_recipe in node_in.converter.needs:
                if out_recipe.resource == in_recipe.resource:
                    d="M 100 350 c 100 -200 200 500 300 0"
                    line = svg.path(d=d)
                    panel <= line
                    node_out.connections.append((line, node_in))

# Init node graphic
for node in nodes:
    panel <= node.circle
    panel <= node.title

# Init resource texts
resources=[]
Y = 20
for res in Resource.resources:
    text = svg.text(repr(res), x=hud.Hud.width-10, y=Y, font_size=20, text_anchor="end")
    panel <= text
    resources.append((res,text))
    Y += 25

# def panel_click(event):
#     hud.Hud.set_active(None)
#     print('panel')
#     return True

# panel.bind('click',panel_click)

def draw_connections():
    for node_out in nodes:
        for connect_out in node_out.connections:
            line, node_in = connect_out
            x1, y1 = map(int,node_out.position)
            x2, y2 = map(int,node_in.position)

            mx1,my1 = int((x1+x2)/2),int(y1)
            mx2,my2 = int((x1+x2)/2),int(y2)
            d = f'M {x1} {y1} C {mx1} {my1} {mx2} {my2} {x2} {y2}'

            line.attrs["d"] = d
            if node_out.converter.state == Converter.OK and not node_in.hidden:
                line.attrs["visibility"] = "visible"
            else:
                line.attrs["visibility"] = "hidden"


def draw_nodes():
    for node in nodes:
        node.update()
        node.draw()

def draw_resources():
    for res,text in resources:
        text.text = res


def drawing():
    draw_nodes()
    draw_connections()
    draw_resources()

# Init GUI
drawing()


