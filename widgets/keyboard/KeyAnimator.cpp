#include "KeyAnimator.h"

KeyAnimator::KeyAnimator(QObject* parent) : QObject(parent) {}

void KeyAnimator::tick(float dt)
{
    m_phase += dt;
    if (m_phase > 1000.f) m_phase = 0.f;
}
