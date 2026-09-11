from marshmallow import Schema, fields, validate

class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1))
    description = fields.Str(allow_none=True)
    status = fields.Str(validate=validate.OneOf(["pending", "in_progress", "completed"]))
    priority = fields.Str(validate=validate.OneOf(["low", "medium", "high"]))
    due_date = fields.Date(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    user_id = fields.Int(dump_only=True)