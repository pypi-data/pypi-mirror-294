from koco_product_sqlmodel.mdb_connect.init_db_con import mdb_engine
from sqlmodel import Session, select
from koco_product_sqlmodel.dbmodels.definition import (
    COption,
)


def create_option(option: COption):
    with Session(mdb_engine) as session:
        session.add(option)
        session.commit()
        statement = (
            select(COption)
            .where(COption.option == option.option)
            .where(COption.family_id == option.family_id)
            .where(COption.category == option.category)
            .where(COption.type == option.type)
        )
    return session.exec(statement=statement).one_or_none()


def main()->None:
    pass

if __name__=="__main__":
    main()