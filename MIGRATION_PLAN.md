# CustomTkinter -> Qt/C++ Migration Plan

## 1. Current Migration Status
- Date: 2026-05-27
- Branch: `main`
- Status: `in_progress`
- Phase: `core Qt migration implemented / final parity validation pending`
- Confidence: `high` for UI/logic parity scope, `high` for encryption compatibility (validated against Python implementation)

## 2. Completed Steps
- Inspected project structure and source modules.
- Mapped main UI shell, action grid, dialogs, and DB/encryption flow.
- Identified assets and sizing behavior used by the Python UI.
- Captured migration strategy and checkpoints in this file.
- Validated local toolchain availability for Qt build start.
- Created Qt project scaffold under `qt/`:
  - `CMakeLists.txt`
  - app entry point (`src/main.cpp`)
  - main window shell (`include/main_window.h`, `src/main_window.cpp`)
  - theme constants/utilities (`include/theme.h`, `src/theme.cpp`)
  - asset path resolver (`include/path_utils.h`, `src/path_utils.cpp`)
- Implemented reusable widgets and styles:
  - `PasswordField` with show/hide toggle and eye icons
  - shared entry/button styling helpers
- Recreated initial main window visual shell:
  - fixed `500x425` window
  - Nord background/frame
  - header title image sizing (`196x50`) and spacing
  - 3x2 action button grid with mapped colors/icons/text
- Implemented all dialogs and interaction flow:
  - Create Password (`300x350`)
  - Update Password (`300x350`)
  - Delete Password (`300x350`)
  - Search Password with tabbed criteria (`300x475`)
  - List Passwords (`300x400`)
  - single-instance dialog behavior per main action button (focus existing window)
- Implemented data/security port:
  - `PasswordStore` with SQLite CRUD/search/list using Qt SQL
  - C++ crypto port with OpenSSL:
    - PBKDF2-HMAC-SHA512 key derivation
    - Fernet-compatible AES/HMAC token handling
    - Python-compatible wrapped payload format (`salt + iterations + raw_fernet`, base64url)
- Verified build and runtime smoke tests:
  - `cmake -S qt -B qt/build`
  - `cmake --build qt/build -j`
- Verified Python/C++ crypto compatibility both directions:
  - Python `encrypt` -> Qt `decrypt` passed
  - Qt `encrypt` -> Python `decrypt` passed
- Added Qt build/run docs in `qt/README.md`.

## 3. Pending Steps
- Run manual UX parity pass against Python app for pixel-level spacing/typography differences.
- Validate build/run on Windows and Linux toolchains.
- Decide whether to keep `lock_qt_crypto_probe` target long-term or move it to a dedicated test harness.
- Optional: package/distribution setup for cross-platform releases.

## 4. Discovered Project Structure
- Entry point: `main.py`
- Main app shell:
  - `components/app.py` (`App` root window)
  - `components/header.py` (title image)
  - `components/buttonframe.py` (3x2 grid)
  - `components/buttons.py` (6 action buttons opening top-level windows)
- Dialogs/forms:
  - `components/toplevels.py`
  - `components/searchform.py`
  - `components/passwordentry.py`
  - `components/customentry.py`
  - `components/cancelbutton.py`
- Data/security:
  - `database/database.py` (SQLite CRUD + search/list)
  - `database/encryptor.py` (PBKDF2-HMAC-SHA512 derived key + Fernet encryption wrapper)
- Theme/fonts/assets:
  - `colors/colors.py` (Nord palette + darken helper)
  - `font/font.py` (`Impact` font helper)
  - `assets/icon/*.png`, `assets/img/dark-title.png`

## 5. UI Components Mapping (CustomTkinter -> Qt Widgets)
- `CTk` main window -> `QMainWindow` with central `QWidget`
- `CTkFrame` -> `QWidget` with layouts (`QVBoxLayout`, `QGridLayout`, `QHBoxLayout`)
- `CTkLabel` (image/text) -> `QLabel` (`QPixmap`)
- `CTkButton` -> `QPushButton`
- `CTkEntry` -> `QLineEdit`
- `PasswordEntry` composite -> custom `QWidget` containing `QLineEdit` + eye-toggle `QPushButton`
- `CTkToplevel` -> `QDialog` (non-resizable, fixed size)
- `CTkTabview` -> `QTabWidget`
- `CTkScrollableFrame` -> `QScrollArea` + content widget/label
- `StringVar` dynamic text -> direct `QLabel::setText`

## 6. Functionality Mapping (Python -> C++)
- `create_password` -> insert encrypted password row into SQLite.
- `update_password` -> locate row by `(email, username, url, service)`, decrypt-check via master, then update encrypted password.
- `delete_password` -> locate row by `(email, username, url, service)`, decrypt-check via master, then delete row.
- `search_password` -> query by criteria (`email|username|url|service`), decrypt each result with provided master.
- `list_passwords` -> fetch all rows, decrypt each password with provided master.
- Password encryption target behavior:
  - random 16-byte salt
  - PBKDF2-HMAC-SHA512, default iterations 100000, key length 32
  - Fernet-compatible token usage and Python-like payload envelope

## 7. Build-System Decisions
- Use CMake (>=3.21) and Qt6 Widgets/Sql.
- Use OpenSSL for cryptographic primitives (PBKDF2, AES/HMAC needed for Fernet-compatible behavior).
- Keep assets in existing `assets/` path and resolve relative to executable working directory (with app-dir fallback).
- Ignore local CMake artifacts via `.gitignore` (`qt/build/`).
- Target platforms: macOS, Linux, Windows.

## 8. Issues Encountered
- Resolved: toolchain blocker from previous checkpoint (CMake + Qt now available).
- Non-blocking: first build attempt failed due parallel configure/build race; resolved by rebuilding after configure completed.
- Non-blocking: initial `MainWindow` header used `Q_OBJECT` without required meta-object use; removed to fix linker vtable error.
- Non-blocking: missing `QDir` include during DB layer port caused compile failure; fixed.
- Known source quirks to preserve or consciously normalize:
  - Several key bindings in Python attach to wrapper widgets instead of internal entry (`PasswordEntry`); Qt port will bind directly to text-change signals for reliable behavior while preserving user-visible behavior.
  - Python `decrypt` catches `InvalidSignature` only; Qt port treats crypto/auth/decode failures as decryption failure without crashing (same intended UX, safer failure behavior).

## 9. Required User Actions
- None currently.

## 10. Resume Point
- Safe resume checkpoint: **after full core Qt feature migration + successful build + crypto compatibility verification**.
- Next concrete step: run cross-platform and UX parity validation pass, then finalize migration handoff.
