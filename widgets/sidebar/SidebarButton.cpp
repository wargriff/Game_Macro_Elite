#include "SidebarButton.h"
#include "../../core/AssetGenerator.h"
#include <QHBoxLayout>
#include <QLabel>
#include <QStyle>

SidebarButton::SidebarButton(NavSection section, const QString& iconAsset, const QString& label, QWidget* parent)
    : QPushButton(parent)
    , m_section(section)
{
    setObjectName(QStringLiteral("sidebarButton"));
    setCheckable(true);
    setCursor(Qt::PointingHandCursor);
    setMinimumHeight(44);

    auto* layout = new QHBoxLayout(this);
    layout->setContentsMargins(10, 6, 10, 6);
    layout->setSpacing(10);

    auto* iconLabel = new QLabel(this);
    iconLabel->setFixedSize(26, 26);
    iconLabel->setPixmap(AssetGenerator::instance().pixmap(iconAsset, QSize(26, 26)));
    iconLabel->setScaledContents(true);
    iconLabel->setAttribute(Qt::WA_TransparentForMouseEvents);
    layout->addWidget(iconLabel);

    auto* textLabel = new QLabel(label, this);
    textLabel->setObjectName(QStringLiteral("sidebarButtonText"));
    textLabel->setAttribute(Qt::WA_TransparentForMouseEvents);
    layout->addWidget(textLabel, 1);
}

void SidebarButton::setActive(bool active)
{
    setChecked(active);
    setProperty("active", active);
    style()->unpolish(this);
    style()->polish(this);
}
