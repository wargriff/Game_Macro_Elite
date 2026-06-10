#pragma once

#include "../../core/Enums.h"
#include <QWidget>
#include <QVector>

class NavigationManager;
class SidebarButton;

class SidebarWidget : public QWidget
{
    Q_OBJECT
public:
    explicit SidebarWidget(NavigationManager* nav, QWidget* parent = nullptr);

signals:
    void navigateRequested(NavSection section);

private:
    void buildUi();

    NavigationManager* m_nav = nullptr;
    QVector<SidebarButton*> m_buttons;
};
