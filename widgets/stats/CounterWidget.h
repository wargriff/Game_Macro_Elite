#pragma once

#include <QFrame>

class CounterWidget : public QFrame
{
    Q_OBJECT
public:
    CounterWidget(const QString& value, const QString& label, const QString& role, QWidget* parent = nullptr);
};
