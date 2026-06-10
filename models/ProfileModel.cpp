#include "ProfileModel.h"

ProfileModel::ProfileModel()
{
    m_profiles = {
        { QStringLiteral("Diablo IV - Main"), QStringLiteral("Diablo IV"), true, true },
        { QStringLiteral("Diablo III - Season"), QStringLiteral("Diablo III"), true, true },
        { QStringLiteral("WoW Raid"), QStringLiteral("World of Warcraft"), false, true },
        { QStringLiteral("Valorant Comp"), QStringLiteral("Valorant"), true, true }
    };
}
