#pragma once

#include "data/password_store.h"

#include <QMainWindow>

class CreateDialog;
class DeleteDialog;
class ListDialog;
class SearchDialog;
class UpdateDialog;

class MainWindow : public QMainWindow {
public:
    explicit MainWindow(QWidget *parent = nullptr);

private:
    void setupUi();
    void openCreateDialog();
    void openUpdateDialog();
    void openDeleteDialog();
    void openSearchByUrlDialog();
    void openSearchByUserDialog();
    void openListDialog();

    PasswordStore store_;

    CreateDialog *createDialog_;
    UpdateDialog *updateDialog_;
    DeleteDialog *deleteDialog_;
    SearchDialog *searchByUrlDialog_;
    SearchDialog *searchByUserDialog_;
    ListDialog *listDialog_;
};
