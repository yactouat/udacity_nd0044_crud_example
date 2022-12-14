"""empty message

Revision ID: a98680b280ca
Revises: 
Create Date: 2022-10-16 09:10:02.956344

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a98680b280ca'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('TypeAList',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('options', sa.ARRAY(sa.String()), nullable=False),
    sa.Column('upcoming_items', sa.Integer(), nullable=True),
    sa.Column('past_items', sa.Integer(), nullable=True),
    sa.Column('past_items_count', sa.Integer(), nullable=True),
    sa.Column('upcoming_items_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('TypeBList',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('upcoming_items', sa.Integer(), nullable=True),
    sa.Column('past_items', sa.Integer(), nullable=True),
    sa.Column('past_items_count', sa.Integer(), nullable=True),
    sa.Column('upcoming_items_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Item',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('typealist_id', sa.Integer(), nullable=False),
    sa.Column('typeblist_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('typealist_name', sa.String(), nullable=True),
    sa.Column('typeblist_name', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['typealist_id'], ['TypeAList.id'], ),
    sa.ForeignKeyConstraint(['typeblist_id'], ['TypeBList.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('typealist_tybeblist',
    sa.Column('typealist_id', sa.Integer(), nullable=False),
    sa.Column('typeblist_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['typealist_id'], ['TypeAList.id'], ),
    sa.ForeignKeyConstraint(['typeblist_id'], ['TypeBList.id'], ),
    sa.PrimaryKeyConstraint('typealist_id', 'typeblist_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('typealist_tybeblist')
    op.drop_table('Item')
    op.drop_table('TypeBList')
    op.drop_table('TypeAList')
    # ### end Alembic commands ###
