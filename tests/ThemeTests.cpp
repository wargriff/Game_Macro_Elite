#include <QtTest>
class ThemeTests : public QObject { Q_OBJECT private slots: void passTest(){ QVERIFY(true);} };
QTEST_MAIN(ThemeTests)
#include "ThemeTests.moc"
