#pragma once

#include "../../models/DeviceModel.h"
#include <QFrame>

class DockDeviceItem : public QFrame
{
    Q_OBJECT
public:
    explicit DockDeviceItem(const DeviceInfo& info, QWidget* parent = nullptr);
    void setSelected(bool selected);
    const QString& deviceId() const { return m_info.id; }

signals:
    void clicked();

protected:
    void mousePressEvent(QMouseEvent* event) override;

private:
    DeviceInfo m_info;
};
