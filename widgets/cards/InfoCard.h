#pragma once

#include <QFrame>

class InfoCard : public QFrame
{
    Q_OBJECT
public:
    InfoCard(const QString& title, const QString& value, const QString& subtitle, QWidget* parent = nullptr);
};
