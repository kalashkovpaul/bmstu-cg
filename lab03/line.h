#ifndef LINE_H
#define LINE_H

#include "canvas.h"
#include <QPainter>

int dda(const QLine &line, Canvas &canvas);
int bresenhamFloat(const QLine &line, Canvas &canvas);
int bresenhamInteger(const QLine &line, Canvas &canvas);
int bresenhamAntialiased(const QLine &line, Canvas &canvas);
int defaultQt(const QLine &line, Canvas &canvas);
int defaultQtCore(const QLine &line, QPainter &painter);
int wu(const QLine &line, Canvas &canvas);

bool ddaTest(const QLine &line, Canvas &canvas);
bool bresenhamFloatTest(const QLine &line, Canvas &canvas);
bool bresenhamIntegerTest(const QLine &line, Canvas &canvas);
bool bresenhamAntialiasedTest(const QLine &line, Canvas &canvas);
bool defaultQtTest(const QLine &line, Canvas &canvas);
bool wuTest(const QLine &line, Canvas &canvas);

#endif // LINE_H
