#pragma once

#include <QString>
#include <QVector>

struct DeviceInfo
{
    QString id;
    QString name;
    QString icon;
    bool connected = true;
    bool rgbActive = false;
    QString battery;
    QString firmware;
    QString polling;
    QString dpi;
    QString temperature;
};

class DeviceModel
{
public:
    DeviceModel();
    const QVector<DeviceInfo>& devices() const { return m_devices; }
    DeviceInfo& deviceAt(int index);
    const DeviceInfo& deviceAt(int index) const;

private:
    QVector<DeviceInfo> m_devices;
};
