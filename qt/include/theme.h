#pragma once

#include <QColor>
#include <QString>

namespace theme {

const QColor &nord0();
const QColor &nord1();
const QColor &nord2();
const QColor &nord3();
const QColor &nord4();
const QColor &nord7();
const QColor &nord8();
const QColor &nord10();
const QColor &nord11();
const QColor &nord13();
const QColor &nord14();
const QColor &nord15();

QString darkenHex(const QColor &color, double factor = 0.8);

} // namespace theme
