from marshmallow import Schema, fields, validates, ValidationError

class SecuritySchema(Schema):
    code = fields.Str(required=True)
    symbol = fields.Str(required=True)
    exchange = fields.Str(required=True)
    type = fields.Str(required=True)
    name = fields.Str(required=True)
    full_name = fields.Str()

    @validates("symbol")
    def validate_symbol(self, value):
        if not value.isalnum():
            raise ValidationError("symbol must be alphanumeric")
