#include "SettingsManager.h"

SettingsManager::SettingsManager(QObject* parent)
    : QObject(parent)
    , m_settings(QStringLiteral("GameX"), QStringLiteral("GAMEX_MACRO"))
{
}

float SettingsManager::rgbSpeed() const { return m_settings.value(QStringLiteral("rgb/speed"), 0.65).toFloat(); }
float SettingsManager::rgbBrightness() const { return m_settings.value(QStringLiteral("rgb/brightness"), 0.80).toFloat(); }
void SettingsManager::setRgbSpeed(float v) { m_settings.setValue(QStringLiteral("rgb/speed"), v); }
void SettingsManager::setRgbBrightness(float v) { m_settings.setValue(QStringLiteral("rgb/brightness"), v); }
