#include "theme.h"

namespace {
const QColor kNord0("#2E3440");
const QColor kNord1("#3B4252");
const QColor kNord2("#434C5E");
const QColor kNord3("#4C566A");
const QColor kNord4("#D8DEE9");
const QColor kNord7("#8FBCBB");
const QColor kNord8("#88C0D0");
const QColor kNord10("#5E81AC");
const QColor kNord11("#BF616A");
const QColor kNord13("#EBCB8B");
const QColor kNord14("#A3BE8C");
const QColor kNord15("#B48EAD");
} // namespace

namespace theme {

const QColor &nord0() { return kNord0; }
const QColor &nord1() { return kNord1; }
const QColor &nord2() { return kNord2; }
const QColor &nord3() { return kNord3; }
const QColor &nord4() { return kNord4; }
const QColor &nord7() { return kNord7; }
const QColor &nord8() { return kNord8; }
const QColor &nord10() { return kNord10; }
const QColor &nord11() { return kNord11; }
const QColor &nord13() { return kNord13; }
const QColor &nord14() { return kNord14; }
const QColor &nord15() { return kNord15; }

QString darkenHex(const QColor &color, double factor) {
    const int red = static_cast<int>(color.red() * factor);
    const int green = static_cast<int>(color.green() * factor);
    const int blue = static_cast<int>(color.blue() * factor);
    return QColor(red, green, blue).name();
}

} // namespace theme
