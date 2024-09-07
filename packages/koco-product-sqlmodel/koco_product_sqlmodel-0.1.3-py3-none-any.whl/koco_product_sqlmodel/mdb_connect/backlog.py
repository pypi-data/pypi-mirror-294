from koco_product_sqlmodel.mdb_connect.init_db_con import mdb_engine
from sqlmodel import Session, select, desc, SQLModel
from koco_product_sqlmodel.dbmodels.definition import (
    CBacklog,
)
from datetime import datetime as DT


def collect_backlog_data(id: int = None, backlog_text: str = None, status: int = None):
    qd = None
    with Session(mdb_engine) as session:
        if id:
            statement = select(CBacklog).where(CBacklog.id == id)
        else:
            if backlog_text and not status:
                statement = select(CBacklog).filter(
                    CBacklog.backlog_text.like("%" + backlog_text.lower() + "%")
                )
            elif backlog_text and status:
                statement = (
                    select(CBacklog)
                    .filter(
                        CBacklog.backlog_text.like("%" + backlog_text.lower() + "%")
                    )
                    .where(CBacklog.status == status)
                )
            elif not backlog_text and status:
                statement = select(CBacklog).where(CBacklog.status == status)
            else:
                statement = select(CBacklog).order_by(CBacklog.status)
        results = session.exec(statement)
        if not results:
            return None, None, None, None
        for ix, res in enumerate(results.all()):
            if ix == 0:
                if id or backlog_text or status:
                    id = res.id
                    backlog_text = res.backlog_text
                    status = res.status
                qd = {"heading": "Backlog data", "query_data": []}
                qd["table_headers"] = [CBacklog.__table__.c.keys()]
                qd["hrefs"] = ["" for th in qd["table_headers"][0]]
            qd["hrefs"][0] = "/backlog_edit" + f"?id="
            line = [res.dict()[th] for th in qd["table_headers"][0]]
            qd["query_data"].append(line)
    return id, backlog_text, status, qd


def add_backlog_data(backlog_text: str = None, status: int = None):
    if not status and not backlog_text:
        return
    with Session(mdb_engine) as session:
        if status not in (1, 2, 3):
            # print(status)
            status = 1
        bli = CBacklog(backlog_text=backlog_text, status=status, insdate=DT.now())
        session.add(bli)
        SQLModel.metadata.create_all(mdb_engine)
        session.commit()
        statement = select(CBacklog.id).order_by(desc(CBacklog.id))
        id = session.exec(statement).first()
    return id


def save_backlog_data(id: int = None, backlog_text: str = None, status: int = None):
    if not id:
        return
    with Session(mdb_engine) as session:
        if status not in (1, 2, 3):
            # print(status)
            status = 1
        statement = select(CBacklog).where(CBacklog.id == id)
        results = session.exec(statement)
        if not results:
            return
        bli = results.first()
        bli.status = status
        bli.upddate = DT.now()
        bli.backlog_text = backlog_text
        session.add(bli)
        SQLModel.metadata.create_all(mdb_engine)
        session.commit()
    return id


def delete_backlog_data(self, id: int = None):
    if not id:
        return
    with Session(mdb_engine) as session:
        statement = select(CBacklog).where(CBacklog.id == id)
        results = session.exec(statement)
        if not results:
            return
        bli = results.first()
        session.delete(bli)
        SQLModel.metadata.create_all(mdb_engine)
        session.commit()

def main()->None:
    pass

if __name__=="__main__":
    main()