#include "RGBPreviewWidget.h"
#include "../../core/AssetGenerator.h"
#include <QPainter>
#include <QSvgRenderer>

RGBPreviewWidget::RGBPreviewWidget(QWidget* parent) : QWidget(parent)
{
    setFixedSize(140, 56);
    setObjectName(QStringLiteral("rgbPreview"));
}

void RGBPreviewWidget::paintEvent(QPaintEvent*)
{
    QPainter p(this);
    p.setRenderHint(QPainter::Antialiasing);

    const QString path = AssetGenerator::instance().resolve(QStringLiteral("previews/keyboard-rgb-preview.svg"));
    QSvgRenderer renderer(path);
    if (renderer.isValid())
    {
        p.setPen(QPen(QColor(42, 42, 54), 1));
        p.setBrush(QColor(18, 18, 24));
        p.drawRoundedRect(rect().adjusted(0, 0, -1, -1), 8, 8);
        renderer.render(&p, rect().adjusted(4, 4, -4, -4));
        return;
    }

    for (int x = 0; x < width(); ++x)
    {
        QColor c = QColor::fromHsv((x * 360 / width()) % 360, 200, 220);
        p.fillRect(x, 0, 1, height(), c);
    }
}
