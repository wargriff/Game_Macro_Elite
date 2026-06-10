#include <QtTest>
class WidgetTests : public QObject { Q_OBJECT private slots: void passTest(){ QVERIFY(true);} };
QTEST_MAIN(WidgetTests)
#include "WidgetTests.moc"
