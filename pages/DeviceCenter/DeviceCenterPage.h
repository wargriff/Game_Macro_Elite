#pragma once

#include <QWidget>

class QTabWidget;
class QComboBox;
class QLabel;
class QDoubleSpinBox;
class QSpinBox;
class QCheckBox;

class DeviceCenterPage : public QWidget
{
    Q_OBJECT
public:
    explicit DeviceCenterPage(QWidget* parent = nullptr);
    void focusDevice(const QString& deviceId);

private slots:
    void refreshProfile();
    void reloadMacroList(int selectIndex);
    void syncPanelFromMacro(int index);
    void onCpsChanged(double cps);
    void onDelayChanged(int ms);

private:
    void updatePanelHeader();

    QTabWidget* m_tabs = nullptr;
    QLabel* m_panelHeader = nullptr;
    QLabel* m_targetLabel = nullptr;
    QComboBox* m_macroCombo = nullptr;
    QDoubleSpinBox* m_cpsSpin = nullptr;
    QSpinBox* m_delaySpin = nullptr;
    QCheckBox* m_activeToggle = nullptr;
    QLabel* m_toggleHint = nullptr;
    bool m_mouseMode = false;
    QString m_mouseButton = QStringLiteral("Gauche");
    QString m_keyLabel = QStringLiteral("W");
};
