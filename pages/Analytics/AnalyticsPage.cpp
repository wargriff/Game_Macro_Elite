#include "AnalyticsPage.h"

#include "../../core/AppState.h"
#include "../../widgets/cards/StatsCard.h"
#include "../../widgets/charts/CpuChartWidget.h"
#include "../../widgets/charts/RamChartWidget.h"
#include "../../widgets/stats/CounterWidget.h"

#include <QFrame>
#include <QGridLayout>
#include <QHBoxLayout>
#include <QLabel>
#include <QVBoxLayout>

namespace
{
QFrame* makeActivityRow(const QString& time, const QString& event, const QString& detail, QWidget* parent)
{
    auto* row = new QFrame(parent);
    row->setObjectName(QStringLiteral("activityRow"));
    auto* layout = new QHBoxLayout(row);
    layout->setContentsMargins(12, 8, 12, 8);
    layout->setSpacing(12);

    auto* timeLb = new QLabel(time, row);
    timeLb->setObjectName(QStringLiteral("activityTime"));
    timeLb->setFixedWidth(52);
    layout->addWidget(timeLb);

    auto* eventLb = new QLabel(event, row);
    eventLb->setObjectName(QStringLiteral("activityEvent"));
    eventLb->setMinimumWidth(140);
    layout->addWidget(eventLb);

    auto* detailLb = new QLabel(detail, row);
    detailLb->setObjectName(QStringLiteral("activityDetail"));
    detailLb->setWordWrap(true);
    layout->addWidget(detailLb, 1);

    return row;
}
}

AnalyticsPage::AnalyticsPage(QWidget* parent) : QWidget(parent)
{
    setObjectName(QStringLiteral("analyticsPage"));

    auto* root = new QVBoxLayout(this);
    root->setContentsMargins(24, 16, 24, 16);
    root->setSpacing(16);

    auto* title = new QLabel(QStringLiteral("Analytics Center"), this);
    title->setObjectName(QStringLiteral("pageTitle"));
    root->addWidget(title);

    auto* subtitle = new QLabel(
        QStringLiteral("Statistiques de session, performance systeme et utilisation des macros."),
        this);
    subtitle->setObjectName(QStringLiteral("pageSubtitle"));
    root->addWidget(subtitle);

    const auto& st = AppStateStore::instance().state();

    auto* counters = new QHBoxLayout();
    counters->setSpacing(14);
    counters->addWidget(new CounterWidget(QStringLiteral("2h 14m"), QStringLiteral("Session"), QStringLiteral("macro"), this));
    counters->addWidget(new CounterWidget(QStringLiteral("1 842"), QStringLiteral("Clics macro"), QStringLiteral("function"), this));
    counters->addWidget(new CounterWidget(QString::number(st.macroCount), QStringLiteral("Macros actives"), QStringLiteral("macro"), this));
    counters->addWidget(new CounterWidget(QStringLiteral("96%"), QStringLiteral("Precision"), QStringLiteral("disabled"), this));
    root->addLayout(counters);

    auto* grid = new QGridLayout();
    grid->setSpacing(16);

    grid->addWidget(new StatsCard(
        QString::number(int(st.cpuUsage * 100)) + QStringLiteral("%"),
        QStringLiteral("CPU moyen"), QStringLiteral("macro"), this), 0, 0);
    grid->addWidget(new StatsCard(
        QString::number(int(st.ramUsage * 100)) + QStringLiteral("%"),
        QStringLiteral("RAM moyenne"), QStringLiteral("function"), this), 0, 1);
    grid->addWidget(new StatsCard(QStringLiteral("847"), QStringLiteral("Macros / h"), QStringLiteral("macro"), this), 0, 2);
    grid->addWidget(new StatsCard(QStringLiteral("3"), QStringLiteral("Changements profil"), QStringLiteral("function"), this), 0, 3);

    grid->addWidget(new CpuChartWidget(this), 1, 0, 1, 2);
    grid->addWidget(new RamChartWidget(this), 1, 2, 1, 2);

    root->addLayout(grid, 1);

    auto* activityPanel = new QFrame(this);
    activityPanel->setObjectName(QStringLiteral("activityPanel"));
    auto* activityLayout = new QVBoxLayout(activityPanel);
    activityLayout->setContentsMargins(16, 14, 16, 14);
    activityLayout->setSpacing(8);

    auto* activityTitle = new QLabel(QStringLiteral("Activite recente"), activityPanel);
    activityTitle->setObjectName(QStringLiteral("panelHeader"));
    activityLayout->addWidget(activityTitle);

    activityLayout->addWidget(makeActivityRow(QStringLiteral("14:32"), QStringLiteral("Macro"), QStringLiteral("Diablo IV — Rotation Boss (Touche W)"), activityPanel));
    activityLayout->addWidget(makeActivityRow(QStringLiteral("14:18"), QStringLiteral("Profil"), QStringLiteral("Profil actif change : Diablo IV - Main"), activityPanel));
    activityLayout->addWidget(makeActivityRow(QStringLiteral("13:55"), QStringLiteral("Peripherique"), QStringLiteral("Elite M40 — DPI passe a 1600"), activityPanel));
    activityLayout->addWidget(makeActivityRow(QStringLiteral("13:40"), QStringLiteral("Macro"), QStringLiteral("Loot rapide (Touche F) — 128 executions"), activityPanel));

    root->addWidget(activityPanel);
}
