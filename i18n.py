import json
import os
from PySide6.QtCore import QObject, Signal


class Translator(QObject):
    language_changed = Signal()

    def __init__(self):
        super().__init__()
        self._strings: dict = {}
        self._lang = "vi"

    def load(self, lang: str):
        path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "translations",
            f"{lang}.json",
        )
        with open(path, "r", encoding="utf-8") as f:
            self._strings = json.load(f)
        self._lang = lang
        self.language_changed.emit()

    def t(self, key: str) -> str:
        return self._strings.get(key, key)

    @property
    def lang(self) -> str:
        return self._lang


_translator: "Translator | None" = None


def get_translator() -> Translator:
    global _translator
    if _translator is None:
        _translator = Translator()
    return _translator


def t(key: str) -> str:
    return get_translator().t(key)
