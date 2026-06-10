#pragma once

#include "KeyWidget.h"
#include "../../core/Enums.h"
#include <QPainter>
#include <QWidget>
#include <QVector>

class KeyboardWidget : public QWidget
{
    Q_OBJECT
public:
    explicit KeyboardWidget(QWidget* parent = nullptr);

    QString selectedKey() const { return m_selectedLabel; }

signals:
    void keySelected(const QString& label);

protected:
    void paintEvent(QPaintEvent* event) override;
    void resizeEvent(QResizeEvent* event) override;
    void mousePressEvent(QMouseEvent* event) override;
    void mouseMoveEvent(QMouseEvent* event) override;
    void leaveEvent(QEvent* event) override;

private:
    void build60Layout();
    int hitTest(const QPoint& p) const;
    void drawPlate(QPainter& p, const QRectF& plate);
    void drawKey(QPainter& p, const KeyData& k, int index);
    QRectF contentRect() const;
    float scaleFactor() const;
    QPointF layoutOffset() const;
    QRectF scaledRect(const QRectF& r) const;

    QVector<KeyData> m_keys;
    int m_selectedIndex = 0;
    int m_hoveredIndex = -1;
    QString m_selectedLabel = QStringLiteral("W");
};
