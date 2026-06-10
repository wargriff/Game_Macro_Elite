#pragma once

#include "../../services/DeviceService.h"
#include <QVector>
#include <QWidget>

class DockDeviceItem;

class DeviceDockWidget : public QWidget
{
    Q_OBJECT
public:
    explicit DeviceDockWidget(DeviceService* service, QWidget* parent = nullptr);
    void selectDevice(int index);

signals:
    void deviceSelected(int index);

private:
    DeviceService* m_service = nullptr;
    QVector<DockDeviceItem*> m_items;
};
