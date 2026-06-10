#include "DockDeviceItem.h"

#include "../../core/AssetGenerator.h"
#include "../../core/Enums.h"

#include <QLabel>
#include <QMouseEvent>
#include <QStyle>

DockDeviceItem::DockDeviceItem(const DeviceInfo& info, QWidget* parent)
    : QFrame(parent)
    , m_info(info)
{
    setObjectName(QStringLiteral("dockItem"));
    setFixedSize(68, 68);
    setCursor(Qt::PointingHandCursor);
    setToolTip(info.name + (info.temperature != QStringLiteral("—") ? QStringLiteral(" — ") + info.temperature : QString()));

    auto* icon = new QLabel(this);
    icon->setGeometry(10, 6, 48, 48);
    icon->setAlignment(Qt::AlignCenter);
    icon->setObjectName(QStringLiteral("dockIcon"));
    icon->setAttribute(Qt::WA_TransparentForMouseEvents);
    const QString asset = deviceIconAsset(info.id);
    icon->setPixmap(AssetGenerator::instance().pixmap(asset, QSize(48, 48)));
    icon->setScaledContents(true);

    if (info.connected)
    {
        auto* dot = new QLabel(this);
        dot->setFixedSize(9, 9);
        dot->move(50, 50);
        dot->setAttribute(Qt::WA_TransparentForMouseEvents);
        dot->setStyleSheet(QStringLiteral("background: #2ecc71; border-radius: 5px;"));
    }

    if (!info.temperature.isEmpty() && info.temperature != QStringLiteral("—"))
    {
        auto* temp = new QLabel(info.temperature, this);
        temp->setObjectName(QStringLiteral("dockTemp"));
        temp->setAlignment(Qt::AlignCenter);
        temp->setAttribute(Qt::WA_TransparentForMouseEvents);
        temp->setGeometry(0, 52, 68, 14);
    }
}

void DockDeviceItem::mousePressEvent(QMouseEvent* event)
{
    if (event->button() == Qt::LeftButton)
        emit clicked();
    QFrame::mousePressEvent(event);
}

void DockDeviceItem::setSelected(bool selected)
{
    setProperty("selected", selected);
    style()->unpolish(this);
    style()->polish(this);
}
