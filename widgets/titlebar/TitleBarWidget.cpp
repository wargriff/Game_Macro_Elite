#include "TitleBarWidget.h"
#include "../../core/Constants.h"
#include "../../core/Enums.h"
#include "../../core/AppState.h"
#include "../../core/EventBus.h"
#include "../../services/ProfileService.h"
#include <QFrame>
#include <QHBoxLayout>
#include <QLabel>
#include <QMenu>
#include <QProgressBar>
#include <QPushButton>
#include <QStyle>

TitleBarWidget::TitleBarWidget(QWidget* parent) : QWidget(parent)
{
    setObjectName(QStringLiteral("titleBar"));
    setFixedHeight(Gx::Layout::TitleBarHeight);
    buildUi();

    connect(&EventBus::instance(), &EventBus::profileChanged, this, [this](int) { refresh(); });
    connect(&EventBus::instance(), &EventBus::sectionChanged, this, [this](NavSection) { refresh(); });
    connect(&EventBus::instance(), &EventBus::macroMasterChanged, this, [this](bool) { refresh(); });
}

void TitleBarWidget::buildUi()
{
    auto* layout = new QHBoxLayout(this);
    layout->setContentsMargins(16, 6, 8, 6);
    layout->setSpacing(12);

    m_sectionLabel = new QLabel(this);
    m_sectionLabel->setObjectName(QStringLiteral("titleBarSection"));
    layout->addWidget(m_sectionLabel);
    layout->addStretch();

    auto* enginePanel = new QFrame(this);
    enginePanel->setObjectName(QStringLiteral("titleBarEngine"));
    auto* engineLayout = new QHBoxLayout(enginePanel);
    engineLayout->setContentsMargins(12, 4, 12, 4);
    engineLayout->setSpacing(10);

    auto* engineTitle = new QLabel(QStringLiteral("MOTEUR"), enginePanel);
    engineTitle->setObjectName(QStringLiteral("titleBarEngineLabel"));
    engineLayout->addWidget(engineTitle);

    m_engineBadge = new QLabel(QStringLiteral("Actif"), enginePanel);
    m_engineBadge->setObjectName(QStringLiteral("titleBarEngineBadge"));
    engineLayout->addWidget(m_engineBadge);

    auto* cpuCol = new QVBoxLayout();
    cpuCol->setSpacing(2);
    auto* cpuRow = new QHBoxLayout();
    auto* cpuLb = new QLabel(QStringLiteral("CPU"), enginePanel);
    cpuLb->setObjectName(QStringLiteral("titleBarMeterLabel"));
    m_cpuBar = new QProgressBar(enginePanel);
    m_cpuBar->setObjectName(QStringLiteral("titleBarMeterBar"));
    m_cpuBar->setProperty("accent", "cpu");
    m_cpuBar->setRange(0, 100);
    m_cpuBar->setFixedSize(72, 5);
    m_cpuBar->setTextVisible(false);
    cpuRow->addWidget(cpuLb);
    cpuRow->addWidget(m_cpuBar);
    cpuCol->addLayout(cpuRow);

    auto* ramRow = new QHBoxLayout();
    auto* ramLb = new QLabel(QStringLiteral("RAM"), enginePanel);
    ramLb->setObjectName(QStringLiteral("titleBarMeterLabel"));
    m_ramBar = new QProgressBar(enginePanel);
    m_ramBar->setObjectName(QStringLiteral("titleBarMeterBar"));
    m_ramBar->setProperty("accent", "ram");
    m_ramBar->setRange(0, 100);
    m_ramBar->setFixedSize(72, 5);
    m_ramBar->setTextVisible(false);
    ramRow->addWidget(ramLb);
    ramRow->addWidget(m_ramBar);
    cpuCol->addLayout(ramRow);
    engineLayout->addLayout(cpuCol);

    auto* ver = new QLabel(Gx::App::Version, enginePanel);
    ver->setObjectName(QStringLiteral("titleBarVersion"));
    engineLayout->addWidget(ver);

    layout->addWidget(enginePanel);

    m_profileLabel = new QLabel(this);
    m_profileLabel->setObjectName(QStringLiteral("titleBarProfile"));
    layout->addWidget(m_profileLabel);

    auto* changeBtn = new QPushButton(QStringLiteral("Changer"), this);
    changeBtn->setObjectName(QStringLiteral("titleBarChangeBtn"));
    connect(changeBtn, &QPushButton::clicked, this, &TitleBarWidget::showProfileMenu);
    layout->addWidget(changeBtn);

    refresh();
}

void TitleBarWidget::showProfileMenu()
{
    QMenu menu(this);
    const auto& profiles = ProfileService::instance().model().profiles();
    const int active = ProfileService::instance().activeIndex();
    for (int i = 0; i < profiles.size(); ++i)
    {
        QAction* action = menu.addAction(profiles.at(i).name);
        action->setCheckable(true);
        action->setChecked(i == active);
        connect(action, &QAction::triggered, this, [i]() {
            ProfileService::instance().applyProfile(i);
        });
    }
    menu.exec(mapToGlobal(m_profileLabel->geometry().bottomLeft()));
}

void TitleBarWidget::refresh()
{
    const auto& st = AppStateStore::instance().state();
    if (m_sectionLabel)
        m_sectionLabel->setText(navSectionLabel(st.currentSection));
    if (m_profileLabel)
        m_profileLabel->setText(QStringLiteral("%1 — Profil actif").arg(st.activeProfileName));
    if (m_engineBadge)
    {
        const bool on = st.engineActive && st.macroMasterEnabled;
        m_engineBadge->setText(on ? QStringLiteral("Macros ON") : QStringLiteral("Actif"));
        m_engineBadge->setProperty("running", on);
        m_engineBadge->style()->unpolish(m_engineBadge);
        m_engineBadge->style()->polish(m_engineBadge);
    }
    if (m_cpuBar)
        m_cpuBar->setValue(int(st.cpuUsage * 100));
    if (m_ramBar)
        m_ramBar->setValue(int(st.ramUsage * 100));
}
