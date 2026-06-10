#pragma once

#include <QObject>
#include <QSettings>

class SettingsManager : public QObject
{
    Q_OBJECT
public:
    explicit SettingsManager(QObject* parent = nullptr);

    float rgbSpeed() const;
    float rgbBrightness() const;
    void setRgbSpeed(float v);
    void setRgbBrightness(float v);

private:
    QSettings m_settings;
};
