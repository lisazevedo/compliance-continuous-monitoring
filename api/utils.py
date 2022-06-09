# -*- coding: utf-8 -*-
"""Utility functions."""

from datetime import datetime, timezone
import sqlalchemy as sa
import uuid
import random

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

def uuid_alpha():
    """
    Generates an uuid that always starts with an alpha char.

    Returns
    -------
    str
    """
    uuid_ = str(uuid.uuid4())
    if not uuid_[0].isalpha():
        c = random.choice(["a", "b", "c", "d", "e", "f"])
        uuid_ = f"{c}{uuid_[1:]}"
    return uuid_
