#include "main_window.h"

#include "path_utils.h"
#include "theme.h"

#include <QFont>
#include <QFrame>
#include <QGridLayout>
#include <QHBoxLayout>
#include <QIcon>
#include <QLabel>
#include <QPixmap>
#include <QPushButton>
#include <QSize>
#include <QVBoxLayout>
#include <QWidget>

namespace {

QPushButton *createActionButton(
    const QString &text,
    const QString &iconPath,
    const QColor &bgColor,
    const QColor &textColor,
    QWidget *parent
) {
    auto *button = new QPushButton(text, parent);
    button->setIcon(QIcon(resolveAssetPath(iconPath)));
    button->setIconSize(QSize(25, 25));

    QFont font("Impact", 18, QFont::Normal);
    button->setFont(font);
    button->setMinimumHeight(56);

    const QString style = QString(
        "QPushButton {"
        " background-color: %1;"
        " color: %2;"
        " border: none;"
        " border-radius: 8px;"
        " text-align: left;"
        " padding: 8px 12px;"
        "}"
        "QPushButton:hover {"
        " background-color: %3;"
        "}"
    )
                              .arg(bgColor.name(), textColor.name(), theme::darkenHex(bgColor));

    button->setStyleSheet(style);
    return button;
}

} // namespace

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent) {
    setupUi();
}

void MainWindow::setupUi() {
    setWindowTitle("Lock");
    setFixedSize(500, 425);

    auto *central = new QWidget(this);
    central->setStyleSheet(QString("background-color: %1;").arg(theme::nord0().name()));
    setCentralWidget(central);

    auto *rootLayout = new QVBoxLayout(central);
    rootLayout->setContentsMargins(0, 0, 0, 0);
    rootLayout->setSpacing(0);

    auto *header = new QWidget(central);
    auto *headerLayout = new QVBoxLayout(header);
    headerLayout->setContentsMargins(0, 0, 0, 0);

    auto *titleLabel = new QLabel(header);
    QPixmap titlePixmap(resolveAssetPath("assets/img/dark-title.png"));
    titleLabel->setPixmap(titlePixmap.scaled(196, 50, Qt::IgnoreAspectRatio, Qt::SmoothTransformation));
    titleLabel->setAlignment(Qt::AlignCenter);
    headerLayout->addWidget(titleLabel);
    headerLayout->setContentsMargins(0, 20, 0, 10);

    rootLayout->addWidget(header, 0);

    auto *buttonFrame = new QFrame(central);
    buttonFrame->setStyleSheet(QString("background-color: %1; border-radius: 8px;").arg(theme::nord1().name()));

    auto *frameHostLayout = new QVBoxLayout;
    frameHostLayout->setContentsMargins(10, 10, 10, 10);
    frameHostLayout->setSpacing(0);
    frameHostLayout->addWidget(buttonFrame);
    rootLayout->addLayout(frameHostLayout, 1);

    auto *grid = new QGridLayout(buttonFrame);
    grid->setContentsMargins(0, 0, 0, 0);
    grid->setHorizontalSpacing(10);
    grid->setVerticalSpacing(10);

    auto *createBtn = createActionButton("Create Password", "assets/icon/plus.png", theme::nord14(), theme::nord2(), buttonFrame);
    auto *updateBtn = createActionButton("Update Password", "assets/icon/arrow.png", theme::nord13(), theme::nord2(), buttonFrame);
    auto *deleteBtn = createActionButton("Delete Password", "assets/icon/bin.png", theme::nord11(), theme::nord2(), buttonFrame);
    auto *searchUrlBtn = createActionButton("by Url / Service", "assets/icon/url.png", theme::nord8(), theme::nord2(), buttonFrame);
    auto *searchUserBtn = createActionButton("by Email / User", "assets/icon/user.png", theme::nord4(), theme::nord2(), buttonFrame);
    auto *listBtn = createActionButton("List Passwords", "assets/icon/list.png", theme::nord15(), theme::nord2(), buttonFrame);

    grid->addWidget(createBtn, 0, 0);
    grid->addWidget(updateBtn, 0, 1);
    grid->addWidget(deleteBtn, 1, 0);
    grid->addWidget(searchUrlBtn, 1, 1);
    grid->addWidget(searchUserBtn, 2, 0);
    grid->addWidget(listBtn, 2, 1);

    for (int row = 0; row < 3; ++row) {
        grid->setRowStretch(row, 1);
    }
    for (int col = 0; col < 2; ++col) {
        grid->setColumnStretch(col, 1);
    }
}
