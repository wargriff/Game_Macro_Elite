#include "DashboardPage.h"
#include "../../widgets/charts/CpuChartWidget.h"
#include "../../widgets/charts/RamChartWidget.h"
#include "../../widgets/cards/InfoCard.h"
#include "../../core/AppState.h"
#include <QGridLayout>
#include <QLabel>
#include <QVBoxLayout>

DashboardPage::DashboardPage(QWidget* parent) : QWidget(parent)
{
    auto* root = new QVBoxLayout(this);
    root->addWidget(new QLabel(QStringLiteral("Mission Control"), this));
    auto* grid = new QGridLayout();
    const auto& st = AppStateStore::instance().state();
    grid->addWidget(new InfoCard(QStringLiteral("CPU"), QString::number(int(st.cpuUsage*100)) + QStringLiteral("%"), QString(), this), 0, 0);
    grid->addWidget(new InfoCard(QStringLiteral("RAM"), QString::number(int(st.ramUsage*100)) + QStringLiteral("%"), QString(), this), 0, 1);
    grid->addWidget(new CpuChartWidget(this), 1, 0);
    grid->addWidget(new RamChartWidget(this), 1, 1);
    root->addLayout(grid);
}
