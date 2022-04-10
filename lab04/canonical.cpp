#include "draw4points.h"
#include <cmath>

QVector<int>& canonicalCircle(const QPoint &c, const int r, Canvas &canvas)
{
    const int r2 = r*r;
    QVector<int> data;
    int deltaX = qRound(r * M_SQRT1_2);
    for (int x = 0; x <= deltaX; ++x) {
        const int y = qRound(sqrt(r2 - x*x));
        add4points(data, c, x, y);
        add4points(data, c, y, x);
    }
    return data;
}

QVector<int>& canonicalEllipce(const QPoint &c, const int a, const int b, Canvas &canvas)
{
    const int a2 = a * a;
    const int b2 = b * b;
    QVector<int> data;
    const float bDivA = static_cast<float>(b) / a;
    const int deltaX = qRound(a2 / sqrt(a2 + b2));
    for (int x = 0; x <= deltaX; ++x) {
        const int y = qRound(sqrt(static_cast<float>(a2 - x*x)) * bDivA);
        add4points(data, c, x, y);
    }

    const float aDivB = static_cast<float>(a) / b;
    const int deltaY = qRound(b2 / sqrt(a2 + b2));
    for (int y = 0; y <= deltaY; ++y) {
        const int x = qRound(sqrt(static_cast<float>(b2 - y*y)) * aDivB);
        add4points(data, c, x, y);
    }
}
