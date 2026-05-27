#include "dialogs/list_dialog.h"

#include "data/password_store.h"
#include "theme.h"
#include "widgets/password_field.h"
#include "widgets/style_helpers.h"

#include <QFont>
#include <QHBoxLayout>
#include <QLabel>
#include <QPushButton>
#include <QScrollArea>
#include <QVBoxLayout>
#include <QWidget>

ListDialog::ListDialog(PasswordStore &store, QWidget *parent)
    : QDialog(parent), store_(store), masterEntry_(nullptr), resultsLabel_(nullptr), listButton_(nullptr) {
    setWindowTitle(QStringLiteral("List Passwords"));
    setFixedSize(300, 400);
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
    frameLayout->addWidget(masterEntry_);

    auto *scrollArea = new QScrollArea(frame);
    scrollArea->setWidgetResizable(true);
    scrollArea->setFrameShape(QFrame::NoFrame);
    scrollArea->setStyleSheet(QString("background-color: %1; border-radius: 6px;").arg(theme::nord2().name()));

    auto *resultsWidget = new QWidget;
    auto *resultsLayout = new QVBoxLayout(resultsWidget);
    resultsLayout->setContentsMargins(10, 10, 10, 10);

    auto *title = new QLabel(QStringLiteral("Passwords"), resultsWidget);
    title->setStyleSheet(QString("background-color: %1; color: %2; padding: 4px 6px; border-radius: 4px;")
                             .arg(theme::nord3().name(), theme::nord4().name()));
    resultsLayout->addWidget(title);

    resultsLabel_ = new QLabel(resultsWidget);
    resultsLabel_->setFont(QFont(QStringLiteral("Arial"), 18));
    resultsLabel_->setText(QString());
    resultsLabel_->setAlignment(Qt::AlignTop | Qt::AlignLeft);
    resultsLabel_->setWordWrap(true);
    resultsLabel_->setStyleSheet(QString("color: %1;").arg(theme::nord4().name()));
    resultsLayout->addWidget(resultsLabel_);
    resultsLayout->addStretch();

    scrollArea->setWidget(resultsWidget);
    frameLayout->addWidget(scrollArea, 1);

    auto *buttonRow = new QHBoxLayout;
    buttonRow->setContentsMargins(0, 0, 0, 0);
    buttonRow->setSpacing(10);

    listButton_ = new QPushButton(QStringLiteral("List"), frame);
    buttonRow->addWidget(listButton_);

    auto *cancelButton = new QPushButton(QStringLiteral("Cancel"), frame);
    style::setFixedButtonStyle(cancelButton, theme::nord3(), theme::nord4());
    buttonRow->addWidget(cancelButton);

    buttonRow->addStretch();
    frameLayout->addLayout(buttonRow);

    connect(masterEntry_->lineEdit(), &QLineEdit::textChanged, this, [this] { updateListButtonState(); });
    connect(listButton_, &QPushButton::clicked, this, &ListDialog::onList);
    connect(cancelButton, &QPushButton::clicked, this, &QDialog::close);

    updateListButtonState();
}

void ListDialog::updateListButtonState() {
    const bool enabled = !masterEntry_->text().isEmpty();
    style::setButtonState(listButton_, enabled, theme::nord15(), theme::nord0(), theme::nord2());
}

void ListDialog::onList() {
    const QStringList passwords = store_.listPasswords(masterEntry_->text());
    resultsLabel_->setText(passwords.join('\n'));
}
