#pragma once

#include "../models/MacroModel.h"

class MacroService
{
public:
    static MacroService& instance();

    MacroModel& model() { return m_model; }
    const MacroModel& model() const { return m_model; }

    int activeProfileIndex() const;
    QVector<MacroEntry>& activeMacros();
    const QVector<MacroEntry>& activeMacros() const;

    void addMacro(const MacroEntry& entry);
    void syncMacroCount();

private:
    MacroService() = default;
    MacroModel m_model;
};
