from typing import Any

from rest_framework import serializers


class BaseSerializer(serializers.Serializer[Any]):
    pass


class BaseInputSerializer(BaseSerializer):
    """
    Base serializer to provide common functionality to input serializers.
    Do not use this serializer directly - subclass it and define fields.
    """

    validated_data: dict[str, Any]

    def get_input_data(self) -> dict[str, Any]:
        """
        Return input data.
        Raises `rest_framework.exceptions.ValidationError` if input data is invalid format.
        """
        self.is_valid(raise_exception=True)
        return self.validated_data


class BaseOutputSerializer(BaseSerializer):
    """
    Base serializer to provide common functionality to output serializers.
    Do not use this serializer directly - subclass it and define fields.
    """

    @classmethod
    def get_output_data(cls, obj: Any) -> dict[str, Any]:
        """
        Serialize object into representation and return as output data.
        """
        return cls(obj).data


class BaseListOutputSerializer(BaseOutputSerializer):
    """
    Base list serializer to provide common functionality to list output serializers.
    Do not use this serializer directly - subclass it and define fields.
    """

    count = serializers.SerializerMethodField()

    def get_count(self, obj: Any) -> int:
        return len(obj.items)
