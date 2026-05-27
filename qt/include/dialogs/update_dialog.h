#pragma once

#include <QDialog>

class PasswordField;
class PasswordStore;
class QLineEdit;
class QPushButton;

class UpdateDialog : public QDialog {
public:
    explicit UpdateDialog(PasswordStore &store, QWidget *parent = nullptr);

private:
    void updateUpdateButtonState();
    void onUpdate();

    PasswordStore &store_;
    PasswordField *masterEntry_;
    PasswordField *newPasswordEntry_;
    QLineEdit *emailEntry_;
    QLineEdit *usernameEntry_;
    QLineEdit *urlEntry_;
    QLineEdit *serviceEntry_;
    QPushButton *updateButton_;
};
