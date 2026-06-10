#include "DeviceCard.h"
#include <QLabel>
#include <QVBoxLayout>

DeviceCard::DeviceCard(const QString& name, QWidget* parent) : QFrame(parent)
{
    setObjectName(QStringLiteral("deviceCard"));
    auto* l = new QVBoxLayout(this);
    l->addWidget(new QLabel(name, this));
}
