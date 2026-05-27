#pragma once

#include <QDialog>

class PasswordField;
class PasswordStore;
class QLineEdit;
class QPushButton;

class DeleteDialog : public QDialog {
public:
    explicit DeleteDialog(PasswordStore &store, QWidget *parent = nullptr);

private:
    void updateDeleteButtonState();
    void onDelete();

    PasswordStore &store_;
    PasswordField *masterEntry_;
    QLineEdit *emailEntry_;
    QLineEdit *usernameEntry_;
    QLineEdit *urlEntry_;
    QLineEdit *serviceEntry_;
    QPushButton *deleteButton_;
};
