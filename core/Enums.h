#pragma once

#include <QMap>
#include <QString>

enum class NavSection
{
    MissionControl,
    DeviceCenter,
    MacroStudio,
    MacroLibrary,
    ProfileManager,
    ActivityMonitor,
    AnalyticsCenter,
    MobileCommand,
    LightingEngine,
    SettingsHub
};

enum class DeviceTab
{
    Mouse,
    Keyboard
};

enum class KeyAssignment
{
    Normal,
    Macro,
    Function,
    Disabled
};

enum class RgbEffect
{
    Rainbow,
    Wave,
    Breathing,
    Ripple,
    Reactive,
    Static
};

inline QString navSectionLabel(NavSection s)
{
    switch (s)
    {
    case NavSection::MissionControl:  return QStringLiteral("Mission Control");
    case NavSection::SettingsHub:     return QStringLiteral("Mission Control");
    case NavSection::DeviceCenter:    return QStringLiteral("Device Center");
    case NavSection::MacroStudio:     return QStringLiteral("Macro Studio");
    case NavSection::MacroLibrary:    return QStringLiteral("Macro Library");
    case NavSection::ProfileManager:  return QStringLiteral("Profile Manager");
    case NavSection::ActivityMonitor: return QStringLiteral("Activity Monitor");
    case NavSection::AnalyticsCenter: return QStringLiteral("Analytics Center");
    case NavSection::MobileCommand:   return QStringLiteral("Mobile Command");
    case NavSection::LightingEngine:  return QStringLiteral("Lighting Engine");
    }
    return {};
}

inline QString navSectionIconAsset(NavSection s)
{
    switch (s)
    {
    case NavSection::MissionControl:
    case NavSection::SettingsHub:     return QStringLiteral("icons/mission-control.svg");
    case NavSection::DeviceCenter:    return QStringLiteral("icons/device-center.svg");
    case NavSection::MacroStudio:     return QStringLiteral("icons/macro-studio.svg");
    case NavSection::MacroLibrary:    return QStringLiteral("icons/macro-library.svg");
    case NavSection::ProfileManager:  return QStringLiteral("icons/profile-manager.svg");
    case NavSection::ActivityMonitor: return QStringLiteral("icons/activity-monitor.svg");
    case NavSection::AnalyticsCenter: return QStringLiteral("icons/analytics-center.svg");
    case NavSection::MobileCommand:   return QStringLiteral("icons/mobile-command.svg");
    case NavSection::LightingEngine:  return QStringLiteral("icons/lighting-engine.svg");
    }
    return QStringLiteral("icons/settings-hub.svg");
}

inline QString deviceIconAsset(const QString& deviceId)
{
    static const QMap<QString, QString> map = {
        { QStringLiteral("mb"),  QStringLiteral("devices/dock-motherboard.svg") },
        { QStringLiteral("gpu"), QStringLiteral("devices/dock-gpu.svg") },
        { QStringLiteral("kb"),  QStringLiteral("devices/dock-keyboard.svg") },
        { QStringLiteral("ms"),  QStringLiteral("devices/dock-mouse-elite-m40.svg") },
        { QStringLiteral("hs"),  QStringLiteral("devices/dock-headset.svg") },
        { QStringLiteral("aio"), QStringLiteral("devices/dock-aio.svg") },
        { QStringLiteral("ssd"), QStringLiteral("devices/dock-ssd.svg") },
        { QStringLiteral("usb"), QStringLiteral("devices/dock-usb.svg") }
    };
    return map.value(deviceId, QStringLiteral("devices/cpu.svg"));
}
