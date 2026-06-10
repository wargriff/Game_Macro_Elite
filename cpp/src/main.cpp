#include "control_panel.h"

#include <windows.h>

int WINAPI wWinMain(HINSTANCE instance, HINSTANCE, PWSTR, int) {
    gx::ControlPanel panel;
    if (!panel.Create(instance)) {
        MessageBoxW(nullptr,
                    L"Impossible de creer Control Panel.\n\n"
                    L"Placez GameXClicker.exe dans le dossier Game_XClicker_Elite.",
                    L"Game XClicker Elite", MB_ICONERROR);
        return 1;
    }
    return panel.Run();
}
