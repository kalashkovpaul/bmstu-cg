# Лабораторная работа №2 по Компьютерной графике, Вариант 13
# Нарисовать исходную фигуру, затем осуществить её перенос, масштабирование 
# и поворот.
# Фигура: эпициклоида

from math import cos, radians, sin, pi
import tkinter as tk
import tkinter.messagebox as box
from tkinter import *
import copy
from turtle import right


# a subclass of Canvas for dealing with resizing of windows
class ResizingCanvas(Canvas):
    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)

class Dot(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return ("({}; {})".format(self.x, self.y))

class Line(object):
    def __init__(self, dot_1, dot_2):
        if dot_1.x == dot_2.x and dot_1.y == dot_2.y:
            return
        self.dot_1 = dot_1
        self.dot_2 = dot_2
        self.center = Dot((dot_1.x + dot_2.x) / 2, (dot_1.y + dot_2.y) / 2)
        self.A = dot_1.y - dot_2.y
        self.B = dot_2.x - dot_1.x
        self.C = dot_1.x * dot_2.y - dot_2.x * dot_1.y
        self.border_1 = dot_1
        self.border_2 = dot_2

    def print_info(self):
        print(str(self.A) + "x + " + str(self.B) + "y + " + str(self.C))

    def find_intersection(self, line):
        tmp = self.A * line.B - self.B * line.A
        if abs(tmp) >= 1e-7:
            x = (self.B * line.C - line.B * self.C) / tmp
            y = (self.C * line.A - self.A * line.C) / tmp
            return Dot(x, y)
        else:
            return None


    def find_borders(self):
        if self.A == 0:
            self.border_1 = Dot((-size[0] - 50) * scale[1], self.dot_1.y)
            self.border_2 = Dot((size[0] + 50) * scale[1], self.dot_1.y)
        elif self.B == 0:
            self.border_1 = Dot(self.dot_1.x, (size[1] + 50) * scale[1])
            self.border_2 = Dot(self.dot_1.x, (-size[1] - 50) * scale[1])
        else:
            self.border_1 = Dot((-size[0] - 50) * scale[1], (-self.C - self.A * (-size[0] - 50) * scale[1]) / self.B)
            self.border_2 = Dot((size[0] + 50) * scale[1], (-self.C - self.A * (size[0] + 50) * scale[1]) / self.B)

    def print_line(self):
        self.find_borders()
        x1 = int(self.border_1.x / scale[1]) + size[0] / 2
        y1 = (-1) * int(self.border_1.y / scale[1]) + size[1] / 2
        x2 = int(self.border_2.x / scale[1]) + size[0] / 2
        y2 = (-1) * int(self.border_2.y / scale[1]) + size[1] / 2
        canvas.create_line(x1, y1, x2, y2, fill='green', activewidth=3)

    def print_target(self):
        self.find_borders()
        x1 = int(self.border_1.x / scale[1]) + size[0] / 2
        y1 = (-1) * int(self.border_1.y / scale[1]) + size[1] / 2
        x2 = int(self.border_2.x / scale[1]) + size[0] / 2
        y2 = (-1) * int(self.border_2.y / scale[1]) + size[1] / 2
        canvas.create_line(x1, y1, x2, y2, fill='red', activewidth=3)
        
def find_middle(first, second):
    x = (first.x + second.x) / 2
    y = (first.y + second.y) / 2
    middle = Dot(x, y)
    return middle

def find_len(dot_1, dot_2):
    return ((dot_1.x - dot_2.x)**2 + (dot_1.y - dot_2.y)**2)**(1 / 2)

def draw_axes(scale, x0, y0):
    border = 60
    delta = 50
    x = 80
    real_x = x0
    real_delta = delta * scale
    smol = 10
    canvas.create_line(x, size[1] + border, size[0] + x, size[1] + border, width=3)
    while x < size[0] + border:
        canvas.create_line(x, size[1] + border - smol / 2, x, size[1] + border + smol / 2, width=3)
        canvas.create_text(x, size[1] + border + 1.5 * smol, text=f'{real_x:5.2f}')
        x += delta
        real_x += real_delta
    x = 80
    y = size[1] + border
    real_y = y0
    canvas.create_line(x, 0, x, size[1] + border, width=3)
    while y > 0:
        canvas.create_line(x - smol / 2, y, x + smol / 2, y, width=3)
        canvas.create_text(x - 4 * smol, y, text=f'{real_y:5.2f}')
        y -= delta
        real_y += real_delta

class Triangle(object):
    middle_ab = Dot(0, 0)
    middle_bc = Dot(0, 0)
    middle_ac = Dot(0, 0)
    median_middle = Dot(0, 0)
    square = 0

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.middle_ab = find_middle(a, b)
        self.middle_bc = find_middle(b, c)
        self.middle_ac = find_middle(a, c)
        ab = find_len(a, b)
        bc = find_len(b, c)
        ac = find_len(a, c)
        p = (ab + bc + ac) / 2
        self.square = (p * (p - ac) * (p - bc) * (p - ab)) ** (1 / 2)
        if abs(self.square) <= 1e-7:
            self.square = 0
            self.median_middle = Dot(0, 0)
        else:
            self.median_middle = Line(self.a, self.middle_bc).find_intersection(Line(self.b, self.middle_ac))

    def has(self, dot):
        return abs(self.square \
            - Triangle(self.a, self.b, dot).square \
                - Triangle(self.b, self.c, dot).square \
                    - Triangle(self.a, self.c, dot).square) < 1e-7

    def print_info(self):
        print(str(self.a) + ", " + str(self.b) + ", " + str(self.c))

            
    def draw(self, with_medians, with_dots):

        canvas.delete("all")
        max_x = max(self.a.x, self.b.x, self.c.x)
        min_x = min(self.a.x, self.b.x, self.c.x)
        max_y = max(self.a.y, self.b.y, self.c.y)
        min_y = min(self.a.y, self.b.y, self.c.y)
        delta_x = max_x - min_x
        delta_y = max_y - min_y
        scale = 1
        width = 4 * delta_x / 3
        height = 4 * delta_y / 3
        if width / height < size[0] / size[1]:
            scale = height / size[1]
        else:
            scale = width / size[0]
        
        width = scale * size[0]
        height = scale * size[1]
        print("Scale: {}".format(scale))
        x0 = min_x - width * 1 / 6
        y0 = min_y - height * 1 / 6
        draw_axes(scale, x0, y0)
        
        border = 60
        delta = 50
        x = 80
        real_x = x0
        real_delta = delta * scale
        smol = 10
        x0_im = x0 / scale
        y0_im = y0 / scale
        ax_im = self.a.x / scale - x0 / scale + x
        bx_im = self.b.x / scale - x0 / scale + x
        cx_im = self.c.x / scale - x0 / scale + x

        ay_im = size[1] + border - ((self.a.y - y0) / scale)
        by_im = size[1] + border - ((self.b.y  - y0) / scale)
        cy_im = size[1] + border - ((self.c.y - y0) / scale)

        canvas.create_polygon(ax_im, ay_im, bx_im, by_im, cx_im, cy_im, width=2, fill="white", outline="black")
        if with_medians:
            middle_ab_x_im = self.middle_ab.x / scale - x0 / scale + x
            middle_bc_x_im = self.middle_bc.x / scale - x0 / scale + x
            middle_ac_x_im = self.middle_ac.x / scale - x0 / scale + x

            middle_ab_y_im = size[1] + border - ((self.middle_ab.y - y0) / scale)
            middle_bc_y_im = size[1] + border - ((self.middle_bc.y - y0) / scale)
            middle_ac_y_im = size[1] + border - ((self.middle_ac.y - y0) / scale)
            
            canvas.create_line(middle_ab_x_im, middle_ab_y_im, cx_im, cy_im, width=2, fill="grey")
            canvas.create_line(middle_bc_x_im, middle_bc_y_im, ax_im, ay_im, width=2, fill="grey")
            canvas.create_line(middle_ac_x_im, middle_ac_y_im, bx_im, by_im, width=2, fill="grey")
        if with_dots:
            radius = 4
            for dot in dots:
                if self.has(dot):
                    x_im = dot.x / scale - x0 / scale + x
                    y_im = size[1] + border - ((dot.y - y0) / scale)
                    canvas.create_oval(x_im - radius, y_im - radius, x_im + radius, y_im + radius, fill="red")

def enter_shift():
    try:
        x, y = map(float, dots_entry.get().split())
        global drawing_old, drawing, scale_old, scale, rect, rect_old, lines, lines_old
        rect_old = copy.deepcopy(rect)
        scale_old = copy.deepcopy(scale)
        drawing_old = copy.deepcopy(drawing)
        lines_old = copy.deepcopy(lines)
        for dot in drawing:
            dot.x += x
            dot.y += y
        for dot in rect:
            dot.x += x
            dot.y += y
        for line in lines:
            for dot in line:
                dot.x += x
                dot.y += y
        
        # dots_entry.delete(0, last='end')
        find_and_build()
    except ValueError:
        # dots_entry.delete(0, last='end')
        box.showwarning("Ошибка ввода", "Вы ввели неверные значения смещения. Координаты точек\
         - вещественные числа, введённые через пробел")

def scale_canvas():
    try:
        global drawing_old, drawing, scale_old, scale, rect, rect_old, lines, lines_old
        x, y, sc_x, sc_y = list(map(float, scale_entry.get().split()))   
        rect_old = copy.deepcopy(rect)
        scale_old = copy.deepcopy(scale)
        drawing_old = copy.deepcopy(drawing)
        lines_old = copy.deepcopy(lines)
        for dot in drawing:
            dot.x = sc_x * dot.x + (1 - sc_x) * x
            dot.y = sc_y * dot.y + (1 - sc_y) * y 
        for dot in rect:
            dot.x = sc_x * dot.x + (1 - sc_x) * x
            dot.y = sc_y * dot.y + (1 - sc_y) * y 
        for line in lines:
            for dot in line:
                dot.x = sc_x * dot.x + (1 - sc_x) * x
                dot.y = sc_y * dot.y + (1 - sc_y) * y 

        # scale_entry.delete(0, last='end')
        find_and_build()
    except ValueError:
        # scale_entry.delete(0, last='end')
        box.showwarning("Ошибка ввода", "Вы ввели неверные параметры масштабирования (должны быть действительные числа через пробел)")

def rotate():
    try:
        global drawing_old, drawing, scale_old, scale, lines, lines_old
        x, y, angle = map(float, rotate_entry.get().split())
        rect_old = copy.deepcopy(rect)
        scale_old = copy.deepcopy(scale)
        drawing_old = copy.deepcopy(drawing)
        lines_old = copy.deepcopy(lines)
        angle = radians(angle)
        for i in range(len(drawing)):
            x_old = drawing[i].x
            y_old = drawing[i].y
            drawing[i].x = x + (x_old - x) * cos(angle) + (y_old - y) * sin(angle)
            drawing[i].y = y - (x_old - x) * sin(angle) + (y_old - y) * cos(angle)
        for i in range(len(rect)):
            x_old = rect[i].x
            y_old = rect[i].y
            rect[i].x = x + (x_old - x) * cos(angle) + (y_old - y) * sin(angle)
            rect[i].y = y - (x_old - x) * sin(angle) + (y_old - y) * cos(angle)
        for line in lines:
            for i in range(len(line)):
                x_old = line[i].x
                y_old = line[i].y
                line[i].x = x + (x_old - x) * cos(angle) + (y_old - y) * sin(angle)
                line[i].y = y - (x_old - x) * sin(angle) + (y_old - y) * cos(angle)
        find_and_build()
    except ValueError:
        # rotate_entry.delete(0, last='end')
        box.showwarning("Ошибка ввода", "Кооординаты и угол - действительные числа, ввод через пробел")

def glob_scale():
    try:
        global scale, scale_old
        new_scale = float(glob_scale_entry.get())
        if new_scale <= 0:
            raise ValueError
        scale_old = scale
        scale /= new_scale
        # glob_scale_entry.delete(0, last='end')
        find_and_build()
    except ValueError:
        # glob_scale_entry.delete(0, last='end')
        box.showwarning("Ошибка ввода", "Во сколько раз хотите увеличить - действительное положительное число")

def refill():
    fill_drawing()
    find_and_build()

def enter_dot_event(event):
    enter_shift()

def glob_scale_event(event):
    glob_scale()

def del_dots():
    dots.clear()
    # dots_entry.delete(0, last='end')
    # dots_listbox.delete(0, dots_listbox.size())

def scale_canvas_event(event):
    scale_canvas()

def rotate_event(event):
    rotate()

def is_parallel(line_1, line_2):
    if line_1.A == 0 and line_2.A == 0 or line_1.B == 0 and line_2.B == 0:
        return 1
    if line_1.A != 0 and line_1.B != 0 and line_2.A != 0 and line_2.B != 0 \
            and abs(line_1.A / line_2.A - line_1.B / line_2.B) < 1e-8:
        return 1
    return 0

def process(triangle):
    amount = len(dots)
    min_amount = -1
    max_amount = amount + 1

    amount_1 = 0; amount_2 = 0; amount_3 = 0
    amount_4 = 0; amount_5 = 0; amount_6 = 0
    first = Triangle(triangle.a, triangle.middle_ab, triangle.median_middle)
    second = Triangle(triangle.b, triangle.middle_ab, triangle.median_middle)
    third = Triangle(triangle.b, triangle.middle_bc, triangle.median_middle)
    fourth = Triangle(triangle.median_middle, triangle.middle_bc, triangle.c)
    fifth = Triangle(triangle.median_middle, triangle.c, triangle.middle_ac)
    sixth = Triangle(triangle.median_middle, triangle.middle_ac, triangle.a)
    
    for dot in dots:
        if dot != triangle.a and dot != triangle.b and dot != triangle.c:
            if first.has(dot):
                amount_1 += 1
            if second.has(dot):
                amount_2 += 1
            if third.has(dot):
                amount_3 += 1
            if fourth.has(dot):
                amount_4 += 1
            if fifth.has(dot):
                amount_5 += 1
            if sixth.has(dot):
                amount_6 += 1

    result = max(amount_1, amount_2, amount_3, amount_4, amount_5, amount_6) - min(amount_1, amount_2, amount_3, amount_4, amount_5, amount_6)
    return result


def find():
    top_result = -1
    res_triangle = None
    for a in dots:
        for b in dots:
            for c in dots:
                if a != b and a != c and b != c:
                    triangle = Triangle(a, b, c)
                    if not res_triangle and triangle:
                        res_triangle = triangle
                    if abs(triangle.square) > 1e-7 and triangle.median_middle != None:
                        result = process(triangle)
                        if result > top_result:
                            top_result = result
                            res_triangle = triangle
    return res_triangle


def is_inside(dot):
    if 0 < dot.x / scale[1] + size[0] / 2 < size[0] and 0 < dot.y / scale[1] - size[1]/2 < size[1]:
        return True
    else:
        return False


def find_scale():
    min_x = 100000000000
    min_y = 100000000000
    max_x = -100000000000
    max_y = -100000000000
    for dot in dots:
        if dot.x > max_x:
            max_x = dot.x
        if dot.x < min_x:
            min_x = dot.x
        if dot.y > max_y:
            max_y = dot.y
        if dot.y < min_y:
            min_y = dot.y
    for line in lines:
        dot = line.dot_1
        if dot.x > max_x:
            max_x = dot.x
        if dot.x < min_x:
            min_x = dot.x
        if dot.y > max_y:
            max_y = dot.y
        if dot.y < min_y:
            min_y = dot.y
        dot = line.dot_2
        if dot.x > max_x:
            max_x = dot.x
        if dot.x < min_x:
            min_x = dot.x
        if dot.y > max_y:
            max_y = dot.y
        if dot.y < min_y:
            min_y = dot.y
    scale[1] = max(abs(max_x - min_x) / size[0] * 2, abs(max_y - min_y) / size[1] * 2) * 1.1


def build(triangle):
    if triangle:
        triangle.print_info()
        canvas.delete("all")
        triangle.draw(True, True)
        
def get_coordinates(dot):
    global border_x, border_y, scale, x0, y0
    x = (dot.x - x0) / scale + border_x
    y = size[1] + border_y - ((dot.y - y0) / scale)
    return Dot(x, y)

def epicycloid(t):
    global a
    global b
    global shift_x, shift_y
    global scale_center, scale_x, scale_y
    global scale_x, scale_y, scale_center
    x = (a + b) * cos(t) - a * cos((a + b) * t / a) + shift_x
    # x = scale_x * x + (1 - scale_x) * scale_center.x
    y = (a + b) * sin(t) - a * sin((a + b) * t / a) + shift_y
    # y = scale_y * y + (1 - scale_x) * scale_center.x
    return Dot(x, y)

def create_lines():
    global lines

    for line in lines:
        fr = get_coordinates(line[0])
        to = get_coordinates(line[1])
        canvas.create_line(fr.x, fr.y, to.x, to.y, width=2, fill="black")

def draw_epicyclod():
    global a
    global b
    global scale
    global center
    global lft
    global rig
    global delta
    global radius
    global rect

    left_low = get_coordinates(rect[0])
    left_high = get_coordinates(rect[1])
    right_high = get_coordinates(rect[2])
    right_low = get_coordinates(rect[3])

    canvas.create_polygon(left_low.x, left_low.y, left_high.x, left_high.y, \
        right_high.x, right_high.y, right_low.x, right_low.y, width=3, fill="white", outline="black")

    create_lines()
    epicycloid_dots = [(0, 0)]  * (len(drawing) - 1)
    j = 0
    for i in range(2, len(drawing)): 
        dot = get_coordinates(drawing[i])
        epicycloid_dots[j] = (dot.x, dot.y)
        j += 1
    epicycloid_dots[len(epicycloid_dots) - 1] = epicycloid_dots[0]
    canvas.create_polygon(epicycloid_dots, fill="white", outline="red", width=3)
    dot = get_coordinates(drawing[0])
    canvas.create_oval(dot.x - radius, dot.y - radius, dot.x + radius, dot.y + radius, fill="red")
    shift = 15
    canvas.create_text(dot.x, dot.y + shift, text=f"({drawing[0].x:4.3f}; {drawing[0].y:4.3f})", font="Times 14")  

        # canvas.create_line(previous.x, previous.y, dot.x, dot.y, fill="red")
        # previous = dot
        # if i == 10:
        #     break
        # canvas.create_oval(dot.x - radius, dot.y - radius, dot.x + radius, dot.y + radius, fill="red")

def backwards():
    global drawing, drawing_old, scale, scale_old, rect, rect_old, lines, lines_old
    t = copy.deepcopy(rect)
    rect = copy.deepcopy(rect_old)
    rect_old = t
    scale, scale_old = scale_old, scale
    t = copy.deepcopy(drawing)
    drawing = copy.deepcopy(drawing_old)
    drawing_old = t
    t = copy.deepcopy(lines)
    lines = copy.deepcopy(lines_old)
    lines_old = t
    find_and_build()


def find_and_build():
    global scale, x0, y0
    global a, b, center
    canvas.delete("all")
    draw_epicyclod()
    draw_axes(scale, x0, y0)

def fill_drawing():
    global rig, lft, delta, center, drawing, drawing_old, rect, rect_old, lines, lines_old
    global scale_old, scale, scale_orig, scale_x, scale_y, scale_center
    lines = [
        [Dot(-7, -5), Dot(3, 5)], 
        [Dot(-7, -3), Dot(1, 5)],
        [Dot(-7, -1), Dot(-1, 5)],
        [Dot(-7, 1), Dot(-3, 5)],
        [Dot(-7, 3), Dot(-5, 5)],
        [Dot(-5, -5), Dot(5, 5)],
        [Dot(-3, -5), Dot(7, 5)],
        [Dot(-1, -5), Dot(7, 3)],
        [Dot(1, -5), Dot(7, 1)],
        [Dot(3, -5), Dot(7, -1)],
        [Dot(5, -5), Dot(7, -3)]
    ]
    lines_old = copy.deepcopy(lines)
    scale_old = 0.02
    scale = 0.02
    scale_orig = 0.02
    scale_center = Dot(0, 0)
    scale_x = 1
    scale_y = 1
    drawing[0].x = center.x
    drawing[0].y = center.y
    index = 1
    t = lft
    while t < rig and index < len(drawing):
        drawing[index] = epicycloid(t)
        index += 1
        t += delta
    drawing_old = copy.deepcopy(drawing)
    rect = [Dot(-7, -5), Dot(-7, 5), Dot(7, 5), Dot(7, -5)]
    rect_old = copy.deepcopy(rect)
    

# Параметры эпициклоиды
a = 1
b = 3



rect = [Dot(-7, -5), Dot(-7, 5), Dot(7, 5), Dot(7, -5)]

lines = [
    [Dot(-7, -5), Dot(3, 5)], 
    [Dot(-7, -3), Dot(1, 5)],
    [Dot(-7, -1), Dot(-1, 5)],
    [Dot(-7, 1), Dot(-3, 5)],
    [Dot(-7, 3), Dot(-5, 5)],
    [Dot(-5, -5), Dot(5, 5)],
    [Dot(-3, -5), Dot(7, 5)],
    [Dot(-1, -5), Dot(7, 3)],
    [Dot(1, -5), Dot(7, 1)],
    [Dot(3, -5), Dot(7, -1)],
    [Dot(5, -5), Dot(7, -3)]
]
lines_old = copy.deepcopy(lines)
rect_old = copy.deepcopy(rect)
scale_old = 0.02
scale = 0.02
scale_orig = 0.02
scale_center = Dot(0, 0)
scale_x = 1
scale_y = 1
dots = []  # массив для точек
size = [1600, 600]
center = Dot(0, 0)
delta = 0.001
lft = 0
rig = 2 * pi
drawing = [ Dot(0, 0) ] * int(((rig - lft) / delta) + 1)
drawing_old = drawing[:]
x0 = (center.x - a - b) * 11 / 3
y0 = (center.y - a - b) * 5 / 3
border_x = 80
border_y = 60
radius = 2

shift_x = 0
shift_y = 0

fill_drawing()








main_window = tk.Tk()
main_window.geometry("1600x1500")
main_window.title("Лаб. работа №2 \"Преобразования изображения на плоскости\", Вариант 13")
dots_listbox = tk.Listbox(master=main_window, font='Times 14', height=14)


task_label1 = tk.Label(master=main_window, text='Нарисовать исходную фигуру, затем осуществить её перенос, масштабирование и поворот. Фигура: эпициклоида',
                      font='Times 14')
# task_label2 = tk.Label(master=main_window, text='и мин. количества точек, попавших в каждый из 6-ти треугольников, образованных пересечением медиан, максимальна.',
#                       font='Times 14')
task_label1.grid(row=0, column=0, columnspan=100)
# task_label2.grid(row=1, column=0, columnspan=100)

dots_label = tk.Label(master=main_window, text='Перенос изображение. Введите смещение по х, у через \
пробел:', font='Times 14')
dots_label.grid(row=2, column=0)
dots_entry = tk.Entry(master=main_window, font='Times 14')
dots_entry.bind("<Return>", enter_dot_event)
dots_entry.grid(row=2, column=1)
dots_button = tk.Button(master=main_window, text='Перенести', font='Times 14', command=enter_shift)
dots_button.grid(row=2, column=2)
dots_listbox_label = tk.Label(master=main_window, text='Введённые точки:', font='Times 14')
# dots_listbox_label.grid(row=2, column=3)
# dots_listbox.grid(row=2, column=4, rowspan=4)
dots_del_button = tk.Button(master=main_window, text='Шаг назад', font='Times 14', command=backwards)
dots_del_button.grid(row=3, column=2)

scale_label = tk.Label(master=main_window, text='Масштабирование. Введите центр масштабирования и коэффициенты:', font='\
Times 14')
scale_label.grid(row=4, column=0)
scale_entry = tk.Entry(master=main_window, font='Times 14')
scale_entry.bind("<Return>", scale_canvas_event)
scale_entry.grid(row=4, column=1)
delete_dot_button = tk.Button(master=main_window, text='Промасштабировать', font='Times 14', command=scale_canvas)
delete_dot_button.grid(row=4, column=2)

rotate_label = tk.Label(master=main_window, text='Поворот. Введите центр поворота и градус поворота: ', font='Times 14')
rotate_label.grid(row=5, column=0)
rotate_entry = tk.Entry(master=main_window, font='Times 14')
rotate_entry.bind("<Return>", rotate_event)
rotate_entry.grid(row=5, column=1)
rotate_button = tk.Button(master=main_window, text='Повернуть', font='Times 14', command=rotate)
rotate_button.grid(row=5, column=2)

glob_scale_label = tk.Label(master=main_window, text='Изменить масштаб. Во сколько раз хотите увеличить масштаб: ', font='Times 14')
glob_scale_label.grid(row=6, column=0)
glob_scale_entry = tk.Entry(master=main_window, font='Times 14')
glob_scale_entry.bind("<Return>", glob_scale_event)
glob_scale_entry.grid(row=6, column=1)
glob_scale_button = tk.Button(master=main_window, text='Изменить масштаб', font='Times 14', command=glob_scale)
glob_scale_button.grid(row=6, column=2)

final_button = tk.Button(master=main_window, text='Построить эпициклоиду', font='Arial\
 16', command=find_and_build)
final_button.grid(row=7, column=1)

refill_button = tk.Button(master=main_window, text='К началу', font='Times 14', command=refill)
refill_button.grid(row=7, column=2)


canvas = ResizingCanvas(main_window, height=size[1], width=size[0], bg='white')
canvas.grid(row=8, column=0, columnspan=7)

for row_num in range(main_window.grid_size()[1]):
    main_window.rowconfigure(row_num, weight=1)
for col_num in range(main_window.grid_size()[0]):
    main_window.columnconfigure(col_num, weight=1)

main_window.mainloop()

