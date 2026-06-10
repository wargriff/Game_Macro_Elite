#pragma once

#include "../models/MacroModel.h"
#include <QAbstractNativeEventFilter>
#include <QObject>
#include <QHash>
#include <QTimer>

class MacroEngine : public QObject
{
    Q_OBJECT
public:
    static MacroEngine& instance();

    void start();
    void stop();
    bool isRunning() const { return m_running; }

    void onMouseSideButton(int buttonIndex);
    void simulateKeyLabel(const QString& label);

signals:
    void masterToggled(bool enabled);
    void macroTriggered(const QString& keyLabel);

private slots:
    void onTick();
    void onMasterChanged(bool enabled);

private:
    explicit MacroEngine(QObject* parent = nullptr);
    bool shouldRunMacro(const MacroEntry& entry) const;
    quint16 virtualKeyForLabel(const QString& label) const;

    QTimer m_timer;
    QHash<int, qint64> m_lastFireMs;
    QAbstractNativeEventFilter* m_nativeFilter = nullptr;
    bool m_running = false;
};
