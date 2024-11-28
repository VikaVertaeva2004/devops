"""initial migration

Revision ID: 477d9be39c8e
Revises: 
Create Date: 2024-11-28 22:39:00.621776

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '477d9be39c8e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('member',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=True),
    sa.Column('home_phone', sa.String(length=20), nullable=True),
    sa.Column('work_phone', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=300), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('commission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('chairperson_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['chairperson_id'], ['member.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('commission_membership',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('member_id', sa.Integer(), nullable=False),
    sa.Column('commission_id', sa.Integer(), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['commission_id'], ['commission.id'], ),
    sa.ForeignKeyConstraint(['member_id'], ['member.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('meeting',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('commission_id', sa.Integer(), nullable=False),
    sa.Column('datetime', sa.DateTime(), nullable=False),
    sa.Column('location', sa.String(length=255), nullable=True),
    sa.Column('attendees', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['commission_id'], ['commission.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('meeting')
    op.drop_table('commission_membership')
    op.drop_table('commission')
    op.drop_table('post')
    op.drop_table('member')
    # ### end Alembic commands ###
