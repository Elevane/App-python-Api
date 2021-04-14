"""empty message

Revision ID: a07114d13b26
Revises: e241a8210e7e
Create Date: 2021-04-11 02:07:24.166599

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a07114d13b26'
down_revision = 'e241a8210e7e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movie', sa.Column('director_id', sa.Integer(), nullable=True))
    op.add_column('movie', sa.Column('rating', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'movie', 'genre', ['director_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'movie', type_='foreignkey')
    op.drop_column('movie', 'rating')
    op.drop_column('movie', 'director_id')
    # ### end Alembic commands ###