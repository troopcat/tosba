from sys import argv
from sys import exit as sysexit
import lark
from lark import Lark, Transformer
from time import sleep
import turtle

colordict = {
    "sarı": "yellow",
    "altın": "gold",
    "turuncu": "orange",
    "kırmızı": "red",
    "bordo": "maroon",
    "menekşe": "violet",
    "eflatun": "magenta",
    "mor": "purple",
    "lacivert": "navy",
    "mavi": "blue",
    "açık mavi": "skyblue",
    "camgöbeği": "cyan",
    "turkuaz": "turquoise",
    "açık yeşil": "lightgreen",
    "yeşil": "green",
    "koyu yeşil": "darkgreen",
    "çikolata": "chocolate",
    "kahverengi": "brown",
    "siyah": "black",
    "gri": "gray",
    "beyaz": "white"
}

lark.use_regex = True
parser = Lark.open("syntax.lark", start="start", parser="lalr")

def walk(t):
    global colordict
    
    if t.data == "end":
        sysexit(0)
        
    elif t.data == "movement":
        name, number = t.children
        {
            'ileri': turtle.fd,
            'geri': turtle.bk,
            'sağ': turtle.lt,
            'sol': turtle.rt,
        }[name](int(number))

    elif t.data == "change_color":
        colors = list()
        
        for color in t.children:
            colors.append(colordict[color.strip()])

        try:
            turtle.color(colors[0], colors[1])
        except IndexError:
            turtle.color(colors[0])

    elif t.data == "repeat":
        count, block = t.children
        for i in range(int(count)):
            walk(block)

    elif t.data == "fill":
        turtle.begin_fill()
        walk(t.children[0])
        turtle.end_fill()

    elif t.data == "code_block":
        for cmd in t.children:
            walk(cmd)
            
    elif t.data == "tsleep":
        sleep(int(t.children[0]))

    elif t.data == "backg":
        turtle.bgcolor(colordict[t.children[0].strip()])

    elif t.data == "tup":
        turtle.up()

    elif t.data == "tdown":
        turtle.down()

    elif t.data == "tspeed":
        turtle.speed(int(t.children[0]))

    elif t.data == "treset":
        turtle.reset()

    elif t.data == "sclear": # clear screen
        turtle.clearscreen()

    elif t.data == "tsize":
        turtle.pensize(int(t.children[0]))

    elif t.data == "stitle":
        turtle.title(t.children[0][1:-1])

    elif t.data == "sresize":
        turtle.setup(int(t.children[0]), int(t.children[1]))

    elif t.data == "comment":
        pass # nothing to do with comments

    elif t.data == "tshape":
        shape = {
            "ok": "arrow",
            "kare": "square",
            "çember": "circle",
            "üçgen": "triangle",
            "klasik": "classic"
        }[t.children[0].strip()]

        turtle.shape(shape)
    
    elif t.data == "ev":
        turtle.home()
    
    elif t.data == "git":
        turtle.goto(int(t.children[0]), int(t.children[1]))
    
    elif t.data == "tauto":
        turtle.resizemode("auto")
    
    elif t.data == "tcircle":
        turtle.circle(int(t.children[0]))
    
    elif t.data == "tstamp":
        turtle.stamp()
    
    elif t.data == "tclearstamps":
        turtle.clearstamps()


if __name__ == "__main__":
    with open(argv[1], "r", encoding="utf8") as f:
        tree = parser.parse(f.read())
        for inst in tree.children:
            walk(inst)
        
        turtle.mainloop()
