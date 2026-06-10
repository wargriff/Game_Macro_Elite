#include "DeviceModel.h"

DeviceModel::DeviceModel()
{
    m_devices = {
        { QStringLiteral("mb"),  QStringLiteral("Motherboard"),     QStringLiteral("MB"),  true,  false, QStringLiteral("—"),   QStringLiteral("F12"),    QStringLiteral("—"),     QStringLiteral("—"),   QStringLiteral("—") },
        { QStringLiteral("gpu"), QStringLiteral("RTX 4080"),       QStringLiteral("GPU"), true,  true,  QStringLiteral("—"),   QStringLiteral("551.23"), QStringLiteral("—"),     QStringLiteral("—"),   QStringLiteral("—") },
        { QStringLiteral("kb"),  QStringLiteral("60% Gaming KB"),  QStringLiteral("KB"),  true,  true,  QStringLiteral("100%"),QStringLiteral("v2.1.4"),  QStringLiteral("1000Hz"),QStringLiteral("—"),   QStringLiteral("—") },
        { QStringLiteral("ms"),  QStringLiteral("Elite M40"),  QStringLiteral("MS"),  true,  true,  QStringLiteral("87%"), QStringLiteral("v1.0.8"),  QStringLiteral("1000Hz"),QStringLiteral("1600"),QStringLiteral("—") },
        { QStringLiteral("hs"),  QStringLiteral("HS80 RGB"),       QStringLiteral("HS"),  true,  true,  QStringLiteral("72%"), QStringLiteral("v1.2.0"),  QStringLiteral("—"),     QStringLiteral("—"),   QStringLiteral("—") },
        { QStringLiteral("aio"), QStringLiteral("H150i Elite"),    QStringLiteral("AIO"), true,  false, QStringLiteral("—"),   QStringLiteral("v1.0.3"),  QStringLiteral("—"),     QStringLiteral("—"),   QStringLiteral("28°") },
        { QStringLiteral("ssd"), QStringLiteral("MP600 PRO"),      QStringLiteral("SSD"), true,  false, QStringLiteral("—"),   QStringLiteral("v1.0"),    QStringLiteral("—"),     QStringLiteral("—"),   QStringLiteral("—") },
        { QStringLiteral("usb"), QStringLiteral("SLIPSTREAM"),     QStringLiteral("USB"), true,  false, QStringLiteral("100%"),QStringLiteral("v5.0"),    QStringLiteral("—"),     QStringLiteral("—"),   QStringLiteral("—") }
    };
}

DeviceInfo& DeviceModel::deviceAt(int index) { return m_devices[index]; }
const DeviceInfo& DeviceModel::deviceAt(int index) const { return m_devices.at(index); }
