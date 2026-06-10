#pragma once

#include <cstdint>

namespace gx {

constexpr std::uint32_t MOUSEEVENTF_LEFTDOWN = 0x0002;
constexpr std::uint32_t MOUSEEVENTF_LEFTUP = 0x0004;
constexpr std::uint32_t MOUSEEVENTF_RIGHTDOWN = 0x0008;
constexpr std::uint32_t MOUSEEVENTF_RIGHTUP = 0x0010;

constexpr int VK_LBUTTON = 0x01;
constexpr int VK_RBUTTON = 0x02;
constexpr int VK_XBUTTON1 = 0x05;
constexpr int VK_XBUTTON2 = 0x06;

void send_mouse(std::uint32_t flag);
void send_key(std::uint16_t vk, bool down = true);
bool key_pressed(int vk);

}  // namespace gx
