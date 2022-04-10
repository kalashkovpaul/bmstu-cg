#ifndef DRAW4POINTS_H
#define DRAW4POINTS_H

#include "canvas.h"

void draw4points(const QPoint &c, int x, int y, Canvas &canvas);

void add4points(QVector<int>& data, const QPoint& c, const int x, const int y);

#endif // DRAW4POINTS_H
