#include "MainWindow.h"
#include "../widgets/sidebar/SidebarWidget.h"
#include "../widgets/titlebar/TitleBarWidget.h"
#include "../widgets/dock/DeviceDockWidget.h"
#include "../pages/Dashboard/DashboardPage.h"
#include "../pages/DeviceCenter/DeviceCenterPage.h"
#include "../pages/MacroStudio/MacroStudioPage.h"
#include "../pages/MacroLibrary/MacroLibraryPage.h"
#include "../pages/ProfileManager/ProfileManagerPage.h"
#include "../pages/LightingEngine/LightingPage.h"
#include "../pages/Analytics/AnalyticsPage.h"
#include "../pages/MobileCommand/MobileCommandPage.h"
#include "../services/DeviceService.h"
#include "../app/NavigationManager.h"
#include "../core/Constants.h"
#include "../core/Enums.h"
#include "../core/AppState.h"
#include <QHBoxLayout>
#include <QStackedWidget>
#include <QVBoxLayout>

MainWindow::MainWindow(NavigationManager* nav, QWidget* parent)
    : QWidget(parent)
    , m_nav(nav)
{
    setObjectName(QStringLiteral("mainWindow"));
    resize(Gx::Layout::WindowWidth, Gx::Layout::WindowHeight);
    setWindowTitle(Gx::App::Name);

    m_deviceService = new DeviceService(this);

    auto* root = new QHBoxLayout(this);
    root->setContentsMargins(0, 0, 0, 0);
    root->setSpacing(0);

    auto* sidebar = new SidebarWidget(m_nav, this);
    root->addWidget(sidebar);

    auto* mainCol = new QVBoxLayout();
    mainCol->setContentsMargins(0, 0, 0, 0);
    mainCol->setSpacing(0);

    m_titleBar = new TitleBarWidget(this);
    mainCol->addWidget(m_titleBar);

    m_stack = new QStackedWidget(this);
    buildPages();
    mainCol->addWidget(m_stack, 1);

    m_dock = new DeviceDockWidget(m_deviceService, this);
    mainCol->addWidget(m_dock);

    root->addLayout(mainCol, 1);

    connect(m_nav, &NavigationManager::sectionChanged, this, &MainWindow::onSectionChanged);
    connect(m_dock, &DeviceDockWidget::deviceSelected, this, &MainWindow::onDockDeviceSelected);
    connect(m_titleBar, &TitleBarWidget::closeClicked, this, &QWidget::close);
    connect(m_titleBar, &TitleBarWidget::minimizeClicked, this, &QWidget::showMinimized);

    onSectionChanged(NavSection::DeviceCenter);
}

void MainWindow::buildPages()
{
    m_stack->addWidget(new DashboardPage(this));           // 0 MissionControl / SettingsHub
    m_deviceCenter = new DeviceCenterPage(this);
    m_stack->addWidget(m_deviceCenter);                    // 1 DeviceCenter
    m_stack->addWidget(new MacroStudioPage(this));        // 2 MacroStudio
    m_stack->addWidget(new MacroLibraryPage(this));        // 3 MacroLibrary
    m_stack->addWidget(new ProfileManagerPage(this));      // 4 ProfileManager
    m_stack->addWidget(new DashboardPage(this));           // 5 ActivityMonitor
    m_stack->addWidget(new AnalyticsPage(this));           // 6 AnalyticsCenter
    m_stack->addWidget(new MobileCommandPage(this));       // 7 MobileCommand
    m_stack->addWidget(new LightingPage(this));            // 8 LightingEngine
}

void MainWindow::onSectionChanged(NavSection section)
{
    AppStateStore::instance().state().currentSection = section;
    int index = 0;
    switch (section)
    {
    case NavSection::MissionControl:
    case NavSection::SettingsHub:     index = 0; break;
    case NavSection::DeviceCenter:    index = 1; break;
    case NavSection::MacroStudio:     index = 2; break;
    case NavSection::MacroLibrary:    index = 3; break;
    case NavSection::ProfileManager: index = 4; break;
    case NavSection::ActivityMonitor: index = 5; break;
    case NavSection::AnalyticsCenter: index = 6; break;
    case NavSection::MobileCommand:   index = 7; break;
    case NavSection::LightingEngine:  index = 8; break;
    }
    m_stack->setCurrentIndex(index);
}

void MainWindow::onDockDeviceSelected(int index)
{
    if (!m_deviceService || !m_dock) return;

    AppStateStore::instance().state().selectedDeviceIndex = index;
    const auto& device = m_deviceService->model().deviceAt(index);

    if (!m_nav) return;

    const QString& id = device.id;
    if (id == QStringLiteral("kb") || id == QStringLiteral("ms"))
    {
        m_nav->navigateTo(NavSection::DeviceCenter);
        if (m_deviceCenter)
            m_deviceCenter->focusDevice(id);
    }
    else if (id == QStringLiteral("hs") || id == QStringLiteral("aio"))
    {
        m_nav->navigateTo(NavSection::LightingEngine);
    }
    else
    {
        m_nav->navigateTo(NavSection::ActivityMonitor);
    }
}
