#pragma once
#include <QPaintEvent>
#include <QWidget>
class RamChartWidget : public QWidget {
public:
    explicit RamChartWidget(QWidget* parent = nullptr);
protected:
    void paintEvent(QPaintEvent*) override;
};
