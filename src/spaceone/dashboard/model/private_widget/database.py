from mongoengine import *

from spaceone.core.model.mongo_model import MongoModel


class PrivateWidget(MongoModel):
    widget_id = StringField(
        max_length=40, generate_id="private-widget", unique=True
    )
    name = StringField(max_length=100)
    description = StringField(default=None)
    widget_type = StringField(max_length=40, default="NONE")
    options = DictField(default=None, null=True)
    tags = DictField(default={})
    dashboard_id = StringField(max_length=40)
    user_id = StringField(max_length=40)
    domain_id = StringField(max_length=40)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    meta = {
        "updatable_fields": [
            "name",
            "description",
            "widget_type",
            "options",
            "tags",
        ],
        "minimal_fields": [
            "widget_id",
            "name",
            "widget_type",
            "dashboard_id",
            "user_id",
            "domain_id",
        ],
        "ordering": ["name"],
        "indexes": [
            "name",
            "widget_type",
            "dashboard_id",
            "user_id",
            "domain_id",
        ],
    }
