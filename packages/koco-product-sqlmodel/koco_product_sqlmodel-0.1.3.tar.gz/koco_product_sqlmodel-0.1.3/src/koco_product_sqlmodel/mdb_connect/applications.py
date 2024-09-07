from koco_product_sqlmodel.mdb_connect.init_db_con import mdb_engine
from sqlmodel import Session, select
from koco_product_sqlmodel.dbmodels.definition import (
    CApplication,
)


def create_application(application: CApplication):
    with Session(mdb_engine) as session:
        session.add(application)
        session.commit()
        statement = (
            select(CApplication)
            .where(CApplication.application == application.application)
            .where(
                CApplication.family_id == application.family_id,
            )
        )
    return session.exec(statement=statement).one_or_none()


def main()->None:
    pass

if __name__=="__main__":
    main()