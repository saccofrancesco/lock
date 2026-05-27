#pragma once

#include <QSqlDatabase>
#include <QString>
#include <QStringList>

class PasswordStore {
public:
    explicit PasswordStore(const QString &dbPath = QStringLiteral("database/.database.db"));
    ~PasswordStore();

    bool createPassword(
        const QString &master,
        const QString &password,
        const QString &email,
        const QString &username,
        const QString &url,
        const QString &service
    );

    bool updatePassword(
        const QString &master,
        const QString &newPassword,
        const QString &email,
        const QString &username,
        const QString &url,
        const QString &service
    );

    bool deletePassword(
        const QString &master,
        const QString &email,
        const QString &username,
        const QString &url,
        const QString &service
    );

    QStringList searchPasswords(const QString &master, const QString &criteria, const QString &value);
    QStringList listPasswords(const QString &master);

private:
    bool open();
    bool ensureTable();

    QString connectionName_;
    QSqlDatabase db_;
};
