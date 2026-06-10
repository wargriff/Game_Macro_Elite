#include "RGBPanelWidget.h"
#include <QComboBox>
#include <QHBoxLayout>
#include <QLabel>
#include <QPushButton>
#include <QSlider>
#include <QVBoxLayout>

RGBPanelWidget::RGBPanelWidget(RGBService* rgb, QWidget* parent)
    : QWidget(parent)
    , m_rgb(rgb)
{
    setObjectName(QStringLiteral("rgbPanel"));
    auto* layout = new QVBoxLayout(this);
    layout->addWidget(new QLabel(QStringLiteral("Effets lumineux"), this));

    auto* row = new QHBoxLayout();
    auto* preset = new QComboBox(this);
    preset->addItems({ QStringLiteral("Arc-en-ciel"), QStringLiteral("Vague"), QStringLiteral("Respiration") });
    row->addWidget(preset);
    auto* dir = new QComboBox(this);
    dir->addItem(QStringLiteral("Gauche → Droite"));
    row->addWidget(dir);
    layout->addLayout(row);

    auto* speed = new QSlider(Qt::Horizontal, this);
    speed->setRange(0, 100);
    speed->setValue(m_rgb ? int(m_rgb->speed() * 100) : 65);
    layout->addWidget(new QLabel(QStringLiteral("Vitesse"), this));
    layout->addWidget(speed);

    auto* bright = new QSlider(Qt::Horizontal, this);
    bright->setRange(0, 100);
    bright->setValue(m_rgb ? int(m_rgb->brightness() * 100) : 80);
    layout->addWidget(new QLabel(QStringLiteral("Luminosite"), this));
    layout->addWidget(bright);

    auto* sync = new QPushButton(QStringLiteral("Synchroniser"), this);
    sync->setObjectName(QStringLiteral("syncButton"));
    layout->addWidget(sync);
}
