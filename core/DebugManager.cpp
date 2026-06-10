#include "DebugManager.h"
#include "Logger.h"
#include <QCoreApplication>
#include <QDateTime>
#include <QDir>
#include <QFile>
#include <QLoggingCategory>
#include <QMutex>
#include <QTextStream>

#ifdef GAMEX_DEBUG
#include <cstdio>
#ifdef _WIN32
#include <Windows.h>
#endif
#endif

namespace
{
QMutex g_logMutex;
QString g_logPath;
bool g_debugEnabled = false;

void writeLogLine(const QString& level, const QString& msg)
{
    QMutexLocker lock(&g_logMutex);
    if (g_logPath.isEmpty())
        return;

    QFile file(g_logPath);
    if (!file.open(QIODevice::WriteOnly | QIODevice::Append | QIODevice::Text))
        return;

    QTextStream out(&file);
    out << QDateTime::currentDateTime().toString(QStringLiteral("yyyy-MM-dd hh:mm:ss.zzz"))
        << " [" << level << "] " << msg << "\n";
}

void qtMessageHandler(QtMsgType type, const QMessageLogContext& ctx, const QString& msg)
{
    Q_UNUSED(ctx);
    QString level = QStringLiteral("INFO");
    switch (type)
    {
    case QtDebugMsg:   level = QStringLiteral("DEBUG"); break;
    case QtInfoMsg:    level = QStringLiteral("INFO"); break;
    case QtWarningMsg: level = QStringLiteral("WARN"); break;
    case QtCriticalMsg:level = QStringLiteral("ERROR"); break;
    case QtFatalMsg:   level = QStringLiteral("FATAL"); break;
    }

    if (g_debugEnabled || type >= QtWarningMsg)
        writeLogLine(level, msg);

#ifdef GAMEX_DEBUG
    fprintf(stderr, "[%s] %s\n", qPrintable(level), qPrintable(msg));
#endif

    if (type == QtFatalMsg)
        abort();
}
}

DebugManager& DebugManager::instance()
{
    static DebugManager mgr;
    return mgr;
}

void DebugManager::initialize(int argc, char** argv)
{
    for (int i = 1; i < argc; ++i)
    {
        const QString arg = QString::fromLocal8Bit(argv[i]);
        if (arg == QStringLiteral("--debug") || arg == QStringLiteral("-d"))
            m_enabled = true;
    }

#ifdef GAMEX_DEBUG
    m_enabled = true;
#endif

    g_debugEnabled = m_enabled;

    const QString logDir = QCoreApplication::applicationDirPath() + QStringLiteral("/logs");
    QDir().mkpath(logDir);
    m_logPath = logDir + QStringLiteral("/gamex.log");
    g_logPath = m_logPath;

    installMessageHandler();
    attachConsoleIfNeeded();

    if (m_enabled)
    {
        Logger::info(QStringLiteral("Mode DEBUG actif — log: %1").arg(m_logPath));
        Logger::debug(QStringLiteral("Version %1 — build debug").arg(QStringLiteral("1.2.0")));
    }
}

void DebugManager::installMessageHandler()
{
    qInstallMessageHandler(qtMessageHandler);
}

void DebugManager::attachConsoleIfNeeded()
{
#ifdef GAMEX_DEBUG
#ifdef _WIN32
    if (AllocConsole())
    {
        freopen("CONOUT$", "w", stdout);
        freopen("CONOUT$", "w", stderr);
        SetConsoleTitleW(L"GAMEX DEBUG");
    }
#endif
#else
    Q_UNUSED(m_enabled);
#endif
}
