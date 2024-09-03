from .fields import CodeField


class CodeFieldAdminMixin:
    class Media:
        css = {
            "all": ("django_sb_codefield/css/codefield_django_admin.css",),
        }

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if issubclass(db_field.__class__, CodeField):
            kwargs["widget"] = db_field.formfield().widget

        return super().formfield_for_dbfield(db_field, request, **kwargs)
