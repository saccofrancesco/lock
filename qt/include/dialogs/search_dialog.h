#pragma once

#include <QDialog>

class PasswordStore;

class SearchDialog : public QDialog {
public:
    SearchDialog(
        PasswordStore &store,
        const QString &firstCriteria,
        const QString &secondCriteria,
        QWidget *parent = nullptr
    );
};
