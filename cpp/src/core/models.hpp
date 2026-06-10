#pragma once

#include <cstdint>
#include <deque>
#include <mutex>
#include <string>
#include <unordered_map>

namespace gx {

struct Btn {
    int cps = 10;
    double delay = 0.01;
    bool active = false;
    int burst_count = 0;
};

struct Stats {
    std::deque<double> timestamps;
    int cps = 0;
    std::mutex lock;
};

}  // namespace gx
