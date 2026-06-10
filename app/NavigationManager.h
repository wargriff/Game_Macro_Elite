#pragma once

#include "Enums.h"
#include <QObject>

class NavigationManager : public QObject
{
    Q_OBJECT
public:
    explicit NavigationManager(QObject* parent = nullptr);

    NavSection currentSection() const { return m_section; }
    void navigateTo(NavSection section);

signals:
    void sectionChanged(NavSection section);

private:
    NavSection m_section = NavSection::DeviceCenter;
};
