"""Безопасное обновление QComboBox без лишних сигналов."""


def reload_combo(combo, items, first_label=None, first_data=None, restore_data=...):
    """
    Перезаполняет комбобокс. items — список пар (label, userData).
    restore_data: значение userData для восстановления; ... = сохранить текущий выбор.
    """
    if restore_data is ...:
        restore_data = combo.currentData()

    combo.blockSignals(True)
    try:
        combo.clear()
        if first_label is not None:
            combo.addItem(first_label, first_data)
        for label, data in items:
            combo.addItem(label, data)
        if restore_data is not None and restore_data != '':
            idx = combo.findData(restore_data)
            if idx >= 0:
                combo.setCurrentIndex(idx)
    finally:
        combo.blockSignals(False)
