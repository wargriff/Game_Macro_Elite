#include "MacroService.h"
#include "../core/AppState.h"

MacroService& MacroService::instance()
{
    static MacroService svc;
    return svc;
}

int MacroService::activeProfileIndex() const
{
    return AppStateStore::instance().state().activeProfileIndex;
}

QVector<MacroEntry>& MacroService::activeMacros()
{
    return m_model.macrosForProfile(activeProfileIndex());
}

const QVector<MacroEntry>& MacroService::activeMacros() const
{
    return m_model.macrosForProfile(activeProfileIndex());
}

void MacroService::addMacro(const MacroEntry& entry)
{
    m_model.addMacro(activeProfileIndex(), entry);
    syncMacroCount();
}

void MacroService::syncMacroCount()
{
    AppStateStore::instance().state().macroCount = activeMacros().size();
}
