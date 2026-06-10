#include "MouseWidget.h"
#include "../../core/AssetGenerator.h"
#include "../../core/Logger.h"
#include <QPainter>
#include <QMouseEvent>
#include <QSvgRenderer>
#include <QtMath>

namespace
{
constexpr QColor kBlue(52, 152, 219);
constexpr QColor kBlueBright(96, 180, 255);
constexpr QColor kOrange(255, 140, 42);
constexpr QColor kRedMacro(224, 38, 38);
}

MouseWidget::MouseWidget(QWidget* parent) : QWidget(parent)
{
    setObjectName(QStringLiteral("mouseWidget"));
    setMinimumSize(520, 620);
    setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Expanding);
    setMouseTracking(true);

    m_zones = {
        { QRectF(68, 44, 140, 224), QStringLiteral("Gauche"), kBlue, false },
        { QRectF(212, 44, 140, 224), QStringLiteral("Droit"), kBlue, false },
        { QRectF(188, 118, 44, 92), QStringLiteral("Molette"), kBlueBright, false },
        { QRectF(34, 194, 56, 72), QStringLiteral("L1"), kOrange, true },
        { QRectF(34, 264, 56, 72), QStringLiteral("L2"), kOrange, true },
        { QRectF(176, 246, 68, 44), QStringLiteral("DPI"), kBlueBright, false }
    };

    m_pulseAnim = new QPropertyAnimation(this, "pulsePhase", this);
    m_pulseAnim->setDuration(1200);
    m_pulseAnim->setStartValue(0.0);
    m_pulseAnim->setEndValue(1.0);
    m_pulseAnim->setLoopCount(-1);
    m_pulseAnim->start();
}

void MouseWidget::setPulsePhase(qreal v)
{
    m_pulsePhase = v;
    update();
}

float MouseWidget::svgScale() const
{
    const float sx = (width() - 12.f) / kSvgW;
    const float sy = (height() - 36.f) / kSvgH;
    return std::min(sx, sy) * 1.08f;
}

QRectF MouseWidget::svgRect() const
{
    const float s = svgScale();
    return QRectF((width() - kSvgW * s) * 0.5f, (height() - kSvgH * s) * 0.5f - 8.f, kSvgW * s, kSvgH * s);
}

QRectF MouseWidget::zoneRect(int index, const QRectF& sr, float s) const
{
    const BtnZone& z = m_zones[index];
    return QRectF(sr.x() + z.rect.x() * s, sr.y() + z.rect.y() * s, z.rect.width() * s, z.rect.height() * s);
}

int MouseWidget::indexForLabel(const QString& label) const
{
    for (int i = 0; i < m_zones.size(); ++i)
    {
        if (m_zones[i].label.compare(label, Qt::CaseInsensitive) == 0)
            return i;
    }
    return -1;
}

void MouseWidget::selectButtonByLabel(const QString& label)
{
    const int idx = indexForLabel(label);
    if (idx >= 0)
        applySelection(idx);
}

int MouseWidget::hitTest(const QPoint& p) const
{
    const float s = svgScale();
    const QRectF sr = svgRect();

    for (int i = m_zones.size() - 1; i >= 0; --i)
    {
        if (zoneRect(i, sr, s).contains(p))
            return i;
    }
    return -1;
}

void MouseWidget::applySelection(int index)
{
    if (index < 0 || index >= m_zones.size())
        return;

    m_selectedIndex = index;
    m_selectedButton = m_zones[index].label;
    Logger::debug(QStringLiteral("Elite M40 — bouton: %1").arg(m_selectedButton));
    emit buttonSelected(m_selectedButton);
    update();
}

void MouseWidget::paintEvent(QPaintEvent*)
{
    QPainter p(this);
    p.setRenderHint(QPainter::Antialiasing);
    p.fillRect(rect(), QColor(10, 11, 15));

    const float s = svgScale();
    const QRectF sr = svgRect();

    const QString path = AssetGenerator::instance().resolve(QStringLiteral("devices/mouse-elite-m40.svg"));
    QSvgRenderer renderer(path);
    if (renderer.isValid())
        renderer.render(&p, sr);

    const qreal pulse = 0.5 + 0.5 * std::sin(m_pulsePhase * 6.28318);

    for (int i = 0; i < m_zones.size(); ++i)
    {
        const BtnZone& z = m_zones[i];
        const QRectF r = zoneRect(i, sr, s);
        const bool selected = (i == m_selectedIndex);
        const bool hovered = (i == m_hoveredIndex);

        QColor idle = z.macroSide ? QColor(255, 140, 42, 55) : QColor(52, 152, 219, 40);
        if (!selected && !hovered)
        {
            p.setPen(QPen(idle, 1.2, Qt::SolidLine));
            p.setBrush(QColor(idle.red(), idle.green(), idle.blue(), 12));
            p.drawRoundedRect(r.adjusted(2, 2, -2, -2), 8, 8);
            continue;
        }

        QColor accent = z.macroSide ? kRedMacro : z.accent;
        if (z.macroSide && selected)
            accent = kOrange;

        const int alphaFill = selected ? int(55 + 25 * pulse) : 28;
        const int penW = selected ? 3 : 2;

        p.setPen(QPen(accent, penW));
        p.setBrush(QColor(accent.red(), accent.green(), accent.blue(), alphaFill));
        p.drawRoundedRect(r.adjusted(1, 1, -1, -1), 10, 10);

        if (selected)
        {
            p.setPen(QPen(accent, 1, Qt::DotLine));
            p.setBrush(Qt::NoBrush);
            p.drawRoundedRect(r.adjusted(-4, -4, 4, 4), 12, 12);
        }
    }

    p.setPen(QColor(180, 190, 210));
    QFont f = p.font();
    f.setPixelSize(13);
    f.setBold(true);
    p.setFont(f);

    const BtnZone& sel = m_zones[m_selectedIndex];
    const QString status = sel.macroSide
        ? QStringLiteral("Elite M40 — %1 (macro / toggle)").arg(sel.label)
        : QStringLiteral("Elite M40 — Bouton %1").arg(sel.label);
    p.drawText(QRectF(0, height() - 34, width(), 24), Qt::AlignCenter, status);
}

void MouseWidget::mousePressEvent(QMouseEvent* e)
{
    const int idx = hitTest(e->pos());
    if (idx >= 0)
        applySelection(idx);
}

void MouseWidget::mouseMoveEvent(QMouseEvent* e)
{
    const int idx = hitTest(e->pos());
    if (idx != m_hoveredIndex)
    {
        m_hoveredIndex = idx;
        setCursor(idx >= 0 ? Qt::PointingHandCursor : Qt::ArrowCursor);
        update();
    }
}

void MouseWidget::leaveEvent(QEvent*)
{
    m_hoveredIndex = -1;
    unsetCursor();
    update();
}
