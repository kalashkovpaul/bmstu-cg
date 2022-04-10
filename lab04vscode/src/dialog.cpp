#include "dialog.h"
#include "ui_dialog.h"

#include <algorithm>

Dialog::Dialog(const QVector<QVector<double>> &ns, int M, QWidget *parent, bool isCircle, int x0, int dr) :
	QDialog(parent),
	ui(new Ui::Dialog)
{
	ui->setupUi(this);

	ui->customPlot->addGraph();
	ui->customPlot->graph(0)->setPen(QPen(QColor(0, 0, 0xff), 2));
	ui->customPlot->addGraph();
	ui->customPlot->graph(1)->setPen(QPen(QColor(0, 0xff, 0), 2));
	ui->customPlot->addGraph();
	ui->customPlot->graph(2)->setPen(QPen(QColor(0xff, 0, 0xff), 2));
	ui->customPlot->addGraph();
	ui->customPlot->graph(3)->setPen(QPen(QColor(0xff, 0, 0), 2));
	ui->customPlot->addGraph();
	ui->customPlot->graph(4)->setPen(QPen(Qt::gray, 2));

	QVector<double> x(M);
    int curX = x0;
    for (int i = 0; i != M; i++) {
        x[i] = curX;
        curX += dr;
    }
	// configure right and top axis to show ticks but no labels:
	// (see QCPAxisRect::setupFullAxesBox for a quicker method to do this)
	ui->customPlot->xAxis2->setVisible(true);
    if (isCircle)
        ui->customPlot->xAxis2->setLabel("Радиус окружности, пкс");
    else
        ui->customPlot->xAxis2->setLabel("Полуось a, пкс");
	ui->customPlot->xAxis2->setTickLabels(true);
	ui->customPlot->yAxis2->setVisible(true);
    ui->customPlot->yAxis2->setLabel("Время отрисовки, наносекунды");
	ui->customPlot->yAxis2->setTickLabels(true);
	// make left and bottom axes always transfer their ranges to right and top axes:
	connect(ui->customPlot->xAxis, SIGNAL(rangeChanged(QCPRange)), ui->customPlot->xAxis2, SLOT(setRange(QCPRange)));
	connect(ui->customPlot->yAxis, SIGNAL(rangeChanged(QCPRange)), ui->customPlot->yAxis2, SLOT(setRange(QCPRange)));
	// pass data points to graphs:
	ui->customPlot->graph(0)->setData(x, ns[0]);
	ui->customPlot->graph(1)->setData(x, ns[1]);
	ui->customPlot->graph(2)->setData(x, ns[2]);
	ui->customPlot->graph(3)->setData(x, ns[3]);
	ui->customPlot->graph(4)->setData(x, ns[4]);

    ui->customPlot->graph(0)->setName("Канонически");
    ui->customPlot->graph(1)->setName("Параметрически");
    ui->customPlot->graph(2)->setName("Метод Брезенхема");
    ui->customPlot->graph(3)->setName("Метод средней точки");
    ui->customPlot->graph(4)->setName("Стандартный алгоритм (Qt)");

	// let the ranges scale themselves so graph 0 fits perfectly in the visible area:
	ui->customPlot->graph(0)->rescaleAxes();
	// same thing for graph 1, but only enlarge ranges (in case graph 1 is smaller than graph 0):
	ui->customPlot->graph(1)->rescaleAxes(true);
	// Note: we could have also just called ui->customPlot->rescaleAxes(); instead
	// Allow user to drag axis ranges with mouse, zoom with mouse wheel and select graphs by clicking:
	ui->customPlot->setInteractions(QCP::iRangeDrag | QCP::iRangeZoom | QCP::iSelectPlottables);

	// setup legend:
	ui->customPlot->legend->setVisible(true);
	ui->customPlot->axisRect()->insetLayout()->setInsetAlignment(0, Qt::AlignTop|Qt::AlignHCenter|Qt::AlignLeft);
	ui->customPlot->legend->setBrush(QColor(255, 255, 255, 100));
	ui->customPlot->legend->setBorderPen(Qt::NoPen);
	QFont legendFont = font();
	legendFont.setPointSize(10);
	ui->customPlot->legend->setFont(legendFont);
	ui->customPlot->setInteractions(QCP::iRangeDrag | QCP::iRangeZoom);
}

Dialog::~Dialog()
{
	delete ui;
}
