"""ORM 模型注册入口：保证 Base.metadata 包含所有表。

导入本模块会顺带注册 Post / Comment / Reaction 三个 mapper，
供 create_all 与 alembic autogenerate 使用。
"""
from app.models.post import Post  # noqa: F401
from app.models.comment import Comment  # noqa: F401
from app.models.reaction import Reaction  # noqa: F401