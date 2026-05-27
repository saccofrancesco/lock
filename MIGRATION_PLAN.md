# CustomTkinter -> Qt/C++ Migration Plan

## 1. Current Migration Status
- Date: 2026-05-27
- Branch: `main`
- Status: `in_progress`
- Phase: `Qt scaffold complete / UI migration in progress`
- Confidence: `high` for UI/logic parity scope, `medium` for encryption compatibility until verified with test vectors

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
- Recreated initial main window visual shell:
  - fixed `500x425` window
  - Nord background/frame
  - header title image sizing (`196x50`) and spacing
  - 3x2 action button grid with mapped colors/icons/text
- Verified scaffold build succeeds:
  - `cmake -S qt -B qt/build`
  - `cmake --build qt/build -j`

## 3. Pending Steps
- Recreate reusable widgets (password entry with show/hide, custom line edit styling).
- Recreate dialogs:
  - Create Password
  - Update Password
  - Delete Password
  - Search Password (tabbed URL/service and email/username)
  - List Passwords
- Port database layer to Qt SQL (`QSqlDatabase` + SQLite).
- Port encryption/decryption logic to C++ with compatibility for existing Python-generated tokens.
- Wire all signal/slot behavior and button enable/disable logic.
- Style match (Nord palette, spacing, fonts, icon sizing, fixed window sizes).
- Build/test on current machine and document cross-platform build instructions.

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
- `PasswordEntry` composite -> custom `QWidget` containing `QLineEdit` + eye-toggle `QToolButton`
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
- Target platforms: macOS, Linux, Windows.

## 8. Issues Encountered
- Resolved: toolchain blocker from previous checkpoint (CMake + Qt now available).
- Non-blocking: first build attempt failed due parallel configure/build race; resolved by rebuilding after configure completed.
- Non-blocking: initial `MainWindow` header used `Q_OBJECT` without required meta-object use; removed to fix linker vtable error.
- Known source quirks to preserve or consciously normalize:
  - Several key bindings in Python attach to wrapper widgets instead of internal entry (`PasswordEntry`); Qt port will bind directly to text-change signals for reliable behavior while preserving user-visible behavior.
  - Python `decrypt` catches `InvalidSignature` only; Qt port will treat any crypto/auth/decode failure as decryption failure (same effective user-facing outcome).

## 9. Required User Actions
- None currently.

## 10. Resume Point
- Safe resume checkpoint: **after Qt scaffold + main window shell build pass**.
- Next concrete step: implement reusable entry widgets and migrate dialogs with real signal/slot logic.
