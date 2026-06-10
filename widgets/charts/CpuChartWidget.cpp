#include "CpuChartWidget.h"
#include <QPainter>
CpuChartWidget::CpuChartWidget(QWidget* p):QWidget(p){ setMinimumSize(200,120);} 
void CpuChartWidget::paintEvent(QPaintEvent*){ QPainter g(this); g.fillRect(rect(),QColor(24,24,30)); g.setPen(QColor(224,38,38)); for(int x=0;x<width();x+=8) g.drawLine(x,height(),x+40,0); }
