from codemirror2.widgets import CodeMirrorEditor
from django.db import models
from django.utils.translation import gettext_lazy as _

CodemirrorDefaultOptions = {
    "theme": "monokai",
    "lineNumbers": True,
}


class CodeField(models.TextField):
    description = _("Code")

    def __init__(self, *args, **kwargs):
        self.options = CodemirrorDefaultOptions.copy()
        self.options.update(kwargs.pop("options", {}))

        self.modes = kwargs.pop("modes", None)

        super().__init__(*args, **kwargs)

    def _get_code_mirror_editor_kwargs(self):
        code_mirror_editor_kwargs = {"options": self.options}

        if self.modes:
            code_mirror_editor_kwargs.update({"modes": self.modes})

        return code_mirror_editor_kwargs

    def formfield(self, **kwargs):
        # Passing max_length to forms.CharField means that the value's length
        # will be validated twice. This is considered acceptable since we want
        # the value in the form field (to pass into widget for example).
        defaults = {
            "max_length": self.max_length,
        }

        code_mirror_editor_kwargs = self._get_code_mirror_editor_kwargs()

        if not self.choices:
            defaults["widget"] = CodeMirrorEditor(**code_mirror_editor_kwargs)

        defaults.update(kwargs)

        return super().formfield(**defaults)
