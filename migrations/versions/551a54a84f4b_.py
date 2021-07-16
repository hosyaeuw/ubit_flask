"""empty message

Revision ID: 551a54a84f4b
Revises: 
Create Date: 2021-06-13 10:46:28.711867

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '551a54a84f4b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('trainer_office',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_trainer_office_id'), 'trainer_office', ['id'], unique=True)
    op.drop_index('ix_trainers_office_id', table_name='trainers_office')
    op.drop_table('trainers_office')
    op.add_column('trainers', sa.Column('office_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'trainers', 'trainer_office', ['office_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'trainers', type_='foreignkey')
    op.drop_column('trainers', 'office_id')
    op.create_table('trainers_office',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='trainers_office_pkey')
    )
    op.create_index('ix_trainers_office_id', 'trainers_office', ['id'], unique=True)
    op.drop_index(op.f('ix_trainer_office_id'), table_name='trainer_office')
    op.drop_table('trainer_office')
    # ### end Alembic commands ###