#include "MacroEngine.h"
#include "MacroService.h"
#include "../core/AppState.h"
#include "../core/EventBus.h"
#include "../core/Logger.h"
#include "../models/MacroModel.h"

#include <QAbstractNativeEventFilter>
#include <QCoreApplication>
#include <QDateTime>

#ifdef Q_OS_WIN
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>
#endif

namespace
{
#ifdef Q_OS_WIN
class MacroNativeFilter : public QAbstractNativeEventFilter
{
public:
    bool nativeEventFilter(const QByteArray& eventType, void* message, qintptr*) override
    {
        if (eventType != "windows_generic_MSG" && eventType != "windows_dispatcher_MSG")
            return false;

        const MSG* msg = static_cast<MSG*>(message);
        if (msg->message != WM_XBUTTONDOWN)
            return false;

        const WORD xbtn = GET_XBUTTON_WPARAM(msg->wParam);
        if (xbtn == XBUTTON1)
            MacroEngine::instance().onMouseSideButton(1);
        else if (xbtn == XBUTTON2)
            MacroEngine::instance().onMouseSideButton(2);
        return false;
    }
};
#endif
}

MacroEngine& MacroEngine::instance()
{
    static MacroEngine engine;
    return engine;
}

MacroEngine::MacroEngine(QObject* parent) : QObject(parent)
{
    m_timer.setInterval(8);
    connect(&m_timer, &QTimer::timeout, this, &MacroEngine::onTick);
    connect(&EventBus::instance(), &EventBus::macroMasterChanged, this, &MacroEngine::onMasterChanged);
}

void MacroEngine::start()
{
    if (m_running)
        return;

#ifdef Q_OS_WIN
    if (!m_nativeFilter)
    {
        m_nativeFilter = new MacroNativeFilter();
        QCoreApplication::instance()->installNativeEventFilter(m_nativeFilter);
    }
#endif

    m_timer.start();
    m_running = true;
    Logger::info(QStringLiteral("MacroEngine actif — L1 = XButton1 (bouton lateral souris)"));
}

void MacroEngine::stop()
{
    m_timer.stop();
    m_running = false;
}

void MacroEngine::onMasterChanged(bool enabled)
{
    Logger::info(enabled ? QStringLiteral("Macros L1 : ON")
                         : QStringLiteral("Macros L1 : OFF"));
}

void MacroEngine::onMouseSideButton(int buttonIndex)
{
    const QString sideLabel = buttonIndex == 1 ? QStringLiteral("L1") : QStringLiteral("L2");
    auto& macros = MacroService::instance().activeMacros();

    for (const MacroEntry& entry : macros)
    {
        if (entry.device != QStringLiteral("mouse"))
            continue;
        if (entry.keyLabel.compare(sideLabel, Qt::CaseInsensitive) != 0)
            continue;
        if (!entry.active)
            return;

        if (entry.toggle)
        {
            auto& st = AppStateStore::instance().state();
            st.macroMasterEnabled = !st.macroMasterEnabled;
            emit EventBus::instance().macroMasterChanged(st.macroMasterEnabled);
            emit masterToggled(st.macroMasterEnabled);
            Logger::info(QStringLiteral("L1 bascule macros : %1")
                             .arg(st.macroMasterEnabled ? QStringLiteral("ON") : QStringLiteral("OFF")));
            return;
        }

        simulateKeyLabel(entry.keyLabel);
        emit macroTriggered(entry.keyLabel);
        return;
    }
}

quint16 MacroEngine::virtualKeyForLabel(const QString& label) const
{
    const QString k = label.trimmed();
    if (k.size() == 1)
    {
        const QChar c = k.at(0).toUpper();
        if (c.isDigit())
            return static_cast<quint16>(c.unicode());
        if (c.isLetter())
            return static_cast<quint16>(c.unicode());
    }

    static const QHash<QString, quint16> map = {
        { QStringLiteral("Space"), VK_SPACE },
        { QStringLiteral("Enter"), VK_RETURN },
        { QStringLiteral("Tab"), VK_TAB },
        { QStringLiteral("Esc"), VK_ESCAPE },
        { QStringLiteral("Shift"), VK_SHIFT },
        { QStringLiteral("Ctrl"), VK_CONTROL },
        { QStringLiteral("Alt"), VK_MENU },
        { QStringLiteral("F"), 'F' },
        { QStringLiteral("Q"), 'Q' },
        { QStringLiteral("W"), 'W' },
        { QStringLiteral("R"), 'R' },
    };

    return map.value(k, 0);
}

void MacroEngine::simulateKeyLabel(const QString& label)
{
#ifdef Q_OS_WIN
    const quint16 vk = virtualKeyForLabel(label);
    if (!vk)
        return;

    INPUT down {};
    down.type = INPUT_KEYBOARD;
    down.ki.wVk = vk;

    INPUT up {};
    up.type = INPUT_KEYBOARD;
    up.ki.wVk = vk;
    up.ki.dwFlags = KEYEVENTF_KEYUP;

    INPUT seq[2] = { down, up };
    SendInput(2, seq, sizeof(INPUT));
#else
    Q_UNUSED(label);
#endif
}

bool MacroEngine::shouldRunMacro(const MacroEntry& entry) const
{
    if (!entry.active || entry.toggle)
        return false;
    if (entry.gatedByMaster)
        return AppStateStore::instance().state().macroMasterEnabled;
    return false;
}

void MacroEngine::onTick()
{
    if (!AppStateStore::instance().state().engineActive)
        return;

    const qint64 now = QDateTime::currentMSecsSinceEpoch();
    const auto& macros = MacroService::instance().activeMacros();

    for (const MacroEntry& entry : macros)
    {
        if (!shouldRunMacro(entry))
            continue;

        const int interval = qMax(1, entry.delayMs);
        const qint64 last = m_lastFireMs.value(entry.id, 0);
        if (now - last < interval)
            continue;

        simulateKeyLabel(entry.keyLabel);
        m_lastFireMs[entry.id] = now;
    }
}
