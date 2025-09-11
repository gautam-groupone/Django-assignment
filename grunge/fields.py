from typing import Any
from rest_framework import serializers


class UUIDHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("source", "*")
        kwargs.setdefault("lookup_field", "uuid")
        kwargs.setdefault("lookup_url_kwarg", "uuid")
        super().__init__(*args, **kwargs)


class UUIDHyperlinkedRelatedField(serializers.HyperlinkedRelatedField):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("lookup_field", "uuid")
        kwargs.setdefault("lookup_url_kwarg", "uuid")
        super().__init__(*args, **kwargs)
