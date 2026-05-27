#pragma once

#include <QDialog>

class PasswordField;
class PasswordStore;
class QLabel;
class QPushButton;

class ListDialog : public QDialog {
public:
    explicit ListDialog(PasswordStore &store, QWidget *parent = nullptr);

private:
    void updateListButtonState();
    void onList();

    PasswordStore &store_;
    PasswordField *masterEntry_;
    QLabel *resultsLabel_;
    QPushButton *listButton_;
};
