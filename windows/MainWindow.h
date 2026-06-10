#pragma once

#include "../core/Enums.h"
#include <QWidget>

class MainWindow : public QWidget
{
    Q_OBJECT
public:
    explicit MainWindow(class NavigationManager* nav, QWidget* parent = nullptr);

private:
    void buildPages();
    void onSectionChanged(NavSection section);
    void onDockDeviceSelected(int index);

    NavigationManager* m_nav = nullptr;
    class QStackedWidget* m_stack = nullptr;
    class TitleBarWidget* m_titleBar = nullptr;
    class DeviceService* m_deviceService = nullptr;
    class DeviceCenterPage* m_deviceCenter = nullptr;
    class DeviceDockWidget* m_dock = nullptr;
};
