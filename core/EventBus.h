#pragma once

#include "Enums.h"
#include <QObject>

class EventBus : public QObject
{
    Q_OBJECT
public:
    static EventBus& instance();

signals:
    void sectionChanged(NavSection section);
    void deviceTabChanged(DeviceTab tab);
    void keySelected(const QString& label);
    void profileChanged(int index);
    void macroMasterChanged(bool enabled);
    void rgbEffectChanged(RgbEffect effect);

private:
    explicit EventBus(QObject* parent = nullptr) : QObject(parent) {}
};
