#pragma once

#include "../../core/Enums.h"
#include <QPushButton>
#include <QString>

class SidebarButton : public QPushButton
{
    Q_OBJECT
public:
    explicit SidebarButton(NavSection section, const QString& iconAsset, const QString& label, QWidget* parent = nullptr);
    NavSection section() const { return m_section; }
    void setActive(bool active);

private:
    NavSection m_section;
};
