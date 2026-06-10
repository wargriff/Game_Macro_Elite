#include "StatsPanelWidget.h"
#include "CounterWidget.h"
#include <QHBoxLayout>
#include <QLabel>
#include <QVBoxLayout>

StatsPanelWidget::StatsPanelWidget(QWidget* parent) : QWidget(parent)
{
    auto* layout = new QVBoxLayout(this);
    layout->addWidget(new QLabel(QStringLiteral("Touches assignees"), this));
    auto* row = new QHBoxLayout();
    const auto& st = AppStateStore::instance().state();
    row->addWidget(new CounterWidget(QString::number(st.macroCount), QStringLiteral("Macros"), QStringLiteral("macro"), this));
    row->addWidget(new CounterWidget(QString::number(st.functionCount), QStringLiteral("Fonctions"), QStringLiteral("function"), this));
    row->addWidget(new CounterWidget(QString::number(st.disabledCount), QStringLiteral("Desactivees"), QStringLiteral("disabled"), this));
    layout->addLayout(row);
}
