#pragma once

#include <QWidget>

class QLineEdit;
class QPushButton;

class PasswordField : public QWidget {
public:
    explicit PasswordField(const QString &placeholderText, QWidget *parent = nullptr);

    QString text() const;
    QLineEdit *lineEdit() const;

private:
    void togglePassword();

    bool showPassword_;
    QLineEdit *entry_;
    QPushButton *toggle_;
};
