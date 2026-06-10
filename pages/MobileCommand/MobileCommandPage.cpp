#include "MobileCommandPage.h"
#include "../../core/AssetGenerator.h"
#include "../../core/Constants.h"
#include <QFrame>
#include <QGridLayout>
#include <QHBoxLayout>
#include <QLabel>
#include <QPushButton>
#include <QVBoxLayout>

namespace
{
QFrame* makeMobileCard(const QString& iconAsset, const QString& title, const QString& desc, QWidget* parent)
{
    auto* card = new QFrame(parent);
    card->setObjectName(QStringLiteral("mobileCard"));

    auto* layout = new QHBoxLayout(card);
    layout->setContentsMargins(16, 14, 16, 14);
    layout->setSpacing(14);

    auto* icon = new QLabel(card);
    icon->setFixedSize(48, 48);
    icon->setPixmap(AssetGenerator::instance().pixmap(iconAsset, QSize(48, 48)));
    icon->setScaledContents(true);
    layout->addWidget(icon);

    auto* textCol = new QVBoxLayout();
    auto* titleLb = new QLabel(title, card);
    titleLb->setObjectName(QStringLiteral("mobileCardTitle"));
    auto* descLb = new QLabel(desc, card);
    descLb->setObjectName(QStringLiteral("mobileCardDesc"));
    descLb->setWordWrap(true);
    textCol->addWidget(titleLb);
    textCol->addWidget(descLb);
    layout->addLayout(textCol, 1);

    return card;
}
}

MobileCommandPage::MobileCommandPage(QWidget* parent) : QWidget(parent)
{
    setObjectName(QStringLiteral("mobileCommandPage"));
    auto* root = new QVBoxLayout(this);
    root->setContentsMargins(24, 16, 24, 16);
    root->setSpacing(16);

    auto* title = new QLabel(QStringLiteral("Mobile Command"), this);
    title->setObjectName(QStringLiteral("pageTitle"));
    root->addWidget(title);

    auto* hero = new QFrame(this);
    hero->setObjectName(QStringLiteral("mobileHero"));
    auto* heroLayout = new QHBoxLayout(hero);
    heroLayout->setContentsMargins(20, 20, 20, 20);

    auto* phone = new QLabel(hero);
    phone->setFixedSize(120, 120);
    phone->setPixmap(AssetGenerator::instance().pixmap(QStringLiteral("icons/mobile-phone.svg"), QSize(120, 120)));
    phone->setScaledContents(true);
    heroLayout->addWidget(phone);

    auto* heroText = new QVBoxLayout();
    heroText->addWidget(new QLabel(QStringLiteral("Controle a distance"), hero));
    auto* status = new QLabel(QStringLiteral("<span style='color:#2ecc71'>●</span> Appareil connecte — iPhone 15 Pro"), hero);
    status->setTextFormat(Qt::RichText);
    heroText->addWidget(status);
    auto* connectBtn = new QPushButton(QStringLiteral("Synchroniser"), hero);
    connectBtn->setObjectName(QStringLiteral("primaryButton"));
    connectBtn->setFixedWidth(160);
    heroText->addWidget(connectBtn);
    heroLayout->addLayout(heroText, 1);

    auto* preview = new QLabel(hero);
    preview->setFixedSize(160, 56);
    preview->setPixmap(AssetGenerator::instance().pixmap(QStringLiteral("previews/mouse-rgb-preview.svg"), QSize(160, 56)));
    preview->setScaledContents(true);
    heroLayout->addWidget(preview);

    root->addWidget(hero);

    auto* grid = new QGridLayout();
    grid->setSpacing(12);
    grid->addWidget(makeMobileCard(QStringLiteral("icons/mobile-sync.svg"),
        QStringLiteral("Sync profils"), QStringLiteral("Synchronise macros et profils entre PC et mobile."), this), 0, 0);
    grid->addWidget(makeMobileCard(QStringLiteral("icons/mobile-remote.svg"),
        QStringLiteral("Telecommande RGB"), QStringLiteral("Controlez l'eclairage en temps reel depuis le telephone."), this), 0, 1);
    grid->addWidget(makeMobileCard(QStringLiteral("icons/mobile-rgb.svg"),
        QStringLiteral("Effets mobiles"), QStringLiteral("Declenchez des effets RGB predefinis a distance."), this), 1, 0);
    grid->addWidget(makeMobileCard(QStringLiteral("devices/mouse.svg"),
        QStringLiteral("Peripheriques"), QStringLiteral("Vue et configuration rapide souris / clavier mobile."), this), 1, 1);
    root->addLayout(grid);
    root->addStretch();
}
