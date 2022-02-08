# Лабораторная работа №1 по Компьютерной графике, Вариант 27
# На плоскости дано множество точек. Найти такой треугольник с вершинами в этих точках,
# у которого разность максимального и минимального количества точек, попавших в каждый из
# 6-ти треугольников, образованных пересечением медиан, максимальна.
# Автор: Калашков Павел, ИУ7-46Б

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

# def main():
#     root = Tk()
#     myframe = Frame(root)
#     myframe.pack(fill=BOTH, expand=YES)
#     mycanvas = ResizingCanvas(myframe,width=850, height=400, bg="red", highlightthickness=0)
#     mycanvas.pack(fill=BOTH, expand=YES)

#     # add some widgets to the canvas
#     mycanvas.create_line(0, 0, 200, 100)
#     mycanvas.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
#     mycanvas.create_rectangle(50, 25, 150, 75, fill="blue")

#     # tag all of the drawn widgets
#     mycanvas.addtag_all("all")
#     root.mainloop()

# if __name__ == "__main__":
#     main()

class Dot(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line(object):
    def __init__(self, dot_1, dot_2):
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


def find():
    maximum = 0
    counter = 0
    target_line = None
    for dot_1 in dots:
        for dot_2 in dots:
            if dot_1 != dot_2:
                line_1 = Line(dot_1, dot_2)
                for line_2 in lines:
                    if is_parallel(line_1, line_2):
                        counter += 1
                    if counter > maximum:
                        maximum = counter
                        target_line = line_1
    return target_line


def is_inside(dot):
    if 0 < dot.x / scale[1] + size[0]/2 < size[0] and 0 < dot.y / scale[1] - size[1]/2 < size[1]:
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


def build():
    canvas.delete("all")
    find_scale()
    for line in lines:
        line.print_line()


def find_and_build():
    if len(dots) == 0 or len(lines) == 0:
        box.showwarning("Недостаточное количество элементов", "Элементов недостаточно. Введите больше элементов")
    build()
    target = find()
    if target is not None:
        target.print_target()


dots = []  # массив для точек
lines = []  # координаты точек, задающих прямую
scale = [1, 1]  # масштаб для canvas
size = [1600, 600]
main_window = tk.Tk()
main_window.geometry("1600x1500")
main_window.title("Лаб. работа №1 \"Геометрическая задача\", Вариант 27")
dots_listbox = tk.Listbox(master=main_window, font='Times 14', height=10)


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
final_button.grid(row=6, column=1)

canvas = tk.Canvas(height=size[1], width=size[0], bg='white')
canvas.grid(row=7, column=0, columnspan=7)

for row_num in range(main_window.grid_size()[1]):
    main_window.rowconfigure(row_num, weight=1)
for col_num in range(main_window.grid_size()[0]):
    main_window.columnconfigure(col_num, weight=1)

main_window.mainloop()
