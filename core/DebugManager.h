#pragma once

#include <QString>

class DebugManager
{
public:
    static DebugManager& instance();

    void initialize(int argc, char** argv);
    bool isEnabled() const { return m_enabled; }

    QString logFilePath() const { return m_logPath; }

private:
    DebugManager() = default;
    void installMessageHandler();
    void attachConsoleIfNeeded();

    bool m_enabled = false;
    QString m_logPath;
};
