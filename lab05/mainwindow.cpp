#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QColorDialog>
#include <QMessageBox>
#include <QPainter>
#include <algorithm>
#include <iostream>

MainWindow::MainWindow(QWidget *parent) :
	QMainWindow(parent),
	ui(new Ui::MainWindow),
	closed(false),
	fillColor(defaultFillColor),
    fillColorInversion(Qt::white),
    n_edges(0),
    max_x(-1)
{
	ui->setupUi(this);

	pixmap = QPixmap(ui->drawLabel->width(), ui->drawLabel->height());
	image = QImage(ui->drawLabel->width(), ui->drawLabel->height(), QImage::Format_RGB32);
	ui->drawLabel->setPixmapPointer(pixmap);

	clearImage();
	colorLabel();

	Q_ASSERT(defaultBoundColor != defaultFillColor);
}

MainWindow::~MainWindow()
{
	delete ui;
}

void MainWindow::mousePressEvent(QMouseEvent *event)
{
	const int x = event->x() - ui->drawLabel->x();
	const int y = event->y() - ui->drawLabel->y();
	if (x < 0 || y < 0 || x >= pixmap.width() || y >= pixmap.height())
		return;

	DrawType drawType = DrawType::none;
	switch (QApplication::keyboardModifiers()) {
	case Qt::ShiftModifier:
		drawType = DrawType::horizontal;
		break;
	case Qt::ControlModifier:
		drawType = DrawType::vertical;
		break;
	case Qt::ShiftModifier | Qt::ControlModifier:
		drawType = DrawType::diagonal;
		break;
	default:
		break;
	}

	addPoint(QPoint(x, y), drawType);
}

void MainWindow::on_addPointPushButton_clicked()
{
	const int x = ui->xSpinBox->text().toInt();
	const int y = ui->ySpinBox->text().toInt();
	addPoint(QPoint(x, y), DrawType::none);
}

void MainWindow::on_closePushButton_clicked()
{
	if (closed) {
        QMessageBox::critical(this, "Ошибка", "Фигура уже замкнута!");
		return;
	}

    if (n_edges < 2) {
        QMessageBox::critical(this, "Ошибка", "Нужно как минимум 2 ребра!");
		return;
	}

    addEdge(QLine(points[points.size() - 1], firstPoint));
	closed = true;
	n_edges = 0;
}

constexpr int sgn(int val) {
	if (val > 0)
		return 1;
	if (val < 0)
		return -1;
	return 0;
}

QVector<QPoint> handleVertices(QVector<QPoint> &intersections, const QVector<QLine> &edges)
{
    QVector<QPoint> extension;
    for (int i = 0; i < edges.size() - 1; ++i) {
        if (edges[i].p1().y() != edges[i].p2().y()) {
            if (edges[i].p2().y() == edges[i + 1].p1().y() &&
                    sgn(edges[i].p1().y() - edges[i].p2().y()) == sgn(edges[i + 1].p1().y() - edges[i + 1].p2().y()))
                extension.push_back(edges[i].p2());
        }
    }
    return extension;
}

void MainWindow::fixVertices(QVector<QPoint>& intersections)
{
    displayImage();

    QPainter painter(&pixmap);
    painter.setPen(fillColor);

    for (int k = 0; k < intersections.size(); k++) {
        int y = intersections[k].y();
        for (int x = intersections[k].x(); x < max_x; x++) {
            if (image.pixelColor(x, y) == fillColor) {
                painter.setPen(Qt::white);
                painter.drawPoint(x, y);
            }
            else if (image.pixelColor(x, y) != defaultBoundColor) {
                painter.setPen(fillColor);
                painter.drawPoint(x, y);
            }
        }
        displayImage();
        if (ui->delayCheckBox->isChecked()) {
            delay(ui->delaySpinBox->value());
        }
    }
    displayImage();
}

void sortY(QVector<QPoint> &intersections)
{
	std::sort(
		intersections.begin(), intersections.end(),
		[](const QPoint &p1, const QPoint &p2) {
			return p1.y() > p2.y();
	});
}

void sortX(QVector<QPoint> &intersections, QVector<int> &indices)
{
	indices.reserve(intersections.front().y() - intersections.back().y() + 1);
	for (int i = 0; i < intersections.size();) {
		indices.push_back(i);
		int j = i;
		while (++j < intersections.size() && intersections[j].y() == intersections[i].y())
			;
		std::sort(
			intersections.begin() + i, intersections.begin() + j,
			[](const QPoint &p1, const QPoint &p2) {
				return p1.x() < p2.x();
		});
		i = j;
	}
	indices.push_back(intersections.size());
}

void MainWindow::on_fillPushButton_clicked()
{
    if (!closed) {
        QMessageBox::critical(this, "Ошибка", "Фигура не замкнута! Воспользуйтесь опцией \"Замкнуть\".");
        return;
    }

    displayImage();

    QPainter painter(&pixmap);
    painter.setPen(fillColor);

    for (int k = 0; k < intersections.size(); k++) {
        int y = intersections[k].y();
        for (int x = intersections[k].x(); x < max_x; x++) {
            if (image.pixelColor(x, y) == fillColor) {
                painter.setPen(Qt::white);
                painter.drawPoint(x, y);
            }
            else if (image.pixelColor(x, y) != defaultBoundColor) {
                painter.setPen(fillColor);
                painter.drawPoint(x, y);
            }
        }
        displayImage();
        if (ui->delayCheckBox->isChecked()) {
            delay(ui->delaySpinBox->value());
        }
    }
    painter.end();
    QVector<QPoint> toFix = handleVertices(intersections, edges);
    fixVertices(toFix);
    fixVertices(firstPoints);
    displayImage();
}

void MainWindow::on_clearPushButton_clicked()
{
	clearImage();
	closed = false;
	points.clear();
	edges.clear();
    firstPoints.clear();
	intersections.clear();
	fillColor = defaultFillColor;
	colorLabel();
	n_edges = 0;
    max_x = -1;
	ui->tableWidget->clearContents();
	ui->tableWidget->model()->removeRows(0, ui->tableWidget->rowCount());
}

void MainWindow::on_setColorPushButton_clicked()
{
    fillColor = QColorDialog::getColor(fillColor, this, "Выберите цвет", QColorDialog::DontUseNativeDialog);
	if (fillColor == defaultBoundColor)
		fillColor = defaultFillColor;
    fillColorInversion = QColor(fillColor.alpha() - fillColor.red(),
                                fillColor.alpha() - fillColor.green(),
                                fillColor.alpha() - fillColor.blue(),
                                fillColor.alpha());
	colorLabel();
}

void MainWindow::addPoint(const QPoint &point, DrawType drawType)
{
	const int n = points.size();
	points.push_back(point);
	ui->tableWidget->insertRow(n);
    if (n && !closed)
		switch (drawType) {
		case DrawType::horizontal:
			points[n].setY(points[n - 1].y());
			break;
		case DrawType::vertical:
			points[n].setX(points[n - 1].x());
			break;
		case DrawType::diagonal: {
			const int dx = points[n].x() - points[n - 1].x();
			const int dy = points[n].y() - points[n - 1].y();
			if (dx * dy >= 0) {
				const int d = (dx + dy) / 2;
				points[n].setX(points[n - 1].x() + d);
				points[n].setY(points[n - 1].y() + d);
			}
			else {
				const int d = (dx - dy) / 2;
				points[n].setX(points[n - 1].x() + d);
				points[n].setY(points[n - 1].y() - d);
			}
		}
		case DrawType::none:
		default:
			break;
		}
    else
        firstPoint = points[n];
	ui->tableWidget->setItem(n, 0, new QTableWidgetItem(QString::number(points[n].x())));
	ui->tableWidget->setItem(n, 1, new QTableWidgetItem(QString::number(points[n].y())));
    if (point.x() > max_x) { max_x = point.x(); }

    if (n && !closed) {
		addEdge(QLine(points[closed ? 0 : n - 1], points[n]));
		closed = false;
    } else if (n != 0)
        firstPoints.push_back(point);
    closed = false;
}

void MainWindow::addEdge(const QLine &edge)
{
	edges.push_back(edge);
	++n_edges;

	dda(edge);

	displayImage();
}

void MainWindow::dda(const QLine &edge)
{
	const int deltaX = edge.p2().x() - edge.p1().x();
	const int deltaY = edge.p2().y() - edge.p1().y();

	int length = qMax(qAbs(deltaX), qAbs(deltaY));

	QPainter painter(&pixmap);
    painter.setPen(defaultBoundColor);

	const bool horizontal = edge.p1().y() == edge.p2().y();
	if (horizontal && edge.p1().x() == edge.p1().y()) {
		painter.drawPoint(edge.p1());
		return;
	}

	// Полагаем большее из приращений dx или dy равным единице растра
	const float dx = static_cast<float>(deltaX) / length;
	const float dy = static_cast<float>(deltaY) / length;

	int xl = -1;
	int xr = -1;
	int yp = -1;
	const int xr_dir = sgn(deltaX);

	float xf = edge.p1().x();
	float yf = edge.p1().y();

	for (int i = 0; i <= length; ++i) {
		const int x = qRound(xf);
		const int y = qRound(yf);
		painter.drawPoint(x, y);
		if (!horizontal) {
			if (y != yp) {
				if (yp != edge.p1().y() && i)
					intersections.push_back(QPoint((xl + xr) / 2, yp));
				xl = xr = x;
				yp = y;
			}
			else
				xr += xr_dir;
		}
		xf += dx;
		yf += dy;
	}
}

void MainWindow::delay(int times)
{
	for (int i = 0; i < times; ++i) {
		repaint();
		resize(width(), height());
	}
}

void MainWindow::clearImage()
{
	pixmap.fill();
	displayImage();
}

void MainWindow::displayImage()
{
	ui->drawLabel->update();
	image = pixmap.toImage();
}

void MainWindow::colorLabel()
{
	QPalette palette = ui->colorLabel->palette();
	palette.setColor(ui->colorLabel->backgroundRole(), fillColor);
	ui->colorLabel->setAutoFillBackground(true);
	ui->colorLabel->setPalette(palette);
}
