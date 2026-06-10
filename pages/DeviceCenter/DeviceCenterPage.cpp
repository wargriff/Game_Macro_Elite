#include "DeviceCenterPage.h"

#include "../../widgets/keyboard/KeyboardWidget.h"
#include "../../widgets/mouse/MouseWidget.h"
#include "../../widgets/rgb/RGBPanelWidget.h"
#include "../../widgets/rgb/RGBPreviewWidget.h"
#include "../../widgets/stats/StatsPanelWidget.h"
#include "../../services/MacroService.h"
#include "../../services/RGBService.h"
#include "../../core/AppState.h"
#include "../../core/EventBus.h"
#include "../../core/Enums.h"

#include <QCheckBox>
#include <QComboBox>
#include <QDoubleSpinBox>
#include <QFormLayout>
#include <QFrame>
#include <QHBoxLayout>
#include <QLabel>
#include <QPushButton>
#include <QSpinBox>
#include <QStackedWidget>
#include <QTabWidget>
#include <QVBoxLayout>

DeviceCenterPage::DeviceCenterPage(QWidget* parent) : QWidget(parent)
{
    setObjectName(QStringLiteral("deviceCenterPage"));

    auto* root = new QVBoxLayout(this);
    root->setContentsMargins(24, 16, 24, 16);
    root->setSpacing(14);

    auto* pageTitle = new QLabel(QStringLiteral("Device Center"), this);
    pageTitle->setObjectName(QStringLiteral("pageTitle"));
    root->addWidget(pageTitle);

    auto* deviceStack = new QStackedWidget(this);

    auto* mousePage = new QWidget(this);
    auto* mouseLayout = new QVBoxLayout(mousePage);
    mouseLayout->setContentsMargins(0, 0, 0, 0);
    auto* mouseWidget = new MouseWidget(mousePage);
    mouseLayout->addWidget(mouseWidget, 1);

    auto* kbPage = new QWidget(this);
    auto* kbLayout = new QVBoxLayout(kbPage);
    kbLayout->setContentsMargins(0, 0, 0, 0);
    auto* keyboard = new KeyboardWidget(kbPage);
    kbLayout->addWidget(keyboard, 1);

    deviceStack->addWidget(mousePage);
    deviceStack->addWidget(kbPage);

    auto* header = new QHBoxLayout();
    m_tabs = new QTabWidget(this);
    m_tabs->setObjectName(QStringLiteral("deviceTabs"));
    m_tabs->addTab(new QWidget(), QStringLiteral("Souris"));
    m_tabs->addTab(new QWidget(), QStringLiteral("Clavier"));
    m_tabs->setCurrentIndex(0);
    connect(m_tabs, &QTabWidget::currentChanged, deviceStack, &QStackedWidget::setCurrentIndex);
    header->addWidget(m_tabs, 1);

    auto* deviceCombo = new QComboBox(this);
    deviceCombo->setMinimumWidth(220);
    deviceCombo->addItem(QStringLiteral("60% Gaming Keyboard"));
    deviceCombo->addItem(QStringLiteral("TKL Gaming Keyboard"));
    deviceCombo->addItem(QStringLiteral("Elite M40"));
    header->addWidget(deviceCombo);
    root->addLayout(header);

    auto* body = new QHBoxLayout();
    body->setSpacing(20);

    auto* left = new QVBoxLayout();
    left->addWidget(deviceStack, 1);

    auto* legend = new QHBoxLayout();
    legend->setSpacing(20);
    auto addLeg = [&](const QString& html) {
        auto* lb = new QLabel(html, this);
        lb->setTextFormat(Qt::RichText);
        lb->setStyleSheet(QStringLiteral("color: #b0b0bc; font-size: 13px;"));
        legend->addWidget(lb);
    };
    addLeg(QStringLiteral("<span style='color:#3498db;font-size:14px'>●</span> Contour bleu"));
    addLeg(QStringLiteral("<span style='color:#e02626;font-size:14px'>●</span> Macro"));
    addLeg(QStringLiteral("<span style='color:#ff8c2a;font-size:14px'>●</span> L1 / L2 gauche"));
    legend->addStretch();
    left->addLayout(legend);
    body->addLayout(left, 3);

    auto* right = new QFrame(this);
    right->setObjectName(QStringLiteral("keyConfigPanel"));
    right->setMinimumWidth(300);
    auto* panelLayout = new QVBoxLayout(right);
    panelLayout->setSpacing(12);

    m_panelHeader = new QLabel(QStringLiteral("TOUCHE W"), this);
    m_panelHeader->setObjectName(QStringLiteral("panelHeader"));
    panelLayout->addWidget(m_panelHeader);

    auto* form = new QFormLayout();
    form->setSpacing(10);
    form->setLabelAlignment(Qt::AlignLeft);

    m_targetLabel = new QLabel(QStringLiteral("Touche W"), this);
    form->addRow(QStringLiteral("Cible"), m_targetLabel);

    m_macroCombo = new QComboBox(this);
    form->addRow(QStringLiteral("Macro assignee"), m_macroCombo);

    m_cpsSpin = new QDoubleSpinBox(this);
    m_cpsSpin->setRange(0.0, 50.0);
    m_cpsSpin->setSingleStep(0.5);
    m_cpsSpin->setDecimals(1);
    m_cpsSpin->setSuffix(QStringLiteral(" CPS"));
    form->addRow(QStringLiteral("Vitesse CPS"), m_cpsSpin);

    m_delaySpin = new QSpinBox(this);
    m_delaySpin->setRange(0, 2000);
    m_delaySpin->setSuffix(QStringLiteral(" ms"));
    form->addRow(QStringLiteral("Delai"), m_delaySpin);

    m_toggleHint = new QLabel(QStringLiteral("Bouton lateral L1 (XButton1) : active/desactive les autoclicks 1-2-3-4"), this);
    m_toggleHint->setObjectName(QStringLiteral("toggleHint"));
    m_toggleHint->hide();
    form->addRow(QString(), m_toggleHint);

    auto* activeRow = new QHBoxLayout();
    auto* activeLabel = new QLabel(QStringLiteral("Actif"), this);
    m_activeToggle = new QCheckBox(this);
    m_activeToggle->setChecked(true);
    m_activeToggle->setStyleSheet(QStringLiteral(
        "QCheckBox::indicator { width: 40px; height: 22px; border-radius: 11px; background: #e02626; }"
        "QCheckBox::indicator:unchecked { background: #3a3a48; }"));
    activeRow->addWidget(activeLabel);
    activeRow->addStretch();
    activeRow->addWidget(m_activeToggle);
    form->addRow(activeRow);

    panelLayout->addLayout(form);
    panelLayout->addStretch();

    auto* btns = new QHBoxLayout();
    auto* save = new QPushButton(QStringLiteral("Enregistrer"), this);
    save->setObjectName(QStringLiteral("primaryButton"));
    auto* test = new QPushButton(QStringLiteral("Tester"), this);
    test->setObjectName(QStringLiteral("secondaryButton"));
    btns->addWidget(test);
    btns->addWidget(save);
    panelLayout->addLayout(btns);

    body->addWidget(right, 1);
    root->addLayout(body, 1);

    auto* bottom = new QHBoxLayout();
    bottom->setSpacing(16);
    static RGBService rgb;
    bottom->addWidget(new RGBPanelWidget(&rgb, this), 2);
    bottom->addWidget(new RGBPreviewWidget(this));
    bottom->addWidget(new StatsPanelWidget(this), 1);
    root->addLayout(bottom);

    connect(m_macroCombo, QOverload<int>::of(&QComboBox::currentIndexChanged), this, &DeviceCenterPage::syncPanelFromMacro);
    connect(m_cpsSpin, QOverload<double>::of(&QDoubleSpinBox::valueChanged), this, &DeviceCenterPage::onCpsChanged);
    connect(m_delaySpin, QOverload<int>::of(&QSpinBox::valueChanged), this, &DeviceCenterPage::onDelayChanged);
    connect(m_activeToggle, &QCheckBox::toggled, this, [this](bool on) {
        auto& macros = MacroService::instance().activeMacros();
        const int idx = m_macroCombo->currentIndex();
        if (idx < 0 || idx >= macros.size()) return;
        macros[idx].active = on;
        if (macros[idx].toggle && macros[idx].device == QStringLiteral("mouse") &&
            macros[idx].keyLabel == QStringLiteral("L1"))
        {
            AppStateStore::instance().state().macroMasterEnabled = on;
            emit EventBus::instance().macroMasterChanged(on);
        }
    });
    connect(test, &QPushButton::clicked, this, [this]() {
        auto& macros = MacroService::instance().activeMacros();
        const int idx = m_macroCombo->currentIndex();
        if (idx < 0 || idx >= macros.size()) return;
        if (macros[idx].toggle && macros[idx].keyLabel == QStringLiteral("L1"))
        {
            const bool next = !AppStateStore::instance().state().macroMasterEnabled;
            AppStateStore::instance().state().macroMasterEnabled = next;
            m_activeToggle->setChecked(next);
            macros[idx].active = next;
            emit EventBus::instance().macroMasterChanged(next);
        }
    });
    connect(save, &QPushButton::clicked, this, [this]() {
        auto& macros = MacroService::instance().activeMacros();
        const int idx = m_macroCombo->currentIndex();
        if (idx < 0 || idx >= macros.size()) return;
        auto& m = macros[idx];
        m.cps = m_cpsSpin->value();
        m.delayMs = m_delaySpin->value();
        m.active = m_activeToggle->isChecked();
        if (m_mouseMode)
        {
            m.device = QStringLiteral("mouse");
            m.keyLabel = m_mouseButton;
        }
        else
        {
            m.device = QStringLiteral("keyboard");
            m.keyLabel = m_keyLabel;
        }
    });

    connect(keyboard, &KeyboardWidget::keySelected, this, [this, deviceCombo](const QString& key) {
        m_mouseMode = false;
        m_keyLabel = key;
        deviceCombo->setCurrentIndex(0);
        updatePanelHeader();
        const auto& macros = MacroService::instance().activeMacros();
        for (int i = 0; i < macros.size(); ++i)
        {
            if (macros[i].device == QStringLiteral("keyboard") &&
                macros[i].keyLabel.compare(key, Qt::CaseInsensitive) == 0)
            {
                reloadMacroList(i);
                return;
            }
        }
    });

    connect(mouseWidget, &MouseWidget::buttonSelected, this, [this, deviceCombo](const QString& btn) {
        m_mouseMode = true;
        m_mouseButton = btn;
        deviceCombo->setCurrentText(QStringLiteral("Elite M40"));
        updatePanelHeader();
        const auto& macros = MacroService::instance().activeMacros();
        for (int i = 0; i < macros.size(); ++i)
        {
            if (macros[i].device == QStringLiteral("mouse") &&
                macros[i].keyLabel.compare(btn, Qt::CaseInsensitive) == 0)
            {
                reloadMacroList(i);
                return;
            }
        }
    });

    connect(m_tabs, &QTabWidget::currentChanged, this, [this, deviceCombo](int idx) {
        m_mouseMode = (idx == 0);
        if (idx == 0)
            deviceCombo->setCurrentText(QStringLiteral("Elite M40"));
        else
            deviceCombo->setCurrentIndex(0);
        updatePanelHeader();
    });

    connect(&EventBus::instance(), &EventBus::profileChanged, this, &DeviceCenterPage::refreshProfile);
    connect(&EventBus::instance(), &EventBus::macroMasterChanged, this, [this](bool on) {
        if (m_activeToggle && m_toggleHint && m_toggleHint->isVisible())
            m_activeToggle->setChecked(on);
    });

    mouseWidget->selectButtonByLabel(QStringLiteral("L1"));
    m_mouseMode = true;
    m_mouseButton = QStringLiteral("L1");
    deviceCombo->setCurrentText(QStringLiteral("Elite M40"));
    updatePanelHeader();

    reloadMacroList(0);
    const auto& macros = MacroService::instance().activeMacros();
    for (int i = 0; i < macros.size(); ++i)
    {
        if (macros[i].device == QStringLiteral("mouse") &&
            macros[i].keyLabel == QStringLiteral("L1"))
        {
            reloadMacroList(i);
            break;
        }
    }
}

void DeviceCenterPage::focusDevice(const QString& deviceId)
{
    if (!m_tabs) return;
    if (deviceId == QStringLiteral("ms"))
    {
        m_tabs->setCurrentIndex(0);
        m_mouseMode = true;
    }
    else if (deviceId == QStringLiteral("kb"))
    {
        m_tabs->setCurrentIndex(1);
        m_mouseMode = false;
    }
    updatePanelHeader();
}

void DeviceCenterPage::refreshProfile()
{
    reloadMacroList(0);
    updatePanelHeader();
}

void DeviceCenterPage::reloadMacroList(int selectIndex)
{
    if (!m_macroCombo) return;

    m_macroCombo->blockSignals(true);
    m_macroCombo->clear();

    const auto& macros = MacroService::instance().activeMacros();
    for (const auto& m : macros)
        m_macroCombo->addItem(m.name);

    const int idx = selectIndex >= 0 ? qBound(0, selectIndex, macros.size() - 1) : 0;
    m_macroCombo->setCurrentIndex(macros.isEmpty() ? -1 : idx);
    m_macroCombo->blockSignals(false);

    if (!macros.isEmpty())
        syncPanelFromMacro(idx);
}

void DeviceCenterPage::syncPanelFromMacro(int index)
{
    const auto& macros = MacroService::instance().activeMacros();
    if (index < 0 || index >= macros.size()) return;

    const MacroEntry& m = macros.at(index);
    MacroService::instance().model().setSelectedIndex(index);

    m_cpsSpin->blockSignals(true);
    m_delaySpin->blockSignals(true);
    m_cpsSpin->setValue(m.cps);
    m_delaySpin->setValue(m.delayMs);
    m_cpsSpin->setEnabled(!m.toggle);
    m_cpsSpin->blockSignals(false);
    m_delaySpin->blockSignals(false);

    m_activeToggle->setChecked(m.toggle ? AppStateStore::instance().state().macroMasterEnabled : m.active);
    m_toggleHint->setVisible(m.toggle);
    if (m.toggle && m.keyLabel == QStringLiteral("L1"))
        m_toggleHint->setText(QStringLiteral("Bouton lateral L1 (XButton1) : active/desactive les autoclicks 1-2-3-4"));

    if (m.device == QStringLiteral("mouse"))
    {
        m_mouseMode = true;
        m_mouseButton = m.keyLabel;
    }
    else
    {
        m_mouseMode = false;
        m_keyLabel = m.keyLabel;
    }
    updatePanelHeader();
}

void DeviceCenterPage::onCpsChanged(double cps)
{
    auto& macros = MacroService::instance().activeMacros();
    const int idx = m_macroCombo->currentIndex();
    if (idx < 0 || idx >= macros.size() || macros[idx].toggle) return;
    macros[idx].cps = cps;
    if (cps > 0.0)
    {
        const int ms = qMax(1, int(1000.0 / cps));
        m_delaySpin->blockSignals(true);
        m_delaySpin->setValue(ms);
        macros[idx].delayMs = ms;
        m_delaySpin->blockSignals(false);
    }
}

void DeviceCenterPage::onDelayChanged(int ms)
{
    auto& macros = MacroService::instance().activeMacros();
    const int idx = m_macroCombo->currentIndex();
    if (idx < 0 || idx >= macros.size() || macros[idx].toggle) return;
    macros[idx].delayMs = ms;
    if (ms > 0)
    {
        const double cps = 1000.0 / ms;
        m_cpsSpin->blockSignals(true);
        m_cpsSpin->setValue(cps);
        macros[idx].cps = cps;
        m_cpsSpin->blockSignals(false);
    }
}

void DeviceCenterPage::updatePanelHeader()
{
    if (!m_panelHeader || !m_targetLabel) return;

    if (m_mouseMode)
    {
        m_panelHeader->setText(QStringLiteral("BOUTON SOURIS"));
        m_targetLabel->setText(QStringLiteral("Elite M40 — %1").arg(m_mouseButton));
    }
    else
    {
        m_panelHeader->setText(QStringLiteral("TOUCHE %1").arg(m_keyLabel.toUpper()));
        m_targetLabel->setText(QStringLiteral("Touche %1").arg(m_keyLabel.toUpper()));
    }
}
