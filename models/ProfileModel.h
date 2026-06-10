#pragma once

#include <QString>
#include <QVector>

struct GameProfile
{
    QString name;
    QString game;
    bool cloud = false;
    bool autoDetect = true;
};

class ProfileModel
{
public:
    ProfileModel();
    const QVector<GameProfile>& profiles() const { return m_profiles; }

private:
    QVector<GameProfile> m_profiles;
};
