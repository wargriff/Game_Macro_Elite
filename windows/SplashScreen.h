#pragma once
#include <QSplashScreen>
class SplashScreen : public QSplashScreen {
public:
    explicit SplashScreen(const QPixmap& px, QWidget* parent = nullptr);
};
