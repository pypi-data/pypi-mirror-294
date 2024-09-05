from amsdal_models.enums import BaseClasses
from amsdal_models.schemas.data_models.schema import ObjectSchema
from amsdal_models.schemas.manager import SchemaManagerHandler
from amsdal_utils.models.enums import SchemaTypes
from amsdal_utils.utils.singleton import Singleton

from amsdal.configs.main import settings


class SchemaManager(metaclass=Singleton):
    def __init__(self) -> None:
        self._schema_manager_handler = SchemaManagerHandler(settings.schemas_root_path)

    def invalidate_user_schemas(self) -> None:
        self._schema_manager_handler.invalidate_user_schemas()

    def class_schemas(self) -> list[tuple[ObjectSchema, SchemaTypes]]:
        return (
            [
                (type_schema, SchemaTypes.TYPE)
                for type_schema in self._schema_manager_handler.type_schemas
                if type_schema.title == BaseClasses.OBJECT
            ]
            + [
                (core_schema, SchemaTypes.CORE)
                for core_schema in sorted(self._schema_manager_handler.core_schemas, key=self._sort_key_for_schema)
            ]
            + [(user_schema, SchemaTypes.USER) for user_schema in self._schema_manager_handler.user_schemas]
            + [(contrib_schema, SchemaTypes.CONTRIB) for contrib_schema in self._schema_manager_handler.contrib_schemas]
        )

    @staticmethod
    def _sort_key_for_schema(schema: ObjectSchema) -> int:
        # We need to register ClassObject first, coz ClassObjectMeta has a reference to it.
        # All other classes have reference to ClassObject
        if schema.title == BaseClasses.CLASS_OBJECT:
            return 0
        elif schema.title == BaseClasses.CLASS_OBJECT_META:
            return 1
        else:
            return 2

    def get_schema_by_name(self, title: str, schema_type: SchemaTypes | None = None) -> ObjectSchema | None:
        _schemas = self.get_schemas(schema_type)

        for schema in _schemas:
            if schema.title == title:
                return schema

        return None

    def get_schemas(self, schema_type: SchemaTypes | None = None) -> list[ObjectSchema]:
        if schema_type == SchemaTypes.CONTRIB:
            return self._schema_manager_handler.contrib_schemas

        if schema_type == SchemaTypes.CORE:
            return self._schema_manager_handler.core_schemas

        if schema_type == SchemaTypes.TYPE:
            return self._schema_manager_handler.type_schemas

        if schema_type == SchemaTypes.USER:
            return self._schema_manager_handler.user_schemas

        return self._schema_manager_handler.all_schemas
