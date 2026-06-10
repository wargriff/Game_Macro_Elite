#pragma once

#include <QMap>
#include <QString>
#include <QVector>

struct MacroEntry
{
    int id = 0;
    QString name;
    QString keyLabel;
    QString device = QStringLiteral("keyboard"); // keyboard | mouse
    double cps = 10.0;
    int delayMs = 100;
    bool active = true;
    bool toggle = false;
    bool gatedByMaster = false;
};

class MacroModel
{
public:
    MacroModel();

    const QVector<MacroEntry>& macrosForProfile(int profileIndex) const;
    QVector<MacroEntry>& macrosForProfile(int profileIndex);

    int selectedIndex() const { return m_selectedIndex; }
    void setSelectedIndex(int index) { m_selectedIndex = index; }

    MacroEntry& selectedMacro(int profileIndex);
    const MacroEntry& selectedMacro(int profileIndex) const;

    void addMacro(int profileIndex, const MacroEntry& entry);

private:
    void seedDefaults();
    QMap<int, QVector<MacroEntry>> m_byProfile;
    int m_selectedIndex = 0;
};
