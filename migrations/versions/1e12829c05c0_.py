"""empty message

Revision ID: 1e12829c05c0
Revises: 
Create Date: 2023-08-24 20:21:28.623359

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e12829c05c0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cliente',
    sa.Column('id_cliente', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=150), nullable=True),
    sa.Column('apellido', sa.String(length=150), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('nombre_usuario', sa.String(length=60), nullable=True),
    sa.Column('contraseña', sa.String(length=25), nullable=True),
    sa.Column('telefono', sa.String(length=25), nullable=True),
    sa.Column('usuario_telegram', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id_cliente')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cliente')
    # ### end Alembic commands ###
