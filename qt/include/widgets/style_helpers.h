#pragma once

#include "theme.h"

#include <QColor>
#include <QLineEdit>
#include <QPushButton>
#include <QString>

namespace style {

inline QString entryStyle() {
    return QString(
               "QLineEdit {"
               " background-color: %1;"
               " color: %2;"
               " border: none;"
               " border-radius: 6px;"
               " padding: 7px 9px;"
               " lineedit-password-character: 9679;"
               "}"
           )
        .arg(theme::nord0().name(), theme::nord4().name());
}

inline QLineEdit *createEntry(const QString &placeholder, QWidget *parent) {
    auto *entry = new QLineEdit(parent);
    entry->setPlaceholderText(placeholder);
    entry->setStyleSheet(entryStyle());
    return entry;
}

inline void setButtonState(
    QPushButton *button,
    bool enabled,
    const QColor &enabledColor,
    const QColor &disabledColor,
    const QColor &textColor
) {
    button->setEnabled(enabled);
    const QColor bg = enabled ? enabledColor : disabledColor;
    const QColor hover = enabled ? QColor(theme::darkenHex(enabledColor)) : disabledColor;

    button->setStyleSheet(QString(
                              "QPushButton {"
                              " background-color: %1;"
                              " color: %2;"
                              " border: none;"
                              " border-radius: 6px;"
                              " padding: 7px 12px;"
                              "}"
                              "QPushButton:hover {"
                              " background-color: %3;"
                              "}"
                          )
                              .arg(bg.name(), textColor.name(), hover.name()));
}

inline void setFixedButtonStyle(QPushButton *button, const QColor &bg, const QColor &textColor) {
    const QColor hover(theme::darkenHex(bg));

    button->setStyleSheet(QString(
                              "QPushButton {"
                              " background-color: %1;"
                              " color: %2;"
                              " border: none;"
                              " border-radius: 6px;"
                              " padding: 7px 12px;"
                              "}"
                              "QPushButton:hover {"
                              " background-color: %3;"
                              "}"
                          )
                              .arg(bg.name(), textColor.name(), hover.name()));
}

} // namespace style
