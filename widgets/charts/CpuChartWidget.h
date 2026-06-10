#pragma once
#include <QPaintEvent>
#include <QWidget>
class CpuChartWidget : public QWidget {
public:
    explicit CpuChartWidget(QWidget* parent = nullptr);
protected:
    void paintEvent(QPaintEvent*) override;
};
