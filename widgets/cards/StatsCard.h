#pragma once

#include <QFrame>

class StatsCard : public QFrame
{
    Q_OBJECT
public:
    StatsCard(const QString& value, const QString& label, const QString& colorRole, QWidget* parent = nullptr);
};
