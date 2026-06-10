#pragma once

#include "../../services/RGBService.h"
#include <QWidget>

class RGBPanelWidget : public QWidget
{
    Q_OBJECT
public:
    explicit RGBPanelWidget(RGBService* rgb, QWidget* parent = nullptr);

private:
    RGBService* m_rgb = nullptr;
};
