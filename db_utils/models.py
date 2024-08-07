from datetime import datetime
import pytz

from sqlalchemy import text
from sqlmodel import SQLModel
from sqlmodel import Field



def utc8_datetime():
    return datetime.now(pytz.timezone("Asia/Shanghai"))


class TableName(SQLModel, table=True):
    __tablename__: str = "your_table_name" # type: ignore

    obj_token: str = Field(primary_key=True, max_length=255)
    name: str | None = Field(nullable=True, default=None, max_length=255)
    revision_id: int = Field(nullable=False, default=1)
    trashed: bool = Field(nullable=False, default=False)

    created_at: datetime = Field(
        default=None,
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
        },
    )
    updated_at: datetime = Field(
        default=None,
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
            "onupdate": text("CURRENT_TIMESTAMP"),
        },
    )