#include "dialogs/update_dialog.h"

#include "data/password_store.h"
#include "theme.h"
#include "widgets/password_field.h"
#include "widgets/style_helpers.h"

#include <QDialog>
#include <QHBoxLayout>
#include <QLineEdit>
#include <QPushButton>
#include <QVBoxLayout>
#include <QWidget>

UpdateDialog::UpdateDialog(PasswordStore &store, QWidget *parent)
    : QDialog(parent),
      store_(store),
      masterEntry_(nullptr),
      newPasswordEntry_(nullptr),
      emailEntry_(nullptr),
      usernameEntry_(nullptr),
      urlEntry_(nullptr),
      serviceEntry_(nullptr),
      updateButton_(nullptr) {
    setWindowTitle(QStringLiteral("Update Password"));
    setFixedSize(300, 350);
    setStyleSheet(QString("background-color: %1;").arg(theme::nord0().name()));

    auto *outerLayout = new QVBoxLayout(this);
    outerLayout->setContentsMargins(10, 10, 10, 10);

    auto *frame = new QWidget(this);
    frame->setStyleSheet(QString("background-color: %1; border-radius: 8px;").arg(theme::nord1().name()));
    outerLayout->addWidget(frame);

    auto *frameLayout = new QVBoxLayout(frame);
    frameLayout->setContentsMargins(10, 10, 10, 10);
    frameLayout->setSpacing(8);

    masterEntry_ = new PasswordField(QStringLiteral("Master Password"), frame);
    newPasswordEntry_ = new PasswordField(QStringLiteral("New Password"), frame);
    emailEntry_ = style::createEntry(QStringLiteral("Email"), frame);
    usernameEntry_ = style::createEntry(QStringLiteral("Username"), frame);
    urlEntry_ = style::createEntry(QStringLiteral("URL"), frame);
    serviceEntry_ = style::createEntry(QStringLiteral("Service"), frame);

    frameLayout->addWidget(masterEntry_);
    frameLayout->addWidget(newPasswordEntry_);
    frameLayout->addWidget(emailEntry_);
    frameLayout->addWidget(usernameEntry_);
    frameLayout->addWidget(urlEntry_);
    frameLayout->addWidget(serviceEntry_);

    auto *buttonRow = new QHBoxLayout;
    buttonRow->setContentsMargins(0, 0, 0, 0);
    buttonRow->setSpacing(10);

    updateButton_ = new QPushButton(QStringLiteral("Update"), frame);
    buttonRow->addWidget(updateButton_);

    auto *cancelButton = new QPushButton(QStringLiteral("Cancel"), frame);
    style::setFixedButtonStyle(cancelButton, theme::nord3(), theme::nord4());
    buttonRow->addWidget(cancelButton);

    buttonRow->addStretch();
    frameLayout->addLayout(buttonRow);

    connect(masterEntry_->lineEdit(), &QLineEdit::textChanged, this, [this] { updateUpdateButtonState(); });
    connect(newPasswordEntry_->lineEdit(), &QLineEdit::textChanged, this, [this] { updateUpdateButtonState(); });
    connect(emailEntry_, &QLineEdit::textChanged, this, [this] { updateUpdateButtonState(); });
    connect(usernameEntry_, &QLineEdit::textChanged, this, [this] { updateUpdateButtonState(); });
    connect(urlEntry_, &QLineEdit::textChanged, this, [this] { updateUpdateButtonState(); });
    connect(serviceEntry_, &QLineEdit::textChanged, this, [this] { updateUpdateButtonState(); });

    connect(updateButton_, &QPushButton::clicked, this, &UpdateDialog::onUpdate);
    connect(cancelButton, &QPushButton::clicked, this, &QDialog::close);

    updateUpdateButtonState();
}

void UpdateDialog::updateUpdateButtonState() {
    const bool firstTwoFilled = !masterEntry_->text().isEmpty() && !newPasswordEntry_->text().isEmpty();
    const bool anyFilterFilled = !emailEntry_->text().isEmpty() || !usernameEntry_->text().isEmpty() ||
                                 !urlEntry_->text().isEmpty() || !serviceEntry_->text().isEmpty();

    style::setButtonState(updateButton_, firstTwoFilled && anyFilterFilled, theme::nord13(), theme::nord0(), theme::nord2());
}

void UpdateDialog::onUpdate() {
    store_.updatePassword(
        masterEntry_->text(),
        newPasswordEntry_->text(),
        emailEntry_->text(),
        usernameEntry_->text(),
        urlEntry_->text(),
        serviceEntry_->text()
    );

    close();
}
