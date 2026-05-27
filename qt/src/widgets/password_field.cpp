#include "widgets/password_field.h"

#include "path_utils.h"
#include "theme.h"
#include "widgets/style_helpers.h"

#include <QHBoxLayout>
#include <QIcon>
#include <QLineEdit>
#include <QPushButton>
#include <QSize>

PasswordField::PasswordField(const QString &placeholderText, QWidget *parent)
    : QWidget(parent), showPassword_(false), entry_(nullptr), toggle_(nullptr) {
    auto *layout = new QHBoxLayout(this);
    layout->setContentsMargins(0, 0, 0, 0);
    layout->setSpacing(10);

    entry_ = style::createEntry(placeholderText, this);
    entry_->setEchoMode(QLineEdit::Password);
    layout->addWidget(entry_, 1);

    toggle_ = new QPushButton(this);
    toggle_->setFixedWidth(45);
    toggle_->setIcon(QIcon(resolveAssetPath("assets/icon/open-eye.png")));
    toggle_->setIconSize(QSize(28, 18));
    style::setFixedButtonStyle(toggle_, theme::nord3(), theme::nord4());

    connect(toggle_, &QPushButton::clicked, this, &PasswordField::togglePassword);

    layout->addWidget(toggle_);
}

QString PasswordField::text() const {
    return entry_->text();
}

QLineEdit *PasswordField::lineEdit() const {
    return entry_;
}

void PasswordField::togglePassword() {
    showPassword_ = !showPassword_;
    if (showPassword_) {
        entry_->setEchoMode(QLineEdit::Normal);
        toggle_->setIcon(QIcon(resolveAssetPath("assets/icon/closed-eye.png")));
    } else {
        entry_->setEchoMode(QLineEdit::Password);
        toggle_->setIcon(QIcon(resolveAssetPath("assets/icon/open-eye.png")));
    }
}
