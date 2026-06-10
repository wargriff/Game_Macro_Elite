#include "InfoCard.h"
#include <QLabel>
#include <QVBoxLayout>

InfoCard::InfoCard(const QString& title, const QString& value, const QString& subtitle, QWidget* parent)
    : QFrame(parent)
{
    setObjectName(QStringLiteral("infoCard"));
    auto* l = new QVBoxLayout(this);
    l->addWidget(new QLabel(title, this));
    auto* v = new QLabel(value, this);
    v->setObjectName(QStringLiteral("infoCardValue"));
    l->addWidget(v);
    if (!subtitle.isEmpty()) l->addWidget(new QLabel(subtitle, this));
}
