#include "core/rgb_engine.hpp"

#include <algorithm>
#include <chrono>
#include <cmath>

namespace {

double now_sec() {
    using clock = std::chrono::steady_clock;
    return std::chrono::duration<double>(clock::now().time_since_epoch()).count();
}

}  // namespace

namespace gx {

RgbEngine::RgbEngine() {
    for (const auto* z : {"left", "right", "wheel", "dpi", "side1", "side2"}) {
        zones_[z] = RgbZone{};
    }
    last_ = now_sec();
}

void RgbEngine::update() {
    const double now = now_sec();
    const double dt = now - last_;
    last_ = now;
    t_ += dt * speed;
    for (auto& [name, z] : zones_) {
        (void)name;
        if (z.flash > 0) {
            z.flash -= dt * 3.0;
            if (z.flash < 0) z.flash = 0;
        }
    }
}

void RgbEngine::set_mode(const std::string& zone, const std::string& mode) {
    auto it = zones_.find(zone);
    if (it != zones_.end()) it->second.mode = mode;
}

void RgbEngine::set_color(const std::string& zone, const RgbColor& color) {
    auto it = zones_.find(zone);
    if (it != zones_.end()) it->second.color = color;
}

RgbColor RgbEngine::get_color(const std::string& zone) const {
    auto it = zones_.find(zone);
    if (it == zones_.end()) return {0, 255, 120};
    const auto& z = it->second;
    if (z.mode == "static") return z.color;
    if (z.mode == "breathing") {
        const double factor = (std::sin(t_) + 1.0) / 2.0;
        return scale(z.color, factor);
    }
    if (z.mode == "rainbow") return rainbow();
    if (z.mode == "reactive") return scale(z.color, 0.3 + z.flash);
    return z.color;
}

void RgbEngine::trigger_reactive(const std::string& zone) {
    auto it = zones_.find(zone);
    if (it != zones_.end()) it->second.flash = 1.0;
}

RgbColor RgbEngine::scale(const RgbColor& c, double factor) const {
    factor = std::clamp(factor, 0.0, 1.0);
    return {static_cast<std::uint8_t>(c.r * factor),
            static_cast<std::uint8_t>(c.g * factor),
            static_cast<std::uint8_t>(c.b * factor)};
}

RgbColor RgbEngine::rainbow() const {
    const double h = std::fmod(t_ * 60.0, 360.0);
    const double s = 1.0, v = 1.0;
    const double c = v * s;
    const double x = c * (1.0 - std::fabs(std::fmod(h / 60.0, 2.0) - 1.0));
    const double m = v - c;
    double r = 0, g = 0, b = 0;
    if (h < 60) {
        r = c;
        g = x;
    } else if (h < 120) {
        r = x;
        g = c;
    } else if (h < 180) {
        g = c;
        b = x;
    } else if (h < 240) {
        g = x;
        b = c;
    } else if (h < 300) {
        r = x;
        b = c;
    } else {
        r = c;
        b = x;
    }
    return {static_cast<std::uint8_t>((r + m) * 255),
            static_cast<std::uint8_t>((g + m) * 255),
            static_cast<std::uint8_t>((b + m) * 255)};
}

}  // namespace gx
