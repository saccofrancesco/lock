# Lock Qt/C++ Port

## Requirements
- CMake 3.21+
- Qt 6 (Widgets, Sql)
- OpenSSL (Crypto)
- C++17 compiler

## Build
```bash
cmake -S qt -B qt/build
cmake --build qt/build -j
```

## Run
```bash
./qt/build/lock_qt
```

## Optional Crypto Compatibility Probe
This helper verifies Python/C++ token compatibility:
```bash
./qt/build/lock_qt_crypto_probe encrypt <master> <plaintext>
./qt/build/lock_qt_crypto_probe decrypt <master> <token>
```

## Notes
- The app stores data in `database/.database.db` to stay compatible with the Python app.
- Assets are loaded from `assets/` using runtime path resolution fallback.
