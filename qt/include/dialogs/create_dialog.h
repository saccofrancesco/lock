#pragma once

#include <QDialog>

class PasswordField;
class PasswordStore;
class QLineEdit;
class QPushButton;

class CreateDialog : public QDialog {
public:
    explicit CreateDialog(PasswordStore &store, QWidget *parent = nullptr);

private:
    void updateCreateButtonState();
    void onCreate();

    PasswordStore &store_;
    PasswordField *masterEntry_;
    PasswordField *passwordEntry_;
    QLineEdit *emailEntry_;
    QLineEdit *usernameEntry_;
    QLineEdit *urlEntry_;
    QLineEdit *serviceEntry_;
    QPushButton *createButton_;
};
