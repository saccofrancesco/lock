#include "path_utils.h"

#include <QCoreApplication>
#include <QDir>
#include <QFileInfo>
#include <QStringList>

QString resolveAssetPath(const QString &relativePath) {
    const QStringList bases = {
        QDir::currentPath(),
        QCoreApplication::applicationDirPath(),
        QDir(QCoreApplication::applicationDirPath()).filePath(".."),
        QDir(QCoreApplication::applicationDirPath()).filePath("../.."),
        QDir(QCoreApplication::applicationDirPath()).filePath("../../..")
    };

    for (const QString &base : bases) {
        const QString candidate = QDir(base).filePath(relativePath);
        if (QFileInfo::exists(candidate)) {
            return candidate;
        }
    }

    return QDir::current().filePath(relativePath);
}
