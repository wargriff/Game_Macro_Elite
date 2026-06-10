#pragma once

#include <QWidget>

class QLabel;
class QProgressBar;

class TitleBarWidget : public QWidget
{
    Q_OBJECT
public:
    explicit TitleBarWidget(QWidget* parent = nullptr);

signals:
    void minimizeClicked();
    void maximizeClicked();
    void closeClicked();

private:
    void buildUi();
    void refresh();
    void showProfileMenu();

    QLabel* m_sectionLabel = nullptr;
    QLabel* m_profileLabel = nullptr;
    QLabel* m_engineBadge = nullptr;
    QProgressBar* m_cpuBar = nullptr;
    QProgressBar* m_ramBar = nullptr;
};
