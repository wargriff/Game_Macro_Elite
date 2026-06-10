#pragma once

#include "../models/ProfileModel.h"

class ProfileService
{
public:
    static ProfileService& instance();

    ProfileModel& model() { return m_model; }
    const ProfileModel& model() const { return m_model; }

    void applyProfile(int index);
    int activeIndex() const;

private:
    ProfileService() = default;
    ProfileModel m_model;
};
