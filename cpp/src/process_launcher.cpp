#include "process_launcher.h"

#include <windows.h>
#include <shlobj.h>

#include <filesystem>
#include <vector>

namespace fs = std::filesystem;

namespace gx {

bool FileExists(const std::wstring& path) {
    return fs::exists(path);
}

std::wstring GetProjectRoot() {
    wchar_t buffer[MAX_PATH]{};
    GetModuleFileNameW(nullptr, buffer, MAX_PATH);
    fs::path exe = buffer;

    // cpp/build/Release/GameXClicker.exe -> remonte vers racine projet
    fs::path root = exe.parent_path();
    for (int i = 0; i < 5; ++i) {
        if (fs::exists(root / L"GameXClicker.py") || fs::exists(root / L"launcher.py")) {
            return root.wstring();
        }
        if (!root.has_parent_path()) break;
        root = root.parent_path();
    }
    return exe.parent_path().wstring();
}

std::wstring FindPythonExe(const std::wstring& projectRoot) {
    const fs::path root(projectRoot);
    const fs::path parent = root.parent_path();

    std::vector<fs::path> candidates = {
        parent / L".venv" / L"Scripts" / L"python.exe",
        root / L".venv" / L"Scripts" / L"python.exe",
        root / L"venv" / L"Scripts" / L"python.exe",
    };

    for (const auto& c : candidates) {
        if (fs::exists(c)) return c.wstring();
    }
    return L"python";
}

static bool Spawn(const std::wstring& exe, const std::wstring& args, const std::wstring& cwd) {
    std::wstring cmd = L"\"" + exe + L"\" " + args;
    std::vector<wchar_t> mutableCmd(cmd.begin(), cmd.end());
    mutableCmd.push_back(L'\0');

    STARTUPINFOW si{};
    si.cb = sizeof(si);
    PROCESS_INFORMATION pi{};

    if (!CreateProcessW(nullptr, mutableCmd.data(), nullptr, nullptr, FALSE,
                        CREATE_NEW_CONSOLE, nullptr, cwd.c_str(), &si, &pi)) {
        return false;
    }
    CloseHandle(pi.hThread);
    CloseHandle(pi.hProcess);
    return true;
}

bool LaunchPythonMode(const std::wstring& projectRoot, const std::wstring& modeArg) {
    const std::wstring py = FindPythonExe(projectRoot);
    const fs::path script = fs::path(projectRoot) / L"OUVRE_MOI.py";

    if (modeArg.empty()) {
        return Spawn(py, L"\"" + script.wstring() + L"\"", projectRoot);
    }

    const fs::path gx = fs::path(projectRoot) / L"GameXClicker.py";
    return Spawn(py, L"\"" + gx.wstring() + L"\" " + modeArg, projectRoot);
}

bool LaunchRepair(const std::wstring& projectRoot) {
    const std::wstring py = FindPythonExe(projectRoot);
    const fs::path script = fs::path(projectRoot) / L"REPARER.py";
    if (!fs::exists(script)) return false;
    return Spawn(py, L"\"" + script.wstring() + L"\"", projectRoot);
}

bool LaunchDesktopExe(const std::wstring& projectRoot) {
    wchar_t desktop[MAX_PATH]{};
    if (FAILED(SHGetFolderPathW(nullptr, CSIDL_DESKTOP, nullptr, 0, desktop))) {
        return false;
    }

    fs::path exe = fs::path(desktop) / L"Game XClicker Elite" / L"Game XClicker Elite.exe";
    if (!fs::exists(exe)) {
        exe = fs::path(projectRoot) / L"dist" / L"Game XClicker Elite" / L"Game XClicker Elite.exe";
    }
    if (!fs::exists(exe)) return false;

    HINSTANCE r = ShellExecuteW(nullptr, L"open", exe.c_str(), nullptr, nullptr, SW_SHOWNORMAL);
    return reinterpret_cast<INT_PTR>(r) > 32;
}

}  // namespace gx
