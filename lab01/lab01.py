# Лабораторная работа №1 по Компьютерной графике, Вариант 27
# На плоскости дано множество точек. Найти такой треугольник с вершинами в этих точках,
# у которого разность максимального и минимального количества точек, попавших в каждый из
# 6-ти треугольников, образованных пересечением медиан, максимальна.
# Автор: Калашков Павел, ИУ7-46Б

from doctest import master
import tkinter as tk
import tkinter.messagebox as box
from tkinter import *


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
    
    def print_info_to_entry(self):
        results_entry.configure(state='normal')
        results_entry.delete(0, last='end')
        string = "треугольник с вершинами в точках " + str(self.a) + ", " + str(self.b) + ", " + str(self.c)
        results_entry.insert(0, string)
        results_entry.configure(state='readonly')

            
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
            

def enter_dot():
    try:
        x, y = map(float, dots_entry.get().split())
        new_dot = Dot(x, y)
        dots.append(new_dot)
        dot_string = "{:d}) ({:6.4f}; {:6.4f})".format(len(dots), x, y)
        dots_listbox.insert(len(dots), dot_string)
        dots_entry.delete(0, last='end')
    except ValueError:
        dots_entry.delete(0, last='end')
        box.showwarning("Ошибка ввода", "Вы ввели неверные координаты точки. Координаты точек\
         - вещественные числа, введённые через пробел")

def delete_dot():
    try:
        number = int(delete_dot_entry.get())
        if number >= 0 and number <= dots_listbox.size():
            dots.pop(number - 1)
            dots_listbox.delete(number - 1)
            for i in range(dots_listbox.size()):
                dot_string = dots_listbox.get(i)
                dot_string = dot_string.replace(")", "")
                dot_string = dot_string.replace("(", "")
                dot_string = dot_string.replace(";", "")
                cur_num, x, y = map(float, dot_string.split())
                cur_num = int(cur_num)
                if cur_num >= number:
                    cur_num -= 1
                    dot_string = "{:d}) ({:6.4f}; {:6.4f})".format(cur_num, x, y)
                    dots_listbox.delete(cur_num - 1)
                    dots_listbox.insert(cur_num - 1, dot_string)
            delete_dot_entry.delete(0, last='end')
        else:
            delete_dot_entry.delete(0, last='end')
            box.showwarning("Ошибка ввода", "Вы ввели неверный номер точки. Уточние, пожалуйста")
    except ValueError:
        delete_dot_entry.delete(0, last='end')
        box.showwarning("Ошибка ввода", "Вы ввели неверный номер точки. Номер точки - неотрицательное целое число")

def edit_dot():
    try:
        number, x, y = map(float, edit_dot_entry.get().split())
        number = int(number)
        if number >= 0 and number <= dots_listbox.size():
            dot_string = "{:d}) ({:6.4f}; {:6.4f})".format(number, x, y)
            new_dot = Dot(x, y)
            dots[number - 1] = new_dot
            dots_listbox.delete(number - 1)
            dots_listbox.insert(number - 1, dot_string)
            edit_dot_entry.delete(0, last='end')
        else:
            edit_dot_entry.delete(0, last='end')
            box.showwarning("Ошибка ввода", "Вы ввели неверный номер точки. Номер точки - неотрицательное целое число")
    except ValueError:
        edit_dot_entry.delete(0, last='end')
        box.showwarning("Ошибка ввода", "Номер точки - неотрицательное целое число, координаты - действительные числа")


def enter_dot_event(event):
    enter_dot()

def del_dots():
    dots.clear()
    dots_entry.delete(0, last='end')
    dots_listbox.delete(0, dots_listbox.size())

def delete_dot_event(event):
    delete_dot()

def edit_dot_event(event):
    edit_dot()

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
        triangle.print_info_to_entry()
        canvas.delete("all")
        triangle.draw(True, True)
        

def find_and_build():
    if len(dots) < 3:
        box.showwarning("Недостаточное количество точек", "Элементов недостаточно. Введите больше точек (как минимум 3)")
    
    triangle = find()
    if triangle:
        if abs(triangle.square) < 1e-7:
            box.showwarning("Все треугольники вырожденные", "Не удалось найти подходящий треугольник. Попробуйте добавить больше точек в множество")
        else:
            build(triangle)
    else:
        box.showwarning("Не получилось", "Не получилось, непонятная ошибка")
    



dots = []  # массив для точек
lines = []  # координаты точек, задающих прямую
scale = [1, 1]  # масштаб для canvas
size = [1600, 600]
main_window = tk.Tk()
main_window.geometry("1600x1500")
main_window.title("Лаб. работа №1 \"Геометрическая задача\", Вариант 27")
dots_listbox = tk.Listbox(master=main_window, font='Times 14', height=14)


task_label1 = tk.Label(master=main_window, text='На плоскости дано множество точек. Найти такой треугольник с вершинами в этих точках, у которого разность макс.',
                      font='Times 14')
task_label2 = tk.Label(master=main_window, text='и мин. количества точек, попавших в каждый из 6-ти треугольников, образованных пересечением медиан, максимальна.',
                      font='Times 14')
task_label1.grid(row=0, column=0, columnspan=100)
task_label2.grid(row=1, column=0, columnspan=100)

dots_label = tk.Label(master=main_window, text='Добавление точки. Введите координаты по х, у через \
пробел:', font='Times 14')
dots_label.grid(row=2, column=0)
dots_entry = tk.Entry(master=main_window, font='Times 14')
dots_entry.bind("<Return>", enter_dot_event)
dots_entry.grid(row=2, column=1)
dots_button = tk.Button(master=main_window, text='Добавить точку', font='Times 14', command=enter_dot)
dots_button.grid(row=2, column=2)
dots_listbox_label = tk.Label(master=main_window, text='Введённые точки:', font='Times 14')
dots_listbox_label.grid(row=2, column=3)
dots_listbox.grid(row=2, column=4, rowspan=4)
dots_del_button = tk.Button(master=main_window, text='Сброс', font='Times 14', command=del_dots)
dots_del_button.grid(row=3, column=2)

delete_label = tk.Label(master=main_window, text='Удаление. Для удаления введите номер точки:', font='\
Times 14')
delete_label.grid(row=4, column=0)
delete_dot_entry = tk.Entry(master=main_window, font='Times 14')
delete_dot_entry.bind("<Return>", delete_dot_event)
delete_dot_entry.grid(row=4, column=1)
delete_dot_button = tk.Button(master=main_window, text='Удалить точку', font='Times 14', command=delete_dot)
delete_dot_button.grid(row=4, column=2)

edit_dot_label = tk.Label(master=main_window, text='Редактирование. Введите номер точки и новые координаты, через пробел:', font='Times 14')
edit_dot_label.grid(row=5, column=0)
edit_dot_entry = tk.Entry(master=main_window, font='Times 14')
edit_dot_entry.bind("<Return>", edit_dot_event)
edit_dot_entry.grid(row=5, column=1)
edit_dot_button = tk.Button(master=main_window, text='Редактировать', font='Times 14', command=edit_dot)
edit_dot_button.grid(row=5, column=2)

final_button = tk.Button(master=main_window, text='Найти треугольник, построить иллюстрацию', font='Arial\
 16', command=find_and_build)
final_button.grid(row=6, column=0)
results_label = tk.Label(master=main_window, text='Результаты: ', font='Times 16')
results_label.grid(row=6, column=1)
results_entry = tk.Entry(master=main_window, font='Times 16', width=60, state='disabled')
results_entry.grid(row=6, column=2, columnspan=2)

canvas = ResizingCanvas(main_window, height=size[1], width=size[0], bg='white')
canvas.grid(row=7, column=0, columnspan=7)

for row_num in range(main_window.grid_size()[1]):
    main_window.rowconfigure(row_num, weight=1)
for col_num in range(main_window.grid_size()[0]):
    main_window.columnconfigure(col_num, weight=1)

main_window.mainloop()
