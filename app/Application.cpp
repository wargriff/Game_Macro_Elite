#include "Application.h"
#include "ThemeManager.h"
#include "SettingsManager.h"
#include "NavigationManager.h"
#include "../windows/MainWindow.h"
#include "../core/Logger.h"
#include "../core/AssetGenerator.h"
#include "../services/MacroEngine.h"
#include "../core/DebugManager.h"
#include <QApplication>
#include <QCoreApplication>
#include <QDir>

Application::Application(int& argc, char** argv)
{
    m_app = new QApplication(argc, argv);
    QApplication::setApplicationName(QStringLiteral("Game_macro_elite"));
    QApplication::setApplicationDisplayName(QStringLiteral("Game_macro_elite"));
    QApplication::setOrganizationName(QStringLiteral("GameX"));

    DebugManager::instance().initialize(argc, argv);

    m_theme = std::make_unique<ThemeManager>();
    m_settings = std::make_unique<SettingsManager>();
    m_navigation = std::make_unique<NavigationManager>();
}

Application::~Application()
{
    delete m_app;
}

int Application::run()
{
    Logger::info(QStringLiteral("Demarrage Game_macro_elite"));

#ifdef GAMEX_SOURCE_DIR
    const QString resourcesRoot = QDir(QStringLiteral(GAMEX_SOURCE_DIR)).filePath(QStringLiteral("resources"));
#else
    const QString resourcesRoot = QDir(QCoreApplication::applicationDirPath()).filePath(QStringLiteral("resources"));
#endif
    AssetGenerator::instance().ensureAll(resourcesRoot);

    m_theme->applyGlobalStyle(m_app);
    m_mainWindow = std::make_unique<MainWindow>(m_navigation.get());
    MacroEngine::instance().start();
    m_mainWindow->show();
    return m_app->exec();
}
