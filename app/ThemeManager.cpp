#include "ThemeManager.h"
#include <QApplication>
#include <QFile>
#include <QDir>

ThemeManager::ThemeManager(QObject* parent) : QObject(parent) {}

QString ThemeManager::readStyleSheet(const QString& fileName) const
{
    QFile f(QStringLiteral(":/styles/") + fileName);
    if (!f.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        const QString disk = QDir(QApplication::applicationDirPath()).filePath(QStringLiteral("../styles/") + fileName);
        f.setFileName(disk);
        if (!f.open(QIODevice::ReadOnly | QIODevice::Text))
            return {};
    }
    return QString::fromUtf8(f.readAll());
}

void ThemeManager::loadTheme(const QString& themeName)
{
    Q_UNUSED(themeName);
}

void ThemeManager::applyGlobalStyle(QApplication* app)
{
    QString style = readStyleSheet(QStringLiteral("main.qss"));
    style += readStyleSheet(QStringLiteral("sidebar.qss"));
    style += readStyleSheet(QStringLiteral("cards.qss"));
    style += readStyleSheet(QStringLiteral("keyboard.qss"));
    style += readStyleSheet(QStringLiteral("dock.qss"));
    style += readStyleSheet(QStringLiteral("rgb.qss"));
    style += readStyleSheet(QStringLiteral("titlebar.qss"));
    app->setStyleSheet(style);
}
