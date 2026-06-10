#include "StatsCard.h"
#include <QLabel>
#include <QVBoxLayout>

StatsCard::StatsCard(const QString& value, const QString& label, const QString& colorRole, QWidget* parent)
    : QFrame(parent)
{
    setObjectName(QStringLiteral("statsCard"));
    setProperty("role", colorRole);
    auto* l = new QVBoxLayout(this);
    auto* v = new QLabel(value, this);
    v->setObjectName(QStringLiteral("statsCardValue"));
    l->addWidget(v, 0, Qt::AlignCenter);
    auto* t = new QLabel(label, this);
    t->setAlignment(Qt::AlignCenter);
    l->addWidget(t);
}
