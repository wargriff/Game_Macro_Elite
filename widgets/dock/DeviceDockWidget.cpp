#include "DeviceDockWidget.h"
#include "DockDeviceItem.h"
#include "../../core/Constants.h"
#include <QHBoxLayout>

DeviceDockWidget::DeviceDockWidget(DeviceService* service, QWidget* parent)
    : QWidget(parent)
    , m_service(service)
{
    setObjectName(QStringLiteral("deviceDock"));
    setFixedHeight(Gx::Layout::DockHeight);

    auto* layout = new QHBoxLayout(this);
    layout->setContentsMargins(24, 8, 24, 8);
    layout->setSpacing(14);
    layout->addStretch();

    if (!m_service) return;

    const auto& devices = m_service->model().devices();
    for (int i = 0; i < devices.size(); ++i)
    {
        auto* item = new DockDeviceItem(devices.at(i), this);
        item->setSelected(i == 2);
        layout->addWidget(item);
        m_items.push_back(item);

        connect(item, &DockDeviceItem::clicked, this, [this, i]() {
            selectDevice(i);
            emit deviceSelected(i);
        });
    }
    layout->addStretch();
}

void DeviceDockWidget::selectDevice(int index)
{
    if (index < 0 || index >= m_items.size()) return;
    for (int i = 0; i < m_items.size(); ++i)
        m_items[i]->setSelected(i == index);
}
