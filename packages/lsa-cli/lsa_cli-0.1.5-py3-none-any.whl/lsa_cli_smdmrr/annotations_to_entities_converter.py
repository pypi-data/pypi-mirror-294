from typing import Any

from .config import AnnotationType
from .models import Entity, EntityInstance, Property


class AnnotationsToEntitiesConverter:
    def __init__(self, annotations_markers_map: dict[AnnotationType, str]) -> None:
        self.annotations_markers_map: dict[AnnotationType, str] = annotations_markers_map
        self.entities: list[Entity] = []

    def _add_instance(self, name: str | None, instance: EntityInstance) -> None:
        entity = next((entity for entity in self.entities if entity.name == name), None)
        if entity:
            entity.instances.append(instance)
        else:
            self.entities.append(Entity(name=name, instances=[instance]))

    def _convert_annotations_to_entities(self, annotations: dict[Any, Any]) -> None:
        current_instance: EntityInstance | None = None
        current_property: Property | None = None
        current_entity_name: str | None = None
        for file_annotation in annotations.get("filesAnnotations", []):
            current_file_path = file_annotation.get("relativeFilePath", None)

            for annotation in file_annotation.get("annotations", []):
                annotation_name = annotation.get("name", None)
                annotation_value = annotation.get("value", None)

                if annotation_name == self.annotations_markers_map[AnnotationType.ENTITY]:
                    if current_instance:
                        self._add_instance(current_entity_name, current_instance)
                    current_entity_name = None
                    current_property = None

                elif annotation_name == self.annotations_markers_map[AnnotationType.PROPERTY]:
                    if current_instance and current_property:
                        current_instance.properties.append(
                            Property(
                                name=current_property.name,
                                description=current_property.description,
                            )
                        )
                    current_property = Property(name=None, description=None)

                elif annotation_name == self.annotations_markers_map[AnnotationType.IDENTIFIER]:
                    current_instance = EntityInstance(
                        from_file=current_file_path, identifier=annotation_value, description=None
                    )

                elif annotation_name == self.annotations_markers_map[AnnotationType.NAME]:
                    if current_instance:
                        if current_property:
                            current_property.name = annotation_value
                        else:
                            current_entity_name = annotation_value

                elif annotation_name == self.annotations_markers_map[AnnotationType.DESCRIPTION]:
                    if current_instance:
                        if current_property:
                            current_property.description = annotation_value
                        else:
                            current_instance.description = annotation_value

        if current_instance:
            self._add_instance(current_entity_name, current_instance)

    def convert(self, annotations: dict[Any, Any]) -> dict[Any, Any]:
        self._convert_annotations_to_entities(annotations)
        json_entities: dict[Any, Any] = {
            "entities": [
                {
                    "name": entity.name,
                    "instances": [
                        {
                            "from_file": instance.from_file,
                            "identifier": instance.identifier,
                            "description": instance.description,
                            "properties": [
                                {
                                    "name": property.name,
                                    "description": property.description,
                                }
                                for property in instance.properties
                            ],
                        }
                        for instance in entity.instances
                    ],
                }
                for entity in self.entities
            ]
        }
        self.entities = []
        return json_entities
