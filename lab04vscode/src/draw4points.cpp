#include "draw4points.h"

void draw4points(const QPoint &c, int x, int y, Canvas &canvas) {
	canvas.image->setPixel(c.x() + x, c.y() + y, canvas.color->rgb());
	canvas.image->setPixel(c.x() + x, c.y() - y, canvas.color->rgb());
	canvas.image->setPixel(c.x() - x, c.y() + y, canvas.color->rgb());
	canvas.image->setPixel(c.x() - x, c.y() - y, canvas.color->rgb());
}

void add4points(QVector<int>& data, const QPoint& c, const int x, const int y) {
    data.append(c.x());
    data.append(c.y());
    data.append(x);
    data.append(y);
}
