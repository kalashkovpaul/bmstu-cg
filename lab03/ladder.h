#ifndef LADDER_H
#define LADDER_H

#include <QDialog>

namespace Ui {
class Ladder;
}

class Ladder : public QDialog
{
    Q_OBJECT

public:
    explicit Ladder(QVector<QVector<double>>& data, QWidget *parent = nullptr);
    ~Ladder();

private:
    Ui::Ladder *ui;
};

#endif // LADDER_H
