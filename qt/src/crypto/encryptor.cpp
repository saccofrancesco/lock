#include "crypto/encryptor.h"

#include <QByteArray>
#include <QDateTime>

#include <openssl/crypto.h>
#include <openssl/evp.h>
#include <openssl/hmac.h>
#include <openssl/rand.h>

namespace {

constexpr int kDerivedKeyLength = 32;
constexpr int kSaltLength = 16;
constexpr int kIvLength = 16;
constexpr int kHmacLength = 32;
constexpr unsigned char kFernetVersion = 0x80;

QByteArray base64UrlEncode(const QByteArray &input) {
    return input.toBase64(QByteArray::Base64UrlEncoding);
}

QByteArray base64UrlDecode(const QByteArray &input, bool *ok) {
    const auto result = QByteArray::fromBase64Encoding(
        input,
        QByteArray::Base64UrlEncoding | QByteArray::AbortOnBase64DecodingErrors
    );

    const bool valid = result.decodingStatus == QByteArray::Base64DecodingStatus::Ok;
    if (ok != nullptr) {
        *ok = valid;
    }

    return result.decoded;
}

QByteArray deriveKeyRaw(const QString &password, const QByteArray &salt, int iterations) {
    QByteArray key(kDerivedKeyLength, Qt::Uninitialized);

    const QByteArray passwordUtf8 = password.toUtf8();
    const int derived = PKCS5_PBKDF2_HMAC(
        passwordUtf8.constData(),
        passwordUtf8.size(),
        reinterpret_cast<const unsigned char *>(salt.constData()),
        salt.size(),
        iterations,
        EVP_sha512(),
        kDerivedKeyLength,
        reinterpret_cast<unsigned char *>(key.data())
    );

    if (derived != 1) {
        return {};
    }

    return key;
}

QByteArray randomBytes(int length) {
    QByteArray bytes(length, Qt::Uninitialized);
    if (RAND_bytes(reinterpret_cast<unsigned char *>(bytes.data()), length) != 1) {
        return {};
    }
    return bytes;
}

QByteArray hmacSha256(const QByteArray &key, const QByteArray &payload) {
    unsigned int outLength = 0;
    QByteArray digest(EVP_MAX_MD_SIZE, Qt::Uninitialized);

    const unsigned char *hmacValue = HMAC(
        EVP_sha256(),
        key.constData(),
        key.size(),
        reinterpret_cast<const unsigned char *>(payload.constData()),
        payload.size(),
        reinterpret_cast<unsigned char *>(digest.data()),
        &outLength
    );

    if (hmacValue == nullptr) {
        return {};
    }

    digest.truncate(static_cast<int>(outLength));
    return digest;
}

QByteArray aes128CbcEncrypt(const QByteArray &plaintext, const QByteArray &key, const QByteArray &iv) {
    if (key.size() != 16 || iv.size() != kIvLength) {
        return {};
    }

    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    if (ctx == nullptr) {
        return {};
    }

    QByteArray ciphertext(plaintext.size() + EVP_MAX_BLOCK_LENGTH, Qt::Uninitialized);
    int outLen1 = 0;
    int outLen2 = 0;

    const int initOk = EVP_EncryptInit_ex(
        ctx,
        EVP_aes_128_cbc(),
        nullptr,
        reinterpret_cast<const unsigned char *>(key.constData()),
        reinterpret_cast<const unsigned char *>(iv.constData())
    );
    const int updateOk = EVP_EncryptUpdate(
        ctx,
        reinterpret_cast<unsigned char *>(ciphertext.data()),
        &outLen1,
        reinterpret_cast<const unsigned char *>(plaintext.constData()),
        plaintext.size()
    );
    const int finalOk = EVP_EncryptFinal_ex(
        ctx,
        reinterpret_cast<unsigned char *>(ciphertext.data()) + outLen1,
        &outLen2
    );

    EVP_CIPHER_CTX_free(ctx);

    if (initOk != 1 || updateOk != 1 || finalOk != 1) {
        return {};
    }

    ciphertext.truncate(outLen1 + outLen2);
    return ciphertext;
}

QByteArray aes128CbcDecrypt(const QByteArray &ciphertext, const QByteArray &key, const QByteArray &iv, bool *ok) {
    if (ok != nullptr) {
        *ok = false;
    }

    if (key.size() != 16 || iv.size() != kIvLength) {
        return {};
    }

    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    if (ctx == nullptr) {
        return {};
    }

    QByteArray plaintext(ciphertext.size() + EVP_MAX_BLOCK_LENGTH, Qt::Uninitialized);
    int outLen1 = 0;
    int outLen2 = 0;

    const int initOk = EVP_DecryptInit_ex(
        ctx,
        EVP_aes_128_cbc(),
        nullptr,
        reinterpret_cast<const unsigned char *>(key.constData()),
        reinterpret_cast<const unsigned char *>(iv.constData())
    );
    const int updateOk = EVP_DecryptUpdate(
        ctx,
        reinterpret_cast<unsigned char *>(plaintext.data()),
        &outLen1,
        reinterpret_cast<const unsigned char *>(ciphertext.constData()),
        ciphertext.size()
    );
    const int finalOk = EVP_DecryptFinal_ex(
        ctx,
        reinterpret_cast<unsigned char *>(plaintext.data()) + outLen1,
        &outLen2
    );

    EVP_CIPHER_CTX_free(ctx);

    if (initOk != 1 || updateOk != 1 || finalOk != 1) {
        return {};
    }

    plaintext.truncate(outLen1 + outLen2);
    if (ok != nullptr) {
        *ok = true;
    }

    return plaintext;
}

QByteArray toBigEndian64(quint64 value) {
    QByteArray bytes(8, Qt::Uninitialized);
    for (int i = 7; i >= 0; --i) {
        bytes[7 - i] = static_cast<char>((value >> (i * 8)) & 0xFF);
    }
    return bytes;
}

quint64 fromBigEndian64(const QByteArray &bytes) {
    quint64 value = 0;
    for (int i = 0; i < bytes.size(); ++i) {
        value = (value << 8) | static_cast<unsigned char>(bytes[i]);
    }
    return value;
}

QByteArray fernetEncryptRaw(const QByteArray &message, const QByteArray &key32) {
    if (key32.size() != kDerivedKeyLength) {
        return {};
    }

    const QByteArray signingKey = key32.left(16);
    const QByteArray encryptionKey = key32.mid(16, 16);

    const QByteArray iv = randomBytes(kIvLength);
    if (iv.size() != kIvLength) {
        return {};
    }

    const QByteArray ciphertext = aes128CbcEncrypt(message, encryptionKey, iv);
    if (ciphertext.isEmpty()) {
        return {};
    }

    QByteArray payload;
    payload.reserve(1 + 8 + kIvLength + ciphertext.size());
    payload.append(static_cast<char>(kFernetVersion));
    payload.append(toBigEndian64(static_cast<quint64>(QDateTime::currentSecsSinceEpoch())));
    payload.append(iv);
    payload.append(ciphertext);

    const QByteArray digest = hmacSha256(signingKey, payload);
    if (digest.size() != kHmacLength) {
        return {};
    }

    return payload + digest;
}

bool fernetDecryptRaw(const QByteArray &tokenRaw, const QByteArray &key32, QByteArray *plaintextOut) {
    if (tokenRaw.size() < (1 + 8 + kIvLength + kHmacLength) || key32.size() != kDerivedKeyLength) {
        return false;
    }

    const unsigned char version = static_cast<unsigned char>(tokenRaw.at(0));
    if (version != kFernetVersion) {
        return false;
    }

    const QByteArray signingKey = key32.left(16);
    const QByteArray encryptionKey = key32.mid(16, 16);

    const int digestOffset = tokenRaw.size() - kHmacLength;
    const QByteArray payload = tokenRaw.left(digestOffset);
    const QByteArray providedDigest = tokenRaw.mid(digestOffset, kHmacLength);
    const QByteArray computedDigest = hmacSha256(signingKey, payload);

    if (computedDigest.size() != kHmacLength ||
        CRYPTO_memcmp(computedDigest.constData(), providedDigest.constData(), kHmacLength) != 0) {
        return false;
    }

    const QByteArray timestampBytes = tokenRaw.mid(1, 8);
    Q_UNUSED(fromBigEndian64(timestampBytes));

    const QByteArray iv = tokenRaw.mid(9, kIvLength);
    const QByteArray ciphertext = tokenRaw.mid(9 + kIvLength, digestOffset - (1 + 8 + kIvLength));

    bool ok = false;
    const QByteArray plaintext = aes128CbcDecrypt(ciphertext, encryptionKey, iv, &ok);
    if (!ok) {
        return false;
    }

    if (plaintextOut != nullptr) {
        *plaintextOut = plaintext;
    }

    return true;
}

} // namespace

namespace crypto {

QByteArray encryptWrapped(const QString &message, const QString &password, int iterations) {
    const QByteArray salt = randomBytes(kSaltLength);
    if (salt.size() != kSaltLength) {
        return {};
    }

    const QByteArray keyRaw = deriveKeyRaw(password, salt, iterations);
    if (keyRaw.size() != kDerivedKeyLength) {
        return {};
    }

    const QByteArray fernetRaw = fernetEncryptRaw(message.toUtf8(), keyRaw);
    if (fernetRaw.isEmpty()) {
        return {};
    }

    QByteArray wrapper;
    wrapper.reserve(kSaltLength + 4 + fernetRaw.size());
    wrapper.append(salt);

    for (int shift = 24; shift >= 0; shift -= 8) {
        wrapper.append(static_cast<char>((iterations >> shift) & 0xFF));
    }

    wrapper.append(fernetRaw);

    return base64UrlEncode(wrapper);
}

DecryptResult decryptWrapped(const QByteArray &token, const QString &password, const QString &errorIndicator) {
    bool decodedOk = false;
    const QByteArray decoded = base64UrlDecode(token, &decodedOk);

    if (!decodedOk || decoded.size() < (kSaltLength + 4 + 1 + 8 + kIvLength + kHmacLength)) {
        return {false, errorIndicator};
    }

    const QByteArray salt = decoded.left(kSaltLength);
    const QByteArray iterBytes = decoded.mid(kSaltLength, 4);
    const int iterations = (static_cast<unsigned char>(iterBytes[0]) << 24) |
                           (static_cast<unsigned char>(iterBytes[1]) << 16) |
                           (static_cast<unsigned char>(iterBytes[2]) << 8) |
                           static_cast<unsigned char>(iterBytes[3]);

    const QByteArray keyRaw = deriveKeyRaw(password, salt, iterations);
    if (keyRaw.size() != kDerivedKeyLength) {
        return {false, errorIndicator};
    }

    const QByteArray fernetRaw = decoded.mid(kSaltLength + 4);
    QByteArray plaintext;
    const bool ok = fernetDecryptRaw(fernetRaw, keyRaw, &plaintext);
    if (!ok) {
        return {false, errorIndicator};
    }

    return {true, QString::fromUtf8(plaintext)};
}

} // namespace crypto
