#include <QtTest>
class DeviceTests : public QObject { Q_OBJECT private slots: void passTest(){ QVERIFY(true);} };
QTEST_MAIN(DeviceTests)
#include "DeviceTests.moc"
