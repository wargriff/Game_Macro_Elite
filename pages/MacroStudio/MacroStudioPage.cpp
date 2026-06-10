#include "MacroStudioPage.h"
#include <QLabel>
#include <QVBoxLayout>

MacroStudioPage::MacroStudioPage(QWidget* parent) : QWidget(parent)
{
    auto* l = new QVBoxLayout(this);
    l->addWidget(new QLabel(QStringLiteral("Macro Studio — Editeur timeline"), this));
}
