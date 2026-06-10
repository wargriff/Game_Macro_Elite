#include "Logger.h"
#include <QDebug>

void Logger::info(const QString& msg)  { qInfo().noquote()     << "[GAMEX]" << msg; }
void Logger::warn(const QString& msg)  { qWarning().noquote()  << "[GAMEX]" << msg; }
void Logger::error(const QString& msg) { qCritical().noquote() << "[GAMEX]" << msg; }
void Logger::debug(const QString& msg) { qDebug().noquote()    << "[GAMEX][DEBUG]" << msg; }
