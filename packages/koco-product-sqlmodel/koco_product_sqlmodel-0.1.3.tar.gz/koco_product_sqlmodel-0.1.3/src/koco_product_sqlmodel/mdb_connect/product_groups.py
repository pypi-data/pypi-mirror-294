from koco_product_sqlmodel.mdb_connect.init_db_con import mdb_engine
from sqlmodel import Session, select
from koco_product_sqlmodel.dbmodels.definition import (
    CCatalog,
    CProductGroup,
)


def create_productgroup(product_group: CProductGroup) -> CProductGroup:
    if not product_group:
        return
    with Session(mdb_engine) as session:
        session.add(product_group)
        session.commit()
        statement = (
            select(CProductGroup)
            .where(CProductGroup.product_group == product_group.product_group)
            .where(CProductGroup.catalog_id == product_group.catalog_id)
        )
        pgn = session.exec(statement=statement).one_or_none()
        return pgn


def collect_product_groups(
    supplier: str = None, year: int = None, catalog_id: int = None, image_not_found_png: str ="/img/koco.png"
):
    with Session(mdb_engine) as session:
        if catalog_id:
            statement = (
                select(CProductGroup)
                .where(CProductGroup.catalog_id == catalog_id)
                .order_by(CProductGroup.id)
            )
            results = session.exec(statement).all()
            statement = select(CCatalog).where(CCatalog.id == catalog_id)
            cat = session.exec(statement).one_or_none()
            if cat:
                supplier = cat.supplier
        elif year:
            statement = (
                select(CProductGroup)
                .join(CCatalog, CCatalog.id == CProductGroup.catalog_id)
                .where(CCatalog.supplier == supplier)
                .where(CCatalog.year == year)
                .order_by(CProductGroup.id)
            )
            results = session.exec(statement).all()
        else:
            statement = (
                select(CCatalog).where(CCatalog.supplier == supplier).order_by(year)
            )
            cats = session.exec(statement).all()
            if cats:
                cat = cats[-1]
            else:
                return None, None
            statement = (
                select(CProductGroup)
                .where(CProductGroup.catalog_id == cat.id)
                .order_by(CProductGroup.id)
            )
            results = session.exec(statement).all()
        for r in results:
            if not r.image_url:
                r.image_url = image_not_found_png

    return results, supplier


def main()->None:
    pass

if __name__=="__main__":
    main()