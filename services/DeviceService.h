#pragma once

#include "../models/DeviceModel.h"
#include <QObject>

class DeviceService : public QObject
{
public:
    explicit DeviceService(QObject* parent = nullptr);
    DeviceModel& model() { return m_model; }
    const DeviceModel& model() const { return m_model; }

private:
    DeviceModel m_model;
};
