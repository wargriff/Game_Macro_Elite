#include "core/win32_input.hpp"

#include <windows.h>

namespace gx {

void send_mouse(std::uint32_t flag) {
    INPUT inp{};
    inp.type = INPUT_MOUSE;
    inp.mi.dwFlags = flag;
    SendInput(1, &inp, sizeof(INPUT));
}

void send_key(std::uint16_t vk, bool down) {
    INPUT inp{};
    inp.type = INPUT_KEYBOARD;
    inp.ki.wVk = vk;
    if (!down) inp.ki.dwFlags = KEYEVENTF_KEYUP;
    SendInput(1, &inp, sizeof(INPUT));
}

bool key_pressed(int vk) {
    return (GetAsyncKeyState(vk) & 0x8000) != 0;
}

}  // namespace gx
