from koco_product_sqlmodel.mdb_connect.init_db_con import mdb_engine
from sqlmodel import SQLModel, Session, select
import koco_product_sqlmodel.dbmodels.definition as sqm
import koco_product_sqlmodel.dbmodels.viewdef as vd
import koco_product_sqlmodel.dbmodels.support as sup
import os
import datetime as dt


def isnull(input, output):
    if not input:
        return output
    return input


def check_field_for_update(old_val: str, new_val: str):
    if old_val == new_val:
        return old_val, False
    return new_val, True


def translate_url_type(in_t: tuple = None) -> tuple:
    td = {
        "photo": "Photo",
        "step": "Step",
        "drawing": "Drawing",
        "datasheet": "Datasheet",
        "software": "Software",
        "supplier_site": "Supplier website",
        "speed_curves": "Speed curves",
        "screw_option": "Screw option",
        "torque_performance_curve": "Torque performance curve",
        "force_curve": "Force curce",
        "accessories": "Accessories",
        "product_datasheet": "Product datasheet",
        "manual": "Manual",
        "user_interface_software": "User interface software",
        "catalog": "Catalog",
        "certifications":"Certificates",
    }
    for element in in_t:
        element.type = td[element.type]
    return in_t


def create_mapper_table():
    SQLModel.metadata.create_all(mdb_engine)


def backup_database(fileurl: str = None, db_backup_folder: str = None, shell_com_path: str = None) -> int:
    if not fileurl:
        fileurl = os.path.join(
            db_backup_folder,
            dt.datetime.strftime(dt.datetime.now(), "%Y-%m-%d-%H-%M-%S")
            + "_db_backup.sql",
        )
    if not os.path.exists(db_backup_folder):
        os.makedirs(db_backup_folder, mode=0o777, exist_ok=True)
    if not os.path.exists(db_backup_folder):
        return -1
    mysql_cmd = os.path.join(shell_com_path, "mysqldump")
    os.system(f"{mysql_cmd} -u {os.environ["MARIADB_USER"]} -p'{os.environ["MARIADB_PW"]}' {os.environ["MARIADB_DATABASE"]} > {fileurl}")
    if not os.path.exists(fileurl):
        return -1
    return 1


def restore_database(fileurl: str = None, shell_com_path: str = None):
    if not fileurl:
        return -1
    if not os.path.exists(fileurl):
        return -1
    mysql_cmd = os.path.join(shell_com_path, "mysql")
    os.system(f"{mysql_cmd} -u {os.environ["MARIADB_USER"]} -p'{os.environ["MARIADB_PW"]}' {os.environ["MARIADB_DATABASE"]} < {fileurl}")
    return 1


def delete_database_backup(fileurl: str = None):
    if not fileurl:
        return -1
    if not os.path.exists(fileurl):
        return -1
    os.remove(fileurl)
    return 1


def update_object(db_object: SQLModel, update_data: dict):
    with Session(mdb_engine) as session:
        print(update_data)
        for d in update_data:
            db_object.__setattr__(d, update_data[d])
        session.add(db_object)
        session.commit()


def create_object(db_object_type: SQLModel, data: dict) -> SQLModel:
    db_obj = db_object_type()
    with Session(mdb_engine) as session:
        for d in data:
            db_obj.__setattr__(d, data[d])
        session.add(db_obj)
        session.commit()
        n_obj = session.exec(
            select(db_object_type).order_by(db_object_type.id.desc()).limit(1)
        ).one_or_none()
    return n_obj


def delete_translations_by_object_id(obj_id: int, object_type: SQLModel):
    with Session(mdb_engine) as session:
        statement = (
            select(vd.TTranslationMapper)
            .where(
                vd.TTranslationMapper.parent
                == sup.get_table_from_sqlmodels(object_type)
            )
            .where(vd.TTranslationMapper.parent_id == obj_id)
        )
        res = session.exec(statement)
        for object in res.all():
            session.delete(object)
        session.commit()


def delete_object_by_id(
    obj_id: int, object_type: SQLModel, delete_connected_items: bool = False
):
    with Session(mdb_engine) as session:
        if not delete_connected_items:
            statement = select(object_type).where(object_type.id == obj_id)
            res = session.exec(statement)
            res = res.one_or_none()
            session.delete(res)
            session.commit()
            return
        if object_type in (
            sqm.CUrl,
            sqm.CApplication,
            sqm.CSpecTableItem,
            sqm.CBacklog,
            sqm.COption,
            sqm.CCategoryMapper,
            sqm.CCategoryTree,
        ):
            statement = select(object_type).where(object_type.id == obj_id)
            res = session.exec(statement)
            res = res.one_or_none()
            session.delete(res)
            session.commit()
    if object_type == sqm.CSpecTable:
        delete_spectable_by_id(spectable_id=obj_id, delete_connected_items=True)
        return
    if object_type == sqm.CArticle:
        delete_article_by_id(article_id=obj_id, delete_connected_items=True)
        return
    if object_type == sqm.CFamily:
        delete_family_by_id(family_id=obj_id, delete_connected_items=True)
        return
    if object_type == sqm.CProductGroup:
        delete_product_group_by_id(product_group_id=obj_id, delete_connected_items=True)
        return
    if object_type == sqm.CCatalog:
        delete_catalog_by_id(catalog_id=obj_id, delete_connected_items=True)
        return
    delete_translations_by_object_id(obj_id=obj_id, object_type=object_type)


def delete_catalog_by_id(catalog_id: int, delete_connected_items: bool = False):
    with Session(mdb_engine) as session:
        cat = session.exec(
            select(sqm.CCatalog).where(sqm.CCatalog.id == catalog_id)
        ).one_or_none()
    if cat:
        delete_catalog(catalog=cat, delete_connected_items=delete_connected_items)


def delete_catalog(catalog: sqm.CCatalog, delete_connected_items: bool = True):
    if delete_connected_items:
        _delete_product_groups_from_catalog(
            catalog=catalog, delete_connected_items=True
        )
    with Session(mdb_engine) as session:
        session.delete(catalog)
        session.commit()


def _delete_product_groups_from_catalog(
    catalog: sqm.CCatalog, delete_connected_items: bool = True
):
    with Session(mdb_engine) as session:
        statement = select(sqm.CProductGroup).where(
            sqm.CProductGroup.catalog_id == catalog.id
        )
        res = session.exec(statement)
        pgs = res.all()
    for pg in pgs:
        delete_product_group(
            product_group=pg, delete_connected_items=delete_connected_items
        )


def delete_product_group_by_id(
    product_group_id: int, delete_connected_items: bool = False
):
    with Session(mdb_engine) as session:
        pg = session.exec(
            select(sqm.CProductGroup).where(sqm.CProductGroup.id == product_group_id)
        ).one_or_none()
    if pg:
        delete_product_group(
            product_group=pg, delete_connected_items=delete_connected_items
        )


def delete_product_group(
    product_group: sqm.CProductGroup, delete_connected_items: bool = True
):
    if delete_connected_items:
        _delete_families_from_product_group(
            product_group=product_group, delete_connected_items=True
        )
    with Session(mdb_engine) as session:
        session.delete(product_group)
        session.commit()


def _delete_families_from_product_group(
    product_group: sqm.CProductGroup, delete_connected_items: bool = True
):
    with Session(mdb_engine) as session:
        statement = select(sqm.CFamily).where(
            sqm.CFamily.product_group_id == product_group.id
        )
        res = session.exec(statement)
        families = res.all()
    for fam in families:
        delete_family(family=fam, delete_connected_items=delete_connected_items)


def delete_family_by_id(family_id: int, delete_connected_items: bool = False):
    with Session(mdb_engine) as session:
        fam = session.exec(
            select(sqm.CFamily).where(sqm.CFamily.id == family_id)
        ).one_or_none()
    if fam:
        delete_family(family=fam, delete_connected_items=delete_connected_items)


def delete_family(family: sqm.CFamily, delete_connected_items: bool = True):
    if delete_connected_items:
        _delete_urls_from_family(family)
        _delete_options_from_family(family)
        _delete_applications_from_family(family)
        _delete_spectables_from_family(family=family, delete_connected_items=True)
        _delete_articles_from_family(family=family, delete_connected_items=True)
    with Session(mdb_engine) as session:
        session.delete(family)
        session.commit()


def _delete_articles_from_family(
    family: sqm.CFamily, delete_connected_items: bool = True
):
    with Session(mdb_engine) as session:
        statement = select(sqm.CArticle).where(sqm.CArticle.family_id == family.id)
        res = session.exec(statement)
        articles = res.all()
    for art in articles:
        delete_article(article=art, delete_connected_items=delete_connected_items)


def _delete_spectables_from_family(
    family: sqm.CFamily, delete_connected_items: bool = True
):
    with Session(mdb_engine) as session:
        statement = (
            select(sqm.CSpecTable)
            .where(sqm.CSpecTable.parent == "family")
            .where(sqm.CSpecTable.parent_id == family.id)
        )
        res = session.exec(statement)
        for st in res.all():
            if delete_connected_items:
                statement = select(sqm.CSpecTableItem).where(
                    sqm.CSpecTableItem.spec_table_id == st.id
                )
                res2 = session.exec(statement)
                for sti in res2.all():
                    session.delete(sti)
            session.delete(st)
        session.commit()


def _delete_urls_from_family(family: sqm.CFamily):
    with Session(mdb_engine) as session:
        statement = (
            select(sqm.CUrl)
            .where(sqm.CUrl.parent_id == family.id)
            .where(sqm.CUrl.parent == "family")
        )
        res = session.exec(statement)
        for url in res.all():
            session.delete(url)
        session.commit()


def _delete_options_from_family(family: sqm.CFamily):
    with Session(mdb_engine) as session:
        statement = select(sqm.COption).where(sqm.COption.family_id == family.id)
        res = session.exec(statement)
        for option in res.all():
            session.delete(option)
        session.commit()


def _delete_applications_from_family(family: sqm.CFamily):
    with Session(mdb_engine) as session:
        statement = select(sqm.CApplication).where(
            sqm.CApplication.family_id == family.id
        )
        res = session.exec(statement)
        for application in res.all():
            session.delete(application)
        session.commit()


def delete_spectable_by_id(spectable_id: int, delete_connected_items: bool = True):
    with Session(mdb_engine) as session:
        st = session.exec(
            select(sqm.CSpecTable).where(sqm.CSpecTable.id == spectable_id)
        ).one_or_none()
    if st:
        delete_spectable(spectable=st, delete_connected_items=delete_connected_items)


def delete_spectable(spectable: sqm.CSpecTable, delete_connected_items: bool = True):
    if delete_connected_items:
        _delete_spectableitems_from_spectable(spectable=spectable)
    with Session(mdb_engine) as session:
        session.delete(spectable)
        session.commit()


def _delete_spectableitems_from_spectable(spectable: sqm.CSpecTable):
    with Session(mdb_engine) as session:
        stis = session.exec(
            select(sqm.CSpecTableItem).where(
                sqm.CSpecTableItem.spec_table_id == spectable.id
            )
        ).all()
        for sti in stis:
            session.delete(sti)
        session.commit()


def delete_article_by_id(article_id: int, delete_connected_items: bool = True):
    with Session(mdb_engine) as session:
        art = session.exec(
            select(sqm.CArticle).where(sqm.CArticle.id == article_id)
        ).one_or_none()
    if art:
        delete_article(article=art, delete_connected_items=delete_connected_items)


def delete_article(article: sqm.CArticle, delete_connected_items: bool = True):
    if delete_connected_items:
        _delete_urls_from_article(article)
        _delete_spectables_from_article(article=article, delete_connected_items=True)
    with Session(mdb_engine) as session:
        session.delete(article)
        session.commit()


def _delete_spectables_from_article(
    article: sqm.CArticle, delete_connected_items: bool = True
):
    with Session(mdb_engine) as session:
        statement = (
            select(sqm.CSpecTable)
            .where(sqm.CSpecTable.parent == "article")
            .where(sqm.CSpecTable.parent_id == article.id)
        )
        res = session.exec(statement)
        for st in res.all():
            if delete_connected_items:
                statement = select(sqm.CSpecTableItem).where(
                    sqm.CSpecTableItem.spec_table_id == st.id
                )
                res2 = session.exec(statement)
                for sti in res2.all():
                    session.delete(sti)
            session.delete(st)
        session.commit()


def _delete_urls_from_article(article: sqm.CArticle):
    with Session(mdb_engine) as session:
        statement = (
            select(sqm.CUrl)
            .where(sqm.CUrl.parent_id == article.id)
            .where(sqm.CUrl.parent == "article")
        )
        res = session.exec(statement)
        for url in res.all():
            session.delete(url)
        session.commit()


def insert_category_mapping(category_id: int, export_target: str, family_id: int):
    with Session(mdb_engine) as session:
        statement = (
            select(sqm.CCategoryMapper)
            .where(sqm.CCategoryMapper.category_id == category_id)
            .where(sqm.CCategoryMapper.family_id == family_id)
        )
        res = session.exec(statement).one_or_none()
        if res:
            return
        cm = sqm.CCategoryMapper(category_id=category_id, family_id=family_id, export_target = export_target)
        session.add(cm)
        session.commit()


def collect_category_tree(pid:int=1) -> dict[dict[dict]]:
    rd = []
    with Session(mdb_engine) as session:
        rd = _get_ct_children(session, pid=pid, level=1)
    return rd


def _get_ct_children(session, pid: int = None, level: int = None):
    if level > 3:
        return None
    if pid == None:
        return None
    children = {}
    statement = (
        select(sqm.CCategoryTree)
        .where(sqm.CCategoryTree.parent_id == pid)
        .order_by(sqm.CCategoryTree.pos)
    )
    layer1 = session.exec(statement).all()
    for child in layer1:
        statement = (
            select(sqm.CUrl)
            .where(sqm.CUrl.parent == "categorytree")
            .where(sqm.CUrl.parent_id == child.id)
            .where(sqm.CUrl.type == "photo")
        )
        urls = session.exec(statement).all()
        children[child.id] = {
            "node": child,
            "children": _get_ct_children(session, pid=child.id, level=level + 1),
            "urls": urls,
        }
    return children


def _add_category_photo_url(cat_id: int = None, KOCO_url: str = None):
    url = sqm.CUrl(
        type="photo",
        KOCO_url=KOCO_url,
        parent_id=cat_id,
        parent="categorytree",
        user_id=1,
    )
    print(url)
    with Session(mdb_engine) as session:
        session.add(url)
        session.commit()


def main()->None:
    pass

if __name__=="__main__":
    main()