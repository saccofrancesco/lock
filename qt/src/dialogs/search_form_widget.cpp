#include "dialogs/search_form_widget.h"

#include "data/password_store.h"
#include "theme.h"
#include "widgets/password_field.h"
#include "widgets/style_helpers.h"

#include <QDialog>
#include <QHBoxLayout>
#include <QLabel>
#include <QLineEdit>
#include <QPushButton>
#include <QScrollArea>
#include <QVBoxLayout>
#include <QWidget>

SearchFormWidget::SearchFormWidget(PasswordStore &store, const QString &criteria, QDialog *topLevel, QWidget *parent)
    : QWidget(parent),
      store_(store),
      criteria_(criteria),
      masterEntry_(nullptr),
      criteriaEntry_(nullptr),
      resultsLabel_(nullptr),
      searchButton_(nullptr) {
    auto *layout = new QVBoxLayout(this);
    layout->setContentsMargins(10, 10, 10, 10);
    layout->setSpacing(8);

    masterEntry_ = new PasswordField(QStringLiteral("Master Password"), this);
    layout->addWidget(masterEntry_);

    const QString labelText = criteria.left(1).toUpper() + criteria.mid(1);
    criteriaEntry_ = style::createEntry(QStringLiteral("Enter %1 to search").arg(labelText), this);
    layout->addWidget(criteriaEntry_);

    auto *scrollArea = new QScrollArea(this);
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
    resultsLabel_->setStyleSheet(QString("color: %1;").arg(theme::nord4().name()));
    resultsLabel_->setFont(QFont(QStringLiteral("Arial"), 18));
    resultsLabel_->setAlignment(Qt::AlignTop | Qt::AlignLeft);
    resultsLabel_->setText(QString());
    resultsLabel_->setWordWrap(true);
    resultsLayout->addWidget(resultsLabel_);
    resultsLayout->addStretch();

    scrollArea->setWidget(resultsWidget);
    layout->addWidget(scrollArea, 1);

    auto *buttonRow = new QHBoxLayout;
    buttonRow->setContentsMargins(0, 0, 0, 0);
    buttonRow->setSpacing(10);

    searchButton_ = new QPushButton(QStringLiteral("Search"), this);
    buttonRow->addWidget(searchButton_);

    auto *cancelButton = new QPushButton(QStringLiteral("Cancel"), this);
    style::setFixedButtonStyle(cancelButton, theme::nord3(), theme::nord4());
    buttonRow->addWidget(cancelButton);

    buttonRow->addStretch();
    layout->addLayout(buttonRow);

    connect(masterEntry_->lineEdit(), &QLineEdit::textChanged, this, [this] { updateSearchButtonState(); });
    connect(criteriaEntry_, &QLineEdit::textChanged, this, [this] { updateSearchButtonState(); });

    connect(searchButton_, &QPushButton::clicked, this, &SearchFormWidget::onSearch);
    connect(cancelButton, &QPushButton::clicked, topLevel, &QDialog::close);

    updateSearchButtonState();
}

void SearchFormWidget::updateSearchButtonState() {
    const bool enabled = !masterEntry_->text().isEmpty() && !criteriaEntry_->text().isEmpty();
    style::setButtonState(searchButton_, enabled, theme::nord7(), theme::nord0(), theme::nord2());
}

void SearchFormWidget::onSearch() {
    const QStringList passwords = store_.searchPasswords(masterEntry_->text(), criteria_, criteriaEntry_->text());
    resultsLabel_->setText(passwords.join('\n'));
}
