#pragma once

#include <QObject>
#include <memory>

class ThemeManager;
class SettingsManager;
class NavigationManager;
class MainWindow;

class Application : public QObject
{
    Q_OBJECT
public:
    explicit Application(int& argc, char** argv);
    ~Application() override;

    int run();

private:
    class QApplication* m_app = nullptr;
    std::unique_ptr<ThemeManager> m_theme;
    std::unique_ptr<SettingsManager> m_settings;
    std::unique_ptr<NavigationManager> m_navigation;
    std::unique_ptr<MainWindow> m_mainWindow;
};
