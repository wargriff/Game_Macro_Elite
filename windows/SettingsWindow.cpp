#include "SettingsWindow.h"
#include <QLabel>
#include <QVBoxLayout>
SettingsWindow::SettingsWindow(QWidget* p):QDialog(p){ setWindowTitle("Parametres"); (new QVBoxLayout(this))->addWidget(new QLabel("Settings Hub",this)); }
