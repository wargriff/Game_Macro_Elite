#pragma once

#include "../../core/Enums.h"
#include <QColor>
#include <QRectF>
#include <QString>

struct KeyData
{
    QString label;
    QRectF rect;
    KeyAssignment assignment = KeyAssignment::Normal;
    float hue = 0.f;
};

class KeyWidget
{
public:
    static QColor colorForAssignment(KeyAssignment a, float hue, float phase);
    static QColor glowForAssignment(KeyAssignment a, float hue, float phase);
    static QColor capTopColor(const QColor& base);
    static QColor capBottomColor(const QColor& base);
};
