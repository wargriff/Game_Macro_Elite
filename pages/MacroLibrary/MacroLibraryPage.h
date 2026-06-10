#pragma once
#include <QWidget>

class MacroLibraryPage : public QWidget
{
    Q_OBJECT
public:
    explicit MacroLibraryPage(QWidget* parent = nullptr);

private slots:
    void refreshList();
    void onAddMacro();
    void onCellChanged(int row, int column);

private:
    void updateStatusCell(int row);

    class QTableWidget* m_table = nullptr;
    bool m_blockTableSignals = false;
};
