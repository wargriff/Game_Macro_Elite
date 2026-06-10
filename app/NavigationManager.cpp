#include "NavigationManager.h"
#include "../core/EventBus.h"

NavigationManager::NavigationManager(QObject* parent) : QObject(parent) {}

void NavigationManager::navigateTo(NavSection section)
{
    if (m_section == section) return;
    m_section = section;
    emit sectionChanged(section);
    emit EventBus::instance().sectionChanged(section);
}
