#pragma once

#include <QWidget>

class PasswordField;
class PasswordStore;
class QDialog;
class QLineEdit;
class QLabel;
class QPushButton;

class SearchFormWidget : public QWidget {
public:
    SearchFormWidget(PasswordStore &store, const QString &criteria, QDialog *topLevel, QWidget *parent = nullptr);

private:
    void updateSearchButtonState();
    void onSearch();

    PasswordStore &store_;
    QString criteria_;
    PasswordField *masterEntry_;
    QLineEdit *criteriaEntry_;
    QLabel *resultsLabel_;
    QPushButton *searchButton_;
};
