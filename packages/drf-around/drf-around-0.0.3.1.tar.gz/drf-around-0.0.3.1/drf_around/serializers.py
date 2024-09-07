from rest_framework.serializers import ModelSerializer


class AnnotationsAsFieldsMixin(ModelSerializer):
    queryset = None

    def get_fields(self):
        fields = super().get_fields()
        for name, annotation in self.get_annotations().items():
            fields[name] = self.create_field(annotation)
        return fields

    def create_field(self, annotation):
        serializer_class = self.serializer_field_mapping[
            annotation.output_field.__class__
        ]
        return serializer_class(required=False, read_only=True)

    def get_queryset(self):
        return self.queryset or self.Meta.model._default_manager.all()

    def get_annotations(self):
        if not hasattr(self, "annotations"):
            self.annotations = self.get_queryset()._query.annotations
        return self.annotations

    def create(self, validated_data):
        pk = super().create(validated_data).pk
        self.instance = self.get_queryset().get(pk=pk)
        return self.instance
