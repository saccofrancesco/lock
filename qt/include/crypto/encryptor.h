#pragma once

#include <QByteArray>
#include <QString>

namespace crypto {

struct DecryptResult {
    bool ok;
    QString value;
};

QByteArray encryptWrapped(const QString &message, const QString &password, int iterations = 100000);
DecryptResult decryptWrapped(
    const QByteArray &token,
    const QString &password,
    const QString &errorIndicator = QStringLiteral("Decryption failed")
);

} // namespace crypto
