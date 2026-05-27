#include "dialogs/create_dialog.h"

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

CreateDialog::CreateDialog(PasswordStore &store, QWidget *parent)
    : QDialog(parent),
      store_(store),
      masterEntry_(nullptr),
      passwordEntry_(nullptr),
      emailEntry_(nullptr),
      usernameEntry_(nullptr),
      urlEntry_(nullptr),
      serviceEntry_(nullptr),
      createButton_(nullptr) {
    setWindowTitle(QStringLiteral("Create Password"));
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
    passwordEntry_ = new PasswordField(QStringLiteral("Password"), frame);
    emailEntry_ = style::createEntry(QStringLiteral("Email"), frame);
    usernameEntry_ = style::createEntry(QStringLiteral("Username"), frame);
    urlEntry_ = style::createEntry(QStringLiteral("URL"), frame);
    serviceEntry_ = style::createEntry(QStringLiteral("Service"), frame);

    frameLayout->addWidget(masterEntry_);
    frameLayout->addWidget(passwordEntry_);
    frameLayout->addWidget(emailEntry_);
    frameLayout->addWidget(usernameEntry_);
    frameLayout->addWidget(urlEntry_);
    frameLayout->addWidget(serviceEntry_);

    auto *buttonRow = new QHBoxLayout;
    buttonRow->setContentsMargins(0, 0, 0, 0);
    buttonRow->setSpacing(10);

    createButton_ = new QPushButton(QStringLiteral("Create"), frame);
    buttonRow->addWidget(createButton_);

    auto *cancelButton = new QPushButton(QStringLiteral("Cancel"), frame);
    style::setFixedButtonStyle(cancelButton, theme::nord3(), theme::nord4());
    buttonRow->addWidget(cancelButton);

    buttonRow->addStretch();
    frameLayout->addLayout(buttonRow);

    connect(masterEntry_->lineEdit(), &QLineEdit::textChanged, this, [this] { updateCreateButtonState(); });
    connect(passwordEntry_->lineEdit(), &QLineEdit::textChanged, this, [this] { updateCreateButtonState(); });
    connect(emailEntry_, &QLineEdit::textChanged, this, [this] { updateCreateButtonState(); });
    connect(usernameEntry_, &QLineEdit::textChanged, this, [this] { updateCreateButtonState(); });
    connect(urlEntry_, &QLineEdit::textChanged, this, [this] { updateCreateButtonState(); });
    connect(serviceEntry_, &QLineEdit::textChanged, this, [this] { updateCreateButtonState(); });

    connect(createButton_, &QPushButton::clicked, this, &CreateDialog::onCreate);
    connect(cancelButton, &QPushButton::clicked, this, &QDialog::close);

    updateCreateButtonState();
}

void CreateDialog::updateCreateButtonState() {
    const bool firstTwoFilled = !masterEntry_->text().isEmpty() && !passwordEntry_->text().isEmpty();
    const bool anyFilterFilled = !emailEntry_->text().isEmpty() || !usernameEntry_->text().isEmpty() ||
                                 !urlEntry_->text().isEmpty() || !serviceEntry_->text().isEmpty();

    style::setButtonState(createButton_, firstTwoFilled && anyFilterFilled, theme::nord14(), theme::nord0(), theme::nord2());
}

void CreateDialog::onCreate() {
    store_.createPassword(
        masterEntry_->text(),
        passwordEntry_->text(),
        emailEntry_->text(),
        usernameEntry_->text(),
        urlEntry_->text(),
        serviceEntry_->text()
    );

    close();
}
