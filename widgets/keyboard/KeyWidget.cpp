#include "KeyWidget.h"
#include <QColor>
#include <QtMath>

QColor KeyWidget::colorForAssignment(KeyAssignment a, float hue, float phase)
{
    const float h = std::fmod(hue + phase * 0.08f, 1.f);
    switch (a)
    {
    case KeyAssignment::Macro:
        return QColor::fromHsvF(0.f, 0.92f, 1.f);
    case KeyAssignment::Function:
        return QColor::fromHsvF(0.08f, 0.85f, 0.95f);
    case KeyAssignment::Disabled:
        return QColor(48, 48, 56);
    default:
        return QColor::fromHsvF(h, 0.88f, 0.98f);
    }
}

QColor KeyWidget::glowForAssignment(KeyAssignment a, float hue, float phase)
{
    const QColor base = colorForAssignment(a, hue, phase);
    QColor glow = base;
    glow.setAlpha(140);
    return glow;
}

QColor KeyWidget::capTopColor(const QColor& base)
{
    return base.lighter(115);
}

QColor KeyWidget::capBottomColor(const QColor& base)
{
    return base.darker(135);
}
