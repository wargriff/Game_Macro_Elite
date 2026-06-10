#include "KeyboardWidget.h"
#include "../../core/Logger.h"
#include <QPainter>
#include <QMouseEvent>
#include <QResizeEvent>
#include <QtMath>

namespace
{
constexpr int kPlatePad = 10;
constexpr float kLayoutW = 612.f;
constexpr float kLayoutH = 220.f;

constexpr QColor kKeyFill(22, 24, 32);
constexpr QColor kKeyBorder(52, 152, 219);       // bleu
constexpr QColor kKeyBorderHover(96, 180, 255);
constexpr QColor kKeyBorderSelected(74, 168, 255);
constexpr QColor kKeyText(220, 228, 240);
}

KeyboardWidget::KeyboardWidget(QWidget* parent) : QWidget(parent)
{
    setObjectName(QStringLiteral("keyboardWidget"));
    setMinimumSize(780, 300);
    setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Expanding);
    setMouseTracking(true);
    build60Layout();
}

QRectF KeyboardWidget::contentRect() const
{
    return QRectF(kPlatePad, kPlatePad, width() - kPlatePad * 2.f, height() - kPlatePad * 2.f);
}

float KeyboardWidget::scaleFactor() const
{
    const QRectF area = contentRect();
    const float sx = (area.width() - 16.f) / kLayoutW;
    const float sy = (area.height() - 16.f) / kLayoutH;
    return std::min(sx, sy);
}

QPointF KeyboardWidget::layoutOffset() const
{
    const QRectF area = contentRect();
    const float s = scaleFactor();
    const float drawnW = kLayoutW * s;
    const float drawnH = kLayoutH * s;
    return QPointF(area.left() + 8 + (area.width() - 16 - drawnW) * 0.5f,
                   area.top() + 8 + (area.height() - 16 - drawnH) * 0.5f);
}

QRectF KeyboardWidget::scaledRect(const QRectF& r) const
{
    const float s = scaleFactor();
    const QPointF off = layoutOffset();
    return QRectF(off.x() + r.x() * s, off.y() + r.y() * s, r.width() * s, r.height() * s);
}

void KeyboardWidget::build60Layout()
{
    m_keys.clear();
    const float kw = 38.f, kh = 38.f, g = 4.f;
    const float x0 = 12.f, y0 = 18.f;

    auto add = [&](float x, float y, float w, const QString& lbl, KeyAssignment a, float hue) {
        KeyData k;
        k.label = lbl;
        k.rect = QRectF(x, y, w * kw + (w - 1) * g, kh);
        k.assignment = a;
        k.hue = hue;
        m_keys.push_back(k);
    };

    float x = x0, y = y0;
    const char* r1[] = {"Esc","1","2","3","4","5","6","7","8","9","0","-","=","Bksp"};
    float w1[] = {1,1,1,1,1,1,1,1,1,1,1,1,1,1.8f};
    for (int i = 0; i < 14; ++i) { add(x, y, w1[i], r1[i], KeyAssignment::Normal, 0.f); x += w1[i]*kw + w1[i]*g; }
    y += kh + g; x = x0;
    add(x,y,1.3f,"Tab",KeyAssignment::Normal,0.f); x += 1.3f*kw+ g;
    const char* r2[] = {"Q","W","E","R","T","Y","U","I","O","P","[","]","\\"};
    for (int i = 0; i < 13; ++i) {
        KeyAssignment a = (QString(r2[i]) == QStringLiteral("W")) ? KeyAssignment::Macro : KeyAssignment::Normal;
        add(x,y,1,r2[i],a,0.f); x += kw+g;
    }
    y += kh + g; x = x0;
    add(x,y,1.5f,"Caps",KeyAssignment::Normal,0.f); x += 1.5f*kw+g;
    const char* r3[] = {"A","S","D","F","G","H","J","K","L",";","'","Enter"};
    float w3[] = {1,1,1,1,1,1,1,1,1,1,1,2.f};
    for (int i = 0; i < 12; ++i) {
        KeyAssignment a = (QString(r3[i]) == QStringLiteral("F")) ? KeyAssignment::Function : KeyAssignment::Normal;
        add(x,y,w3[i],r3[i],a,0.f); x += w3[i]*kw+w3[i]*g;
    }
    y += kh + g; x = x0;
    add(x,y,1.8f,"Shift",KeyAssignment::Normal,0.f); x += 1.8f*kw+g;
    const char* r4[] = {"Z","X","C","V","B","N","M",",",".","/","Shift"};
    float w4[] = {1,1,1,1,1,1,1,1,1,1,2.f};
    for (int i = 0; i < 11; ++i) { add(x,y,w4[i],r4[i],KeyAssignment::Normal,0.f); x += w4[i]*kw+w4[i]*g; }
    y += kh + g; x = x0;
    add(x,y,1.2f,"Ctrl",KeyAssignment::Normal,0.f); x += 1.2f*kw+g;
    add(x,y,1,"Win",KeyAssignment::Function,0.f); x += kw+g;
    add(x,y,1,"Alt",KeyAssignment::Normal,0.f); x += kw+g;
    add(x,y,5,"Space",KeyAssignment::Normal,0.f); x += 5*kw+5*g;
    add(x,y,1,"Alt",KeyAssignment::Normal,0.f); x += kw+g;
    add(x,y,1.2f,"Ctrl",KeyAssignment::Normal,0.f);

    for (int i = 0; i < m_keys.size(); ++i)
        if (m_keys[i].label == QStringLiteral("W")) { m_selectedIndex = i; break; }
}

int KeyboardWidget::hitTest(const QPoint& p) const
{
    for (int i = m_keys.size() - 1; i >= 0; --i)
        if (scaledRect(m_keys[i].rect).contains(p)) return i;
    return -1;
}

void KeyboardWidget::drawPlate(QPainter& p, const QRectF& plate)
{
    QLinearGradient body(plate.topLeft(), plate.bottomLeft());
    body.setColorAt(0, QColor(20, 22, 30));
    body.setColorAt(1, QColor(12, 13, 18));
    p.setBrush(body);
    p.setPen(QPen(QColor(42, 46, 58), 1.2));
    p.drawRoundedRect(plate, 12, 12);
}

void KeyboardWidget::drawKey(QPainter& p, const KeyData& k, int index)
{
    const QRectF r = scaledRect(k.rect);
    const bool selected = index == m_selectedIndex;
    const bool hovered = index == m_hoveredIndex;

    QColor border = kKeyBorder;
    if (selected) border = kKeyBorderSelected;
    else if (hovered) border = kKeyBorderHover;

    const float penW = selected ? 2.4f : (hovered ? 2.0f : 1.6f);

    p.setBrush(kKeyFill);
    p.setPen(QPen(border, penW));
    p.drawRoundedRect(r, 5, 5);

    p.setPen(kKeyText);
    QFont f = p.font();
    const float s = scaleFactor();
    f.setPixelSize(int((k.label.length() > 3 ? 10 : 12) * std::max(0.85f, s)));
    f.setBold(selected);
    p.setFont(f);
    p.drawText(r, Qt::AlignCenter, k.label);
}

void KeyboardWidget::paintEvent(QPaintEvent*)
{
    QPainter p(this);
    p.setRenderHint(QPainter::Antialiasing);
    p.setRenderHint(QPainter::TextAntialiasing);
    p.fillRect(rect(), QColor(10, 11, 15));

    drawPlate(p, contentRect());

    for (int i = 0; i < m_keys.size(); ++i)
        drawKey(p, m_keys[i], i);
}

void KeyboardWidget::resizeEvent(QResizeEvent* e)
{
    QWidget::resizeEvent(e);
    update();
}

void KeyboardWidget::mousePressEvent(QMouseEvent* e)
{
    const int idx = hitTest(e->pos());
    if (idx >= 0)
    {
        m_selectedIndex = idx;
        m_selectedLabel = m_keys[idx].label;
        Logger::debug(QStringLiteral("Touche selectionnee: %1").arg(m_selectedLabel));
        emit keySelected(m_selectedLabel);
        update();
    }
}

void KeyboardWidget::mouseMoveEvent(QMouseEvent* e)
{
    const int idx = hitTest(e->pos());
    if (idx != m_hoveredIndex) { m_hoveredIndex = idx; update(); }
}

void KeyboardWidget::leaveEvent(QEvent*)
{
    m_hoveredIndex = -1;
    update();
}
