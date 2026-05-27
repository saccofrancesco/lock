#include "crypto/encryptor.h"

#include <QCoreApplication>
#include <QTextStream>

int main(int argc, char *argv[]) {
    QCoreApplication app(argc, argv);
    QTextStream out(stdout);

    const QStringList args = QCoreApplication::arguments();
    if (args.size() < 4) {
        out << "usage: crypto_probe <encrypt|decrypt> <password> <value>\n";
        return 2;
    }

    const QString mode = args.at(1);
    const QString password = args.at(2);
    const QString value = args.at(3);

    if (mode == QStringLiteral("encrypt")) {
        const QByteArray token = crypto::encryptWrapped(value, password);
        out << token << '\n';
        return token.isEmpty() ? 1 : 0;
    }

    if (mode == QStringLiteral("decrypt")) {
        const crypto::DecryptResult result = crypto::decryptWrapped(value.toLatin1(), password);
        out << (result.ok ? "OK:" : "ERR:") << result.value << '\n';
        return result.ok ? 0 : 1;
    }

    out << "invalid mode\n";
    return 2;
}
