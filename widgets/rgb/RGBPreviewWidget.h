#pragma once

#include <QWidget>

class RGBPreviewWidget : public QWidget
{
    Q_OBJECT
public:
    explicit RGBPreviewWidget(QWidget* parent = nullptr);

protected:
    void paintEvent(QPaintEvent* event) override;
};
