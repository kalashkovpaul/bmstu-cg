#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QColorDialog>
#include <QElapsedTimer>
#include <cmath>
#include <iostream>

#include "circle.h"
#include "ellipse.h"
#include "dialog.h"

MainWindow::MainWindow(QWidget *parent) :
	QMainWindow(parent),
	ui(new Ui::MainWindow),
	fgColor(defaultFgColor),
	scene(new QGraphicsScene(0, 0, 721, 721)),
	image(QImage(721, 721, QImage::Format_ARGB32))
{
	ui->setupUi(this);

	ui->graphicsView->setScene(scene);
	imageView();

	on_clearAllPushButton_clicked();
	on_setDefaultFgColor_clicked();
}

MainWindow::~MainWindow()
{
	delete ui;
}

void MainWindow::colorLabel(QLabel *label, QColor &color) {
	QPalette palette = label->palette();
	palette.setColor(label->backgroundRole(), color);
	label->setAutoFillBackground(true);
	label->setPalette(palette);
}

void MainWindow::imageView() {
	scene->addPixmap(QPixmap::fromImage(image));
}

template <typename T> int sgn1(T val) {
	return (val > 0) - (val < 0);
}

void MainWindow::on_setFgColorPushButton_clicked()
{
	fgColor = QColorDialog::getColor(fgColor, this, "Pick a FG color", QColorDialog::DontUseNativeDialog);
	colorLabel(ui->fgLabel, fgColor);
}

void MainWindow::on_setBgColorToFgPushButton_clicked()
{
	fgColor = defaultBgColor;
	colorLabel(ui->fgLabel, fgColor);
}

void MainWindow::on_setDefaultFgColor_clicked()
{
	fgColor = defaultFgColor;
	colorLabel(ui->fgLabel, fgColor);
}

void MainWindow::drawCircle(const QPoint &center, int radius, Canvas &canvas)
{
	if (ui->canonicalRadioButton->isChecked())
		canonical(center, radius, canvas);
	else if (ui->parametricRadioButton->isChecked())
		parametric(center, radius, canvas);
	else if (ui->bresenhamRadioButton->isChecked())
		bresenham(center, radius, canvas);
	else if (ui->midPointRadioButton->isChecked())
		midPoint(center, radius, canvas);
	else if (ui->defaultQtRadioButton->isChecked())
		defaultQt(center, radius, canvas);
}

void MainWindow::drawEllipse(const QPoint &center, int a, int b, Canvas &canvas)
{
	if (ui->canonicalRadioButton->isChecked())
		canonical(center, a, b, canvas);
	else if (ui->parametricRadioButton->isChecked())
		parametric(center, a, b, canvas);
	else if (ui->bresenhamRadioButton->isChecked())
		bresenham(center, a, b, canvas);
	else if (ui->midPointRadioButton->isChecked())
		midPoint(center, a, b, canvas);
	else if (ui->defaultQtRadioButton->isChecked())
		defaultQt(center, a, b, canvas);
}

void MainWindow::on_drawCirclePushButton_clicked()
{
	const int x = 360 + ui->xSpinBox->text().toInt();
	const int y = 360 - ui->ySpinBox->text().toInt();
	const int r = ui->rSpinBox->text().toInt();
	const QPoint center(x, y);
	Canvas canvas = { &image, &fgColor };

	QElapsedTimer timer;
	timer.start();

	drawCircle(center, r, canvas);

	ui->statusBar->showMessage(QString::number(timer.nsecsElapsed()));

	imageView();
}

void MainWindow::on_drawEllipsePushButton_clicked()
{
	const int x = 360 + ui->xSpinBox->text().toInt();
	const int y = 360 - ui->ySpinBox->text().toInt();
	const int a = ui->aSpinBox->text().toInt();
	const int b = ui->bSpinBox->text().toInt();
	const QPoint center(x, y);
	Canvas canvas = { &image, &fgColor };

	QElapsedTimer timer;
	timer.start();

    drawEllipse(center, a, b, canvas);

	ui->statusBar->showMessage(QString::number(timer.nsecsElapsed()));

	imageView();
}

void MainWindow::on_drawCirclesPushButton_clicked()
{
	int r0 = ui->r0SpinBox->text().toInt();
	const int dr = ui->drSpinBox->text().toInt();
	const int n = ui->nSpinBox->text().toInt();
	const QPoint center(360, 360);
	Canvas canvas = { &image, &fgColor };

	for (int i = 0; i != n; ++i) {
		drawCircle(center, r0, canvas);
		r0 += dr;
	}

	imageView();
}

void MainWindow::on_drawEllipsesPushButton_clicked()
{
	int a = ui->a0SpinBox->text().toInt();
	int b = ui->b0SpinBox->text().toInt();
	const int dr = ui->drSpinBox->text().toInt();
	const int n = ui->nSpinBox->text().toInt();
	const QPoint center(360, 360);
	Canvas canvas = { &image, &fgColor };

	for (int i = 0; i != n; ++i) {
		drawEllipse(center, a, b, canvas);
		a += dr;
		b += dr;
	}

	imageView();
}

void MainWindow::on_clearAllPushButton_clicked()
{
	ui->statusBar->showMessage("");
	image.fill(defaultBgColor);
	imageView();
}

void MainWindow::on_statisticsCirclePushButton_clicked()
{
    const int testAmount = 100;
    const int maxRadius = 100;
    const int functionAmount = 5;
    double nanoseconds[functionAmount][maxRadius];
    const QPoint center(360, 360);
    QColor color = defaultBgColor;
    Canvas canvas = { &image, &color};
    void (*func[functionAmount])(const QPoint&, const int, Canvas &) = {
        canonical,
        parametric,
        bresenham,
        midPoint,
    };
    for (int i = 0; i != functionAmount - 1; i++) {
        for (int radius = 1; radius != maxRadius + 1; radius++) {
            QElapsedTimer timer;
            timer.start();
            for (int k = 0; k < testAmount; k++) {
                func[i](center, radius, canvas);
            }
            nanoseconds[i][radius - 1] = static_cast<double> (timer.nsecsElapsed() / testAmount);
        }
    }
    for (int radius = 1; radius != maxRadius - 1; radius++) {
        size_t time = 0;
        for (int k = 0; k < testAmount; k++) {
            time += defaultQt(center, radius, canvas);
        }
        nanoseconds[functionAmount - 1][radius - 1] = static_cast<double> (time / testAmount);
    }
    QVector<QVector<double>> nanoVector(functionAmount);
    for (int i = 0; i < functionAmount; i++) {
        std::copy(nanoseconds[i], nanoseconds[i] + maxRadius, std::back_inserter(nanoVector[i]));
    }
    Dialog dialog(nanoVector, maxRadius, nullptr, true);
    dialog.setModal(true);
    dialog.exec();
}

void MainWindow::on_statisticsEllipsePushButton_clicked()
{
    const int testAmount = 500;
    const int functionAmount = 5;
    int a0 = ui->a0SpinBox->text().toInt();
    int b0 = ui->b0SpinBox->text().toInt();
    const int dr = ui->drSpinBox->text().toInt();
    const int n = ui->nSpinBox->text().toInt();
    double nanoseconds[functionAmount][n];
    const QPoint center(360, 360);
    QColor color = defaultBgColor;
    Canvas canvas = { &image, &color};
    void (*func[functionAmount])(const QPoint&, const int, const int, Canvas &) = {
        canonical,
        parametric,
        bresenham,
        midPoint
    };
    int a = a0;
    int b = b0;
    for (int i = 0; i != functionAmount - 1; i++) {
        a = a0;
        b = b0;
        for (int j = 1; j != n + 1; j++) {
            a += dr;
            b += dr;
            QElapsedTimer timer;
            timer.start();
            for (int k = 0; k < testAmount; k++) {
                func[i](center, a, b, canvas);
            }
            nanoseconds[i][j - 1] = static_cast<double> (timer.nsecsElapsed() / testAmount);
        }
    }
    a = a0;
    b = b0;
    for (int j = 1; j != n + 1; j++) {
        a += dr;
        b += dr;
        size_t time = 0;
        for (int k = 0; k < testAmount; k++) {
            time += defaultQt(center, a, b, canvas);
        }
        nanoseconds[functionAmount - 1][j - 1] = static_cast<double> (time / testAmount);
    }
    QVector<QVector<double>> nanoVector(functionAmount);
    for (int i = 0; i < functionAmount; i++) {
        std::copy(nanoseconds[i], nanoseconds[i] + n, std::back_inserter(nanoVector[i]));
    }
    Dialog dialog(nanoVector, n, nullptr, false, a0, dr);
    dialog.setModal(true);
    dialog.exec();
}























