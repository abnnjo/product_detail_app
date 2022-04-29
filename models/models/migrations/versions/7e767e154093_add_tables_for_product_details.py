"""add tables for product details

Revision ID: 7e767e154093
Revises: 
Create Date: 2022-04-29 20:07:45.244360

"""
from alembic import op
import sqlalchemy as sa
import datetime

# revision identifiers, used by Alembic.
revision = '7e767e154093'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('brand',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('category',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('brand_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=f"{datetime.datetime.now()}", nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=f"{datetime.datetime.now()}", onupdate=f"{datetime.datetime.now()}", nullable=False),
    sa.ForeignKeyConstraint(['brand_id'], ['brand.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product')
    op.drop_table('category')
    op.drop_table('brand')
    # ### end Alembic commands ###