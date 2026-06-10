#include "CounterWidget.h"
#include "../cards/StatsCard.h"
#include <QVBoxLayout>

CounterWidget::CounterWidget(const QString& value, const QString& label, const QString& role, QWidget* parent)
    : QFrame(parent)
{
    auto* card = new StatsCard(value, label, role, this);
    auto* l = new QVBoxLayout(this);
    l->setContentsMargins(0,0,0,0);
    l->addWidget(card);
}
