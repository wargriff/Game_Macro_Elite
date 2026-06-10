#pragma once

#include "../core/Enums.h"

class RGBService
{
public:
    RGBService();
    RgbEffect effect() const { return m_effect; }
    void setEffect(RgbEffect e) { m_effect = e; }
    float speed() const { return m_speed; }
    float brightness() const { return m_brightness; }
    void setSpeed(float s) { m_speed = s; }
    void setBrightness(float b) { m_brightness = b; }

private:
    RgbEffect m_effect = RgbEffect::Rainbow;
    float m_speed = 0.65f;
    float m_brightness = 0.80f;
};
