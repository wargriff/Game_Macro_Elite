#include "AboutWindow.h"
#include "../core/Constants.h"
#include <QLabel>
#include <QVBoxLayout>
AboutWindow::AboutWindow(QWidget* p):QDialog(p){ setWindowTitle("A propos"); auto* l=new QVBoxLayout(this); l->addWidget(new QLabel(Gx::App::Name + " " + Gx::App::Version)); }
