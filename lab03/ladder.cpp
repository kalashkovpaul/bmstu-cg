#include "ladder.h"
#include "ui_ladder.h"

Ladder::Ladder(QVector<QVector<double>>& data, QWidget *parent) :
    QDialog(parent),
    ui(new Ui::Ladder)
{
    ui->setupUi(this);

    ui->DDAPlot->addGraph();
    ui->DDAPlot->graph(0)->setPen(QPen(QColor(0xff, 0, 0), 2));

    const int maxAngle = 180;
    QVector<double> x(maxAngle);
    for (int i = 0; i != maxAngle; ++i)
        x[i] = i;

    ui->DDAPlot->xAxis2->setVisible(true);
    ui->DDAPlot->xAxis2->setLabel("Угол наклона");
    ui->DDAPlot->xAxis2->setTickLabels(true);
    ui->DDAPlot->yAxis2->setVisible(true);
    ui->DDAPlot->yAxis2->setLabel("Количество ступенек");
    ui->DDAPlot->yAxis2->setTickLabels(true);

    connect(ui->DDAPlot->xAxis, SIGNAL(rangeChanged(QCPRange)), ui->DDAPlot->xAxis2, SLOT(setRange(QCPRange)));
    connect(ui->DDAPlot->yAxis, SIGNAL(rangeChanged(QCPRange)), ui->DDAPlot->yAxis2, SLOT(setRange(QCPRange)));

    ui->DDAPlot->graph(0)->setData(x, data[0]);
    ui->DDAPlot->graph(0)->rescaleAxes();
    ui->DDAPlot->plotLayout()->insertRow(0);
    ui->DDAPlot->plotLayout()->addElement(0, 0, new QCPTextElement(ui->DDAPlot, "ЦДА", QFont("sans", 12, QFont::Bold)));
    ui->DDAPlot->graph(0)->setName("ЦДА");

    ui->BresenhemPlot->addGraph();
    ui->BresenhemPlot->graph(0)->setPen(QPen(QColor(0xff, 0, 0), 2));
    ui->BresenhemPlot->xAxis2->setVisible(true);
    ui->BresenhemPlot->xAxis2->setLabel("Угол наклона");
    ui->BresenhemPlot->xAxis2->setTickLabels(true);
    ui->BresenhemPlot->yAxis2->setVisible(true);
    ui->BresenhemPlot->yAxis2->setLabel("Количество ступенек");
    ui->BresenhemPlot->yAxis2->setTickLabels(true);

    connect(ui->BresenhemPlot->xAxis, SIGNAL(rangeChanged(QCPRange)), ui->BresenhemPlot->xAxis2, SLOT(setRange(QCPRange)));
    connect(ui->BresenhemPlot->yAxis, SIGNAL(rangeChanged(QCPRange)), ui->BresenhemPlot->yAxis2, SLOT(setRange(QCPRange)));

    ui->BresenhemPlot->graph(0)->setData(x, data[1]);
    ui->BresenhemPlot->graph(0)->rescaleAxes();
    ui->BresenhemPlot->plotLayout()->insertRow(0);
    ui->BresenhemPlot->plotLayout()->addElement(0, 0, new QCPTextElement(ui->BresenhemPlot, "Брезенхем (с действительными данными)", QFont("sans", 12, QFont::Bold)));

    ui->BresenhemIntegerPlot->addGraph();
    ui->BresenhemIntegerPlot->graph(0)->setPen(QPen(QColor(0xff, 0, 0), 2));
    ui->BresenhemIntegerPlot->xAxis2->setVisible(true);
    ui->BresenhemIntegerPlot->xAxis2->setLabel("Угол наклона");
    ui->BresenhemIntegerPlot->xAxis2->setTickLabels(true);
    ui->BresenhemIntegerPlot->yAxis2->setVisible(true);
    ui->BresenhemIntegerPlot->yAxis2->setLabel("Количество ступенек");
    ui->BresenhemIntegerPlot->yAxis2->setTickLabels(true);

    connect(ui->BresenhemIntegerPlot->xAxis, SIGNAL(rangeChanged(QCPRange)), ui->BresenhemIntegerPlot->xAxis2, SLOT(setRange(QCPRange)));
    connect(ui->BresenhemIntegerPlot->yAxis, SIGNAL(rangeChanged(QCPRange)), ui->BresenhemIntegerPlot->yAxis2, SLOT(setRange(QCPRange)));

    ui->BresenhemIntegerPlot->graph(0)->setData(x, data[1]);
    ui->BresenhemIntegerPlot->graph(0)->rescaleAxes();
    ui->BresenhemIntegerPlot->plotLayout()->insertRow(0);
    ui->BresenhemIntegerPlot->plotLayout()->addElement(0, 0, new QCPTextElement(ui->BresenhemIntegerPlot, "Брезенхем (с целыми числами)", QFont("sans", 12, QFont::Bold)));


    ui->BresenhemAntiPlot->addGraph();
    ui->BresenhemAntiPlot->graph(0)->setPen(QPen(QColor(0xff, 0, 0), 2));
    ui->BresenhemAntiPlot->xAxis2->setVisible(true);
    ui->BresenhemAntiPlot->xAxis2->setLabel("Угол наклона");
    ui->BresenhemAntiPlot->xAxis2->setTickLabels(true);
    ui->BresenhemAntiPlot->yAxis2->setVisible(true);
    ui->BresenhemAntiPlot->yAxis2->setLabel("Количество ступенек");
    ui->BresenhemAntiPlot->yAxis2->setTickLabels(true);

    connect(ui->BresenhemAntiPlot->xAxis, SIGNAL(rangeChanged(QCPRange)), ui->BresenhemAntiPlot->xAxis2, SLOT(setRange(QCPRange)));
    connect(ui->BresenhemAntiPlot->yAxis, SIGNAL(rangeChanged(QCPRange)), ui->BresenhemAntiPlot->yAxis2, SLOT(setRange(QCPRange)));

    ui->BresenhemAntiPlot->graph(0)->setData(x, data[1]);
    ui->BresenhemAntiPlot->graph(0)->rescaleAxes();
    ui->BresenhemAntiPlot->plotLayout()->insertRow(0);
    ui->BresenhemAntiPlot->plotLayout()->addElement(0, 0, new QCPTextElement(ui->BresenhemAntiPlot, "Брезенхем (с устранением ступенчатости)", QFont("sans", 12, QFont::Bold)));

}

Ladder::~Ladder()
{
    delete ui;
}
