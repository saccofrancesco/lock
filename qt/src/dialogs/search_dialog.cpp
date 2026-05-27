#include "dialogs/search_dialog.h"

#include "data/password_store.h"
#include "dialogs/search_form_widget.h"
#include "theme.h"

#include <QTabWidget>
#include <QVBoxLayout>
#include <QWidget>

SearchDialog::SearchDialog(
    PasswordStore &store,
    const QString &firstCriteria,
    const QString &secondCriteria,
    QWidget *parent
)
    : QDialog(parent) {
    setWindowTitle(QStringLiteral("Search Password"));
    setFixedSize(300, 475);
    setStyleSheet(QString("background-color: %1;").arg(theme::nord0().name()));

    auto *layout = new QVBoxLayout(this);
    layout->setContentsMargins(10, 0, 10, 10);

    auto *tabs = new QTabWidget(this);
    tabs->setStyleSheet(QString(
                            "QTabWidget::pane {"
                            " background-color: %1;"
                            " border: none;"
                            " border-radius: 8px;"
                            "}"
                            "QTabBar::tab {"
                            " background-color: %2;"
                            " color: %3;"
                            " border: none;"
                            " padding: 8px 10px;"
                            " border-top-left-radius: 6px;"
                            " border-top-right-radius: 6px;"
                            "}"
                            "QTabBar::tab:selected {"
                            " background-color: %4;"
                            "}"
                            "QTabBar::tab:!selected:hover {"
                            " background-color: %5;"
                            "}"
                        )
                            .arg(
                                theme::nord1().name(),
                                theme::nord2().name(),
                                theme::nord4().name(),
                                theme::nord10().name(),
                                theme::darkenHex(theme::nord2())
                            ));

    auto *firstTab = new QWidget(tabs);
    auto *firstLayout = new QVBoxLayout(firstTab);
    firstLayout->setContentsMargins(0, 0, 0, 0);
    firstLayout->addWidget(new SearchFormWidget(store, firstCriteria, this, firstTab));

    auto *secondTab = new QWidget(tabs);
    auto *secondLayout = new QVBoxLayout(secondTab);
    secondLayout->setContentsMargins(0, 0, 0, 0);
    secondLayout->addWidget(new SearchFormWidget(store, secondCriteria, this, secondTab));

    tabs->addTab(firstTab, firstCriteria.left(1).toUpper() + firstCriteria.mid(1));
    tabs->addTab(secondTab, secondCriteria.left(1).toUpper() + secondCriteria.mid(1));

    layout->addWidget(tabs);
}
