from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column
from sqlalchemy.types import TIMESTAMP

from sqlmodel import Field, SQLModel, text
from sqlmodel.main import Relationship

# Lines needed to avoid warning due to unset inherit_cache attribute
from sqlmodel.sql.expression import Select, SelectOfScalar

import koco_product_sqlmodel.dbmodels.models_enums as m_enum

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

# ViewDef = {}


class CCatalog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    supplier: str = Field(default=None, max_length=128)
    year: Optional[int] = None
    status: int = Field(
        default=m_enum.StatusEnum.in_work.value
    )  # general status of the data set 1: "in work", 2: "ready for review". 3: "released"
    user_id: int = Field(default=1, foreign_key="cuser.id")
    insdate: datetime = Field(
        sa_column=Column(
            TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
        )
    )
    upddate: datetime = Field(
        sa_column=Column(
            TIMESTAMP,
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        )
    )
    product_groups: List["CProductGroup"] = Relationship(back_populates="catalog")


class CUser(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None, min_length=4, max_length=128)
    first_name: Optional[str] = Field(default=None, max_length=128)
    last_name: Optional[str] = Field(default=None, max_length=128)
    email: Optional[str] = Field(default=None, max_length=256)
    password: Optional[bytes] = Field(default=None, max_length=32)
    role_id: int = Field(default=m_enum.CUserRoleIdEnum.reader.value)
    insdate: datetime = Field(
        sa_column=Column(
            TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
        )
    )
    upddate: datetime = Field(
        sa_column=Column(
            TIMESTAMP,
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        )
    )


class CUserRole(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    role: str = Field(default=None, min_length=4, max_length=64)
    description: Optional[str] = Field(default=None, max_length=1024)
    insdate: datetime = Field(
        sa_column=Column(
            TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
        )
    )
    upddate: datetime = Field(
        sa_column=Column(
            TIMESTAMP,
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        )
    )


class CProductGroup(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_group: str = Field(default=None, max_length=256)
    description: Optional[str] = Field(default=None, max_length=1024)
    image_url: Optional[str] = Field(default=None, max_length=1024)
    supplier_site_url: Optional[str] = Field(default=None, max_length=1024)
    catalog_id: Optional[int] = Field(default=None, foreign_key="ccatalog.id")
    status: int = Field(
        default=m_enum.StatusEnum.in_work.value
    )  # general status of the data set 1: "in work", 2: "ready for review". 3: "released"
    user_id: int = Field(default=1, foreign_key="cuser.id")
    order_priority: int = Field(default=0)
    upddate: datetime = Field(
        sa_column=Column(
            TIMESTAMP,
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        )
    )
    insdate: datetime = Field(
        sa_column=Column(
            TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
        )
    )
    catalog: Optional[CCatalog] = Relationship(back_populates="product_groups")
    families: List["CFamily"] = Relationship(back_populates="product_group")


class CFamily(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    family: str = Field(default=None, max_length=256)
    type: Optional[str] = Field(default=None, max_length=1024)
    description: Optional[str] = Field(default=None, max_length=1024)
    short_description: Optional[str] = Field(default=None, max_length=256)
    upddate: datetime = Field(
        sa_column=Column(
            TIMESTAMP,
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        )
    )
    insdate: datetime = Field(
        sa_column=Column(
            TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
        )
    )
    product_group_id: Optional[int] = Field(
        default=None, foreign_key="cproductgroup.id"
    )
    status: int = Field(
        default=m_enum.StatusEnum.in_work.value
    )  # general status of the data set 1: "in work", 2: "ready for review". 3: "released"
    user_id: int = Field(default=1, foreign_key="cuser.id")
    product_group: Optional[CProductGroup] = Relationship(back_populates="families")
    articles: List["CArticle"] = Relationship(back_populates="family")
    applications: List["CApplication"] = Relationship(back_populates="family")
    options: List["COption"] = Relationship(back_populates="family")


class CArticle(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    article: str = Field(default=None, max_length=256)
    description: Optional[str] = Field(default=None, max_length=4096)
    short_description: Optional[str] = Field(default=None, max_length=256)
    upddate: datetime = Field(
        sa_column=Column(
            TIMESTAMP,
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        )
    )
    insdate: datetime = Field(
        sa_column=Column(
            TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
        )
    )
    family_id: Optional[int] = Field(default=None, foreign_key="cfamily.id")
    status: int = Field(
        default=m_enum.StatusEnum.in_work.value
    )  # general status of the data set 1: "in work", 2: "ready for review". 3: "released"
    user_id: int = Field(default=1, foreign_key="cuser.id")
    family: Optional[CFamily] = Relationship(back_populates="articles")


class CApplication(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    application: Optional[str] = Field(default=None, max_length=256)
    family_id: Optional[int] = Field(default=None, foreign_key="cfamily.id")
    user_id: int = Field(default=1, foreign_key="cuser.id")
    upddate: datetime = Field(
        sa_column=Column(
            TIMESTAMP,
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        )
    )
    insdate: datetime = Field(
        sa_column=Column(
            TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
        )
    )
    family: Optional[CFamily] = Relationship(back_populates="applications")


class COption(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: Optional[str] = Field(
        default=m_enum.OptionFeatureEnum.feature.value, max_length=64
    )  # distinguish between 'Option' and 'Feature', use same table for storage
    option: Optional[str] = Field(default=None, max_length=256)
    category: Optional[str] = Field(default=None, max_length=256)
    user_id: int = Field(default=1, foreign_key="cuser.id")
    family_id: Optional[int] = Field(default=None, foreign_key="cfamily.id")
    upddate: datetime = Field(
        sa_column=Column(
            TIMESTAMP,
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        )
    )
    insdate: datetime = Field(
        sa_column=Column(
            TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
        )
    )
    family: Optional[CFamily] = Relationship(back_populates="options")


class CUrl(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: Optional[str] = Field(default=m_enum.CUrlTypeEnum.datasheet.value, max_length=64)
    supplier_url: Optional[str] = Field(default=None, max_length=1024)
    KOCO_url: Optional[str] = Field(default=None, max_length=1024)
    description: Optional[str] = Field(default=None, max_length=1024)
    parent_id: Optional[int] = Field(default=None)
    parent: Optional[str] = Field(
        default=m_enum.CUrlParentEnum.family.value, max_length=64
    )  # selector if table belongs to 'article', 'family', 'categorytree'
    user_id: int = Field(default=1, foreign_key="cuser.id")
    upddate: datetime = Field(
        sa_column=Column(
            TIMESTAMP,
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        )
    )
    insdate: datetime = Field(
        sa_column=Column(
            TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
        )
    )


class CSpecTable(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None, max_length=256)
    type: Optional[str] = Field(
        default=m_enum.SpectableTypeEnum.overview.value, max_length=64
    )  # selector if 'singlecol', 'multicol', 'overview'
    has_unit: Optional[bool] = None  # switch if unit col is needed or not
    parent: Optional[str] = Field(
        default=m_enum.SpectableParentEnum.family.value, max_length=64
    )  # selector if table belongs to 'article', 'family', 'product_group', or 'catalog'
    user_id: int = Field(default=1, foreign_key="cuser.id")
    upddate: datetime = Field(
        sa_column=Column(
            TIMESTAMP,
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        )
    )
    insdate: datetime = Field(
        sa_column=Column(
            TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
        )
    )
    parent_id: int = Field(default=None)
    spec_table_items: List["CSpecTableItem"] = Relationship(back_populates="spec_table")


class CSpecTableItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    pos: str = Field(default=None, max_length=32)
    name: str = Field(default=None, max_length=256)
    value: Optional[str] = Field(default=None, max_length=256)
    min_value: Optional[str] = Field(default=None, max_length=256)
    max_value: Optional[str] = Field(default=None, max_length=256)
    unit: Optional[str] = Field(default=None, max_length=256)
    user_id: int = Field(default=1, foreign_key="cuser.id")
    upddate: datetime = Field(
        sa_column=Column(
            TIMESTAMP,
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        )
    )
    insdate: datetime = Field(
        sa_column=Column(
            TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
        )
    )
    spec_table_id: int = Field(default=None, foreign_key="cspectable.id")
    spec_table: CSpecTable = Relationship(back_populates="spec_table_items")


class CBacklog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    backlog_text: str = Field(default=None, max_length=1024)
    status: int = Field(default=1)
    user_id: int = Field(default=1, foreign_key="cuser.id")
    upddate: datetime = Field(
        sa_column=Column(
            TIMESTAMP,
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        )
    )
    insdate: datetime = Field(
        sa_column=Column(
            TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
        )
    )


class CCategoryTree(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    category: str = Field(default=None, max_length=128)
    export_target: str = Field(default=None, max_length=16)
    description: str = Field(default=None, max_length=4096)
    parent_id: int = Field(default=None)
    pos: int = Field(default=1)
    user_id: int = Field(default=1, foreign_key="cuser.id")
    upddate: datetime = Field(
        sa_column=Column(
            TIMESTAMP,
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        )
    )
    insdate: datetime = Field(
        sa_column=Column(
            TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
        )
    )


class CCategoryMapper(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    category_id: Optional[int] = Field(default=None, foreign_key='ccategorytree.id')
    family_id: Optional[int] = Field(default=None, foreign_key='cfamily.id')
    user_id: int = Field(default=1, foreign_key="cuser.id")
    upddate: datetime = Field(
        sa_column=Column(
            TIMESTAMP,
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        )
    )
    insdate: datetime = Field(
        sa_column=Column(
            TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
        )
    )


def Main():
    pass


if __name__ == "__main__":
    Main()
