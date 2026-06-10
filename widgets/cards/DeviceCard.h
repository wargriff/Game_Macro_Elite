#pragma once

#include <QFrame>

class DeviceCard : public QFrame
{
    Q_OBJECT
public:
    explicit DeviceCard(const QString& name, QWidget* parent = nullptr);
};
