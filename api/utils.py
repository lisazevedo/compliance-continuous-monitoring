# -*- coding: utf-8 -*-
"""Utility functions."""

from datetime import datetime, timezone
import sqlalchemy as sa

class TimeStamp(sa.types.TypeDecorator):
    impl = sa.types.DateTime

    def process_bind_param(self, value: datetime, dialect):
        if value.tzinfo is None:
            value = value.astimezone(timezone.utc)

        return value.astimezone(timezone.utc)

    def process_result_value(self, value, dialect):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)

        return value.astimezone(timezone.utc)
        
def now():
    return datetime.utcnow().replace(tzinfo=timezone.utc)
