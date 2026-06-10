#pragma once

#include <QObject>

class KeyAnimator : public QObject
{
    Q_OBJECT
public:
    explicit KeyAnimator(QObject* parent = nullptr);
    float phase() const { return m_phase; }
    void tick(float dt);

private:
    float m_phase = 0.f;
};
