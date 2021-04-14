"""empty message

Revision ID: e241a8210e7e
Revises: 631ea7ea9ffc
Create Date: 2021-04-11 01:59:34.954384

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e241a8210e7e'
down_revision = '631ea7ea9ffc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('genre',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('cinematheque_genre')
    op.add_column('movie', sa.Column('genre_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'movie', 'genre', ['genre_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'movie', type_='foreignkey')
    op.drop_column('movie', 'genre_id')
    op.create_table('cinematheque_genre',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('movie_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.id'], name='cinematheque_genre_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    op.drop_table('genre')
    # ### end Alembic commands ###