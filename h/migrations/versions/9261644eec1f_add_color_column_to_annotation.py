# -*- coding: utf-8 -*-
"""Add the color column to the annotation table"""
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

from alembic import op
import sqlalchemy as sa


revision = "9261644eec1f"
down_revision = "8bd83598ad77"


def upgrade():
    op.add_column("annotation", sa.Column("color", sa.UnicodeText))


def downgrade():
    op.drop_column("annotation", "color")
