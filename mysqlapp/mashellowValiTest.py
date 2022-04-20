from marshmallow import Schema, fields, validates_schema, ValidationError


class NumberSchema(Schema):
    field_a = fields.Integer()
    field_b = fields.Integer()
    field_c = fields.Integer()
    field_d = fields.Integer()

    @validates_schema
    def validate_lower_bound(self, data, **kwargs):
        errors = {}
        if data["field_b"] <= data["field_a"]:
            errors["field_b"] = ["field_b must be greater than field_a"]
        if data["field_c"] <= data["field_a"]:
            errors["field_c"] = ["field_c must be greater than field_a"]
        if errors:
            raise ValidationError(errors)

    @validates_schema
    def validate_upper_bound(self, data, **kwargs):
        errors = {}
        if data["field_b"] >= data["field_d"]:
            errors["field_b"] = ["field_b must be lower than field_d"]
        if data["field_c"] >= data["field_d"]:
            errors["field_c"] = ["field_c must be lower than field_d"]
        if errors:
            raise ValidationError(errors)


schema = NumberSchema()
try:
    schema.load({"field_a": 3, "field_b": 2, "field_c": 1, "field_d": 0})
except ValidationError as err:
    err.messages

schema.load({"field_a": 3, "field_b": 2, "field_c": 1, "field_d": 0})
print("##################################")