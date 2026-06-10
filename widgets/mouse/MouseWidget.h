#pragma once

#include <QColor>
#include <QPropertyAnimation>
#include <QRectF>
#include <QString>
#include <QVector>
#include <QWidget>

class MouseWidget : public QWidget
{
    Q_OBJECT
    Q_PROPERTY(qreal pulsePhase READ pulsePhase WRITE setPulsePhase)

public:
    explicit MouseWidget(QWidget* parent = nullptr);

    QString selectedButton() const { return m_selectedButton; }
    void selectButtonByLabel(const QString& label);

signals:
    void buttonSelected(const QString& button);

protected:
    void paintEvent(QPaintEvent* event) override;
    void mousePressEvent(QMouseEvent* event) override;
    void mouseMoveEvent(QMouseEvent* event) override;
    void leaveEvent(QEvent* event) override;

private:
    qreal pulsePhase() const { return m_pulsePhase; }
    void setPulsePhase(qreal v);

    int hitTest(const QPoint& p) const;
    int indexForLabel(const QString& label) const;
    QRectF svgRect() const;
    float svgScale() const;
    QRectF zoneRect(int index, const QRectF& sr, float s) const;
    void applySelection(int index);

    QString m_selectedButton = QStringLiteral("L1");
    int m_selectedIndex = 3;
    int m_hoveredIndex = -1;
    qreal m_pulsePhase = 0.0;
    QPropertyAnimation* m_pulseAnim = nullptr;

    struct BtnZone {
        QRectF rect;
        QString label;
        QColor accent;
        bool macroSide = false;
    };
    QVector<BtnZone> m_zones;

    static constexpr float kSvgW = 420.f;
    static constexpr float kSvgH = 580.f;
};
