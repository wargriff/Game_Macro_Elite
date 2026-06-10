#include "SplashScreen.h"
SplashScreen::SplashScreen(const QPixmap& px, QWidget* p):QSplashScreen(px, Qt::WindowStaysOnTopHint){ Q_UNUSED(p); showMessage("GAMEX CLICKER", Qt::AlignBottom|Qt::AlignCenter, Qt::white); }
