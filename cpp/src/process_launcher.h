#pragma once

#include <string>

namespace gx {

std::wstring GetProjectRoot();
std::wstring FindPythonExe(const std::wstring& projectRoot);
bool LaunchPythonMode(const std::wstring& projectRoot, const std::wstring& modeArg);
bool LaunchRepair(const std::wstring& projectRoot);
bool LaunchDesktopExe(const std::wstring& projectRoot);
bool FileExists(const std::wstring& path);

}  // namespace gx
