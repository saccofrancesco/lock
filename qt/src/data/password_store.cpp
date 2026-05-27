#include "data/password_store.h"

#include "crypto/encryptor.h"

#include <QByteArray>
#include <QDir>
#include <QFileInfo>
#include <QSqlError>
#include <QSqlQuery>
#include <QUuid>

namespace {

bool isAllowedCriteria(const QString &criteria) {
    return criteria == QLatin1String("email") || criteria == QLatin1String("username") ||
           criteria == QLatin1String("url") || criteria == QLatin1String("service");
}

} // namespace

PasswordStore::PasswordStore(const QString &dbPath)
    : connectionName_(QStringLiteral("lock_qt_%1").arg(QUuid::createUuid().toString(QUuid::Id128))),
      db_(QSqlDatabase::addDatabase(QStringLiteral("QSQLITE"), connectionName_)) {
    QFileInfo info(dbPath);
    if (info.dir().exists() || info.dir().mkpath(QStringLiteral("."))) {
        db_.setDatabaseName(dbPath);
    } else {
        db_.setDatabaseName(QStringLiteral(".database.db"));
    }

    open();
    ensureTable();
}

PasswordStore::~PasswordStore() {
    if (db_.isOpen()) {
        db_.close();
    }
    const QString name = connectionName_;
    db_ = QSqlDatabase();
    QSqlDatabase::removeDatabase(name);
}

bool PasswordStore::open() {
    if (db_.isOpen()) {
        return true;
    }

    return db_.open();
}

bool PasswordStore::ensureTable() {
    if (!open()) {
        return false;
    }

    QSqlQuery query(db_);
    const bool ok = query.exec(
        QStringLiteral("CREATE TABLE IF NOT EXISTS passwords ("
                       "password BLOB,"
                       "email TEXT,"
                       "username TEXT,"
                       "url TEXT,"
                       "service TEXT)")
    );

    return ok;
}

bool PasswordStore::createPassword(
    const QString &master,
    const QString &password,
    const QString &email,
    const QString &username,
    const QString &url,
    const QString &service
) {
    if (!ensureTable()) {
        return false;
    }

    const QByteArray encrypted = crypto::encryptWrapped(password, master);
    if (encrypted.isEmpty()) {
        return false;
    }

    QSqlQuery query(db_);
    query.prepare(QStringLiteral("INSERT INTO passwords VALUES (?, ?, ?, ?, ?)"));
    query.addBindValue(encrypted);
    query.addBindValue(email);
    query.addBindValue(username);
    query.addBindValue(url);
    query.addBindValue(service);

    return query.exec();
}

bool PasswordStore::updatePassword(
    const QString &master,
    const QString &newPassword,
    const QString &email,
    const QString &username,
    const QString &url,
    const QString &service
) {
    if (!ensureTable()) {
        return false;
    }

    QSqlQuery select(db_);
    select.prepare(
        QStringLiteral("SELECT password FROM passwords WHERE email=? AND username=? AND url=? AND service=?")
    );
    select.addBindValue(email);
    select.addBindValue(username);
    select.addBindValue(url);
    select.addBindValue(service);

    if (!select.exec() || !select.next()) {
        return false;
    }

    const QByteArray existingToken = select.value(0).toByteArray();
    const crypto::DecryptResult check = crypto::decryptWrapped(existingToken, master);
    if (!check.ok) {
        return false;
    }

    const QByteArray encrypted = crypto::encryptWrapped(newPassword, master);
    if (encrypted.isEmpty()) {
        return false;
    }

    QSqlQuery update(db_);
    update.prepare(
        QStringLiteral("UPDATE passwords SET password=? WHERE email=? AND username=? AND url=? AND service=?")
    );
    update.addBindValue(encrypted);
    update.addBindValue(email);
    update.addBindValue(username);
    update.addBindValue(url);
    update.addBindValue(service);

    return update.exec();
}

bool PasswordStore::deletePassword(
    const QString &master,
    const QString &email,
    const QString &username,
    const QString &url,
    const QString &service
) {
    if (!ensureTable()) {
        return false;
    }

    QSqlQuery select(db_);
    select.prepare(
        QStringLiteral("SELECT password FROM passwords WHERE email=? AND username=? AND url=? AND service=?")
    );
    select.addBindValue(email);
    select.addBindValue(username);
    select.addBindValue(url);
    select.addBindValue(service);

    if (!select.exec() || !select.next()) {
        return false;
    }

    const QByteArray existingToken = select.value(0).toByteArray();
    const crypto::DecryptResult check = crypto::decryptWrapped(existingToken, master);
    if (!check.ok) {
        return false;
    }

    QSqlQuery remove(db_);
    remove.prepare(QStringLiteral("DELETE FROM passwords WHERE email=? AND username=? AND url=? AND service=?"));
    remove.addBindValue(email);
    remove.addBindValue(username);
    remove.addBindValue(url);
    remove.addBindValue(service);

    return remove.exec();
}

QStringList PasswordStore::searchPasswords(const QString &master, const QString &criteria, const QString &value) {
    if (!ensureTable() || !isAllowedCriteria(criteria)) {
        return {};
    }

    QSqlQuery query(db_);
    query.prepare(QStringLiteral("SELECT password FROM passwords WHERE %1=?").arg(criteria));
    query.addBindValue(value);

    if (!query.exec()) {
        return {};
    }

    QStringList decrypted;
    while (query.next()) {
        const QByteArray token = query.value(0).toByteArray();
        const crypto::DecryptResult result = crypto::decryptWrapped(token, master);
        decrypted << result.value;
    }

    return decrypted;
}

QStringList PasswordStore::listPasswords(const QString &master) {
    if (!ensureTable()) {
        return {};
    }

    QSqlQuery query(db_);
    if (!query.exec(QStringLiteral("SELECT password FROM passwords"))) {
        return {};
    }

    QStringList decrypted;
    while (query.next()) {
        const QByteArray token = query.value(0).toByteArray();
        const crypto::DecryptResult result = crypto::decryptWrapped(token, master);
        decrypted << result.value;
    }

    return decrypted;
}
