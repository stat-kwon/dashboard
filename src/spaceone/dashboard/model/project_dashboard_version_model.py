from mongoengine import *

from spaceone.core.model.mongo_model import MongoModel


class DateRange(EmbeddedDocument):
    enabled = BooleanField(default=False)


class Currency(EmbeddedDocument):
    enabled = BooleanField(default=False)
    value = StringField(default="")


class Settings(EmbeddedDocument):
    date_range = EmbeddedDocumentField(DateRange, default=DateRange)
    currency = EmbeddedDocumentField(Currency, default=Currency)


class ProjectDashboardVersion(MongoModel):
    project_dashboard_id = StringField(max_length=40)
    version = IntField()
    layouts = ListField(default=[])
    variables = DictField(default={})
    settings = EmbeddedDocumentField(Settings, default=Settings)
    variables_schema = DictField(default={})
    domain_id = StringField(max_length=40)
    created_at = DateTimeField(auto_now_add=True)

    meta = {
        'updatable_fields': [],
        'minimal_fields': [
            'project_dashboard_id',
            'version',
            'domain_id',
            'created_at',
        ],
        'ordering': ['-version'],
        'indexes': [
            'project_dashboard_id',
            'version',
            'domain_id',
            'created_at'
        ]
    }
