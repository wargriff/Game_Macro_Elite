#pragma once

#include <QObject>
#include <QString>

class ThemeManager : public QObject
{
    Q_OBJECT
public:
    explicit ThemeManager(QObject* parent = nullptr);

    void loadTheme(const QString& themeName = QStringLiteral("red"));
    void applyGlobalStyle(class QApplication* app);

private:
    QString readStyleSheet(const QString& fileName) const;
};
