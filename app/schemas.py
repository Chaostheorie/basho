from voluptuous import (
    Schema,
    Required,
    REMOVE_EXTRA,
    Optional,
    All,
    Invalid,
    Length,
    MultipleInvalid,
)
from re import fullmatch


class WrappedSchema(Schema):
    def __call__(self, data) -> bool:
        """Validate data against this schema."""
        try:
            return self._compiled([], data)
        except MultipleInvalid:
            return False
        except Invalid as e:
            return False
            # return self.validate([], self.schema, data)
        finally:
            return True


def is_url(url: str) -> bool:
    if fullmatch(
        "https:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\/[-a-zA-Z0-9()@:%_\+.~#?]*",
        url,
    ):
        return True
    else:
        raise Invalid("Invalid Url supplied")


UserRegisterSchema = WrappedSchema(
    {
        Optional("username"): str,
        Required("id"): int,
        Optional("avatar_url"): All(str, Length(max=256), is_url),
    },
    extra=REMOVE_EXTRA,
)
