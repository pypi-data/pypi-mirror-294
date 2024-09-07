from sqlmodel import select, text, Session
from koco_product_sqlmodel.mdb_connect.init_db_con import mdb_engine
from koco_product_sqlmodel.mdb_connect.mdb_connector import mdb_engine, isnull
from koco_product_sqlmodel.dbmodels.definition import (
    CArticle,
    CSpecTable,
    CSpecTableItem,
)
from typing import List


def collect_overview_spectables_ids(family_id:int) -> list[int]:
    engine = mdb_engine
    with Session(engine) as session:
        statement = (
            select(CSpecTable)
            .join(
                CArticle,
                CArticle.id == CSpecTable.parent_id,
            )
            .where(CArticle.family_id == family_id)
            .where(CSpecTable.parent == "article")
            .where(CSpecTable.parent_id == CArticle.id)
            .where(CSpecTable.type == "overview")
            .order_by(CArticle.id)
        )
        result =  session.exec(statement)
        if result:
            return [r.id for r in result]
    

def collect_overview_spectables(
    engine=None,
    fam_info: tuple = None,
    family_id: int = None,
    table_header_hrefs: bool = True,
):
    if not engine:
        engine = mdb_engine
    with Session(engine) as session:
        statement = (
            select(CSpecTable, CArticle)
            .join(
                CArticle,
                CArticle.id == CSpecTable.parent_id,
            )
            .where(CArticle.family_id == family_id)
            .where(CSpecTable.parent == "article")
            .where(CSpecTable.parent_id == CArticle.id)
            .where(CSpecTable.type == "overview")
            .order_by(CArticle.id)
        )
        results = session.exec(statement)
        overview = {"query_data": []}
        overview["table_headers"] = [["", "Name", "Unit"]]
        overview["type"] = "overview"
        overview["has_unit"] = True
        results = results.all()
        # print(results)
    for ix, st_art in enumerate(results):
        st, art = st_art
        if ix == 0:
            overview["heading"] = st.name
        if fam_info["supplier"] in ["Constar Motion", "Motor Power Company", "Novanta"]:
            overview["table_headers"][0].append(
                _build_article_href_str(
                    art.article[len(fam_info["family"]["family"]) :],
                    art.id,
                    table_header_hrefs,
                )
            )
        else:
            overview["table_headers"][0].append(
                _build_article_href_str(art.article, art.id, table_header_hrefs)
            )
        res = _get_spectable_items(spectable_id=st.id)
        for iy, rr in enumerate(res):
            if ix == 0:
                overview["query_data"].append([rr.pos, rr.name, isnull(rr.unit, " - ")])
            overview["query_data"][iy].append(isnull(rr.value, " - "))
    try:
        overview["hrefs"] = ["" for hr in range(len(overview["query_data"][0]) + 2)]
    except:
        overview["hrefs"] = []
    return overview


def collect_family_spectables(engine=None, family_id: int = None):
    if not engine:
        engine = mdb_engine
    with Session(engine) as session:
        statement = (
            select(CSpecTable)
            .where(CSpecTable.parent_id == family_id)
            .where(CSpecTable.parent == "family")
            .order_by(CSpecTable.id)
        )
        results = session.exec(statement).all()
        st_tuple = []
    for spect in results:
        if spect.type == "multicol":
            st = collect_multicol_spectable(
                spect.id, spect.name, spect.type, spect.has_unit
            )
        if spect.type == "singlecol":
            st = collect_singlecol_spectable(
                spect.id, spect.name, spect.type, spect.has_unit
            )
        if spect.type == "free":
            st = collect_free_spectable(
                spect.id, spect.name, spect.type, spect.has_unit
            )
        st_tuple.append(st)
    return st_tuple


def collect_article_spectables(engine=None, article_id: int = None) -> tuple:
    if not engine:
        engine = mdb_engine
    sts = collect_article_overview_spectable(article_id=article_id)
    with Session(engine) as session:
        statement = (
            select(CSpecTable)
            .where(CSpecTable.parent_id == article_id)
            .where(CSpecTable.parent == "article")
            .order_by(CSpecTable.id)
        )
        results = session.exec(statement).all()
    for r in results:
        if r.type == "multicol":
            sts.append(collect_multicol_spectable(r.id, r.name, r.type, r.has_unit))
        if r.type == "singlecol":
            sts.append(collect_singlecol_spectable(r.id, r.name, r.type, r.has_unit))
        if r.type == "free":
            sts.append(collect_free_spectable(r.id, r.name, r.type, r.has_unit))
    return sts


def collect_free_spectable(
    spectable_id: int = None,
    spectable_heading: str = None,
    spectable_type: str = None,
    has_unit: bool = True,
) -> dict:
    st = {"heading": spectable_heading, "has_unit": has_unit, "type": spectable_type}
    st_items = _get_spectable_items(spectable_id=spectable_id)
    st["table_headers"] = _get_free_spectable_headers(st_items)
    st["query_data"] = _get_free_query_data(st_items)
    st["hrefs"] = ["" for d in st["table_headers"][0]]
    print(st["table_headers"])
    return st


def _get_free_spectable_headers(st_items: tuple) -> tuple:
    headers = [""]
    for sti in st_items:
        p_split = str(sti.pos).split(";")
        if int(p_split[0]) == 0:
            headers.append(sti.value)
    return [headers]


def _get_free_query_data(st_items: tuple) -> tuple:
    qd = []
    nrows, ncols, _, _ = _get_number_of_rows_and_cols("free", st_items)
    for ix in range(1, nrows):
        qdd = []
        qdd.append(ix)
        for iy in range(1, ncols + 1):
            sti = _get_free_spectable_cell(st_items, ix, iy)
            if sti:
                qdd.append(isnull(sti.value, ""))
        qd.append(qdd)
    return qd


def _get_free_spectable_cell(st_items: tuple, row_ix, col_ix) -> CSpecTableItem:
    pos = f"{row_ix};{col_ix}"
    for sti in st_items:
        if sti.pos == pos:
            return sti
    return None


def collect_singlecol_spectable(
    spectable_id: int = None,
    spectable_heading: str = None,
    spectable_type: str = None,
    has_unit: bool = True,
) -> dict:
    st = {"heading": spectable_heading, "has_unit": has_unit, "type": spectable_type}
    st_items = _get_spectable_items(spectable_id=spectable_id)
    st["table_headers"] = _get_singlecol_spectable_headers(st_items, has_unit)
    st["query_data"] = _get_singlecol_query_data(st_items, has_unit)
    st["hrefs"] = ["" for d in st["table_headers"][0]]
    return st


def _get_singlecol_spectable_headers(st_items: tuple, has_unit: bool) -> tuple:
    headers = ["", "Name"]
    if has_unit:
        headers.append("Unit")
    headers += ["Value", "min Value", "max Value"]
    # print(headers)
    return [headers]


def _get_singlecol_query_data(st_items: tuple, has_unit: bool) -> tuple:
    qd = []
    for ix, rr in enumerate(st_items):
        qdd = [ix, rr.name]
        if has_unit:
            qdd.append(isnull(rr.unit, " - "))
        qdd += [
            isnull(rr.value, ""),
            isnull(rr.min_value, ""),
            isnull(rr.max_value, ""),
        ]
        qd.append(qdd)
    return qd


def collect_multicol_spectable(
    spectable_id: int, spectable_heading: str, spectable_type: str, has_unit: bool
) -> dict:
    st = {"heading": spectable_heading, "has_unit": has_unit, "type": spectable_type}
    st_items = _get_spectable_items(spectable_id=spectable_id)
    st["table_headers"] = _get_multicol_spectable_headers(st_items, has_unit)
    st["query_data"] = _get_multicol_query_data(st_items, has_unit)
    st["hrefs"] = ["" for d in range(len(st["query_data"][0]) + 2)]
    return st


def collect_spectable_object_with_items(st_id: int) -> dict:
    if not st_id:
        return None
    with Session(mdb_engine) as session:
        statement = select(CSpecTable).where(CSpecTable.id == st_id)
        st = session.exec(statement).one_or_none()
        if not st:
            return None
        statement = select(CSpecTableItem).where(CSpecTableItem.spec_table_id == st_id)
        st_items = session.exec(statement).all()
        return {
            "parent": st,
            "children": st_items,
            "p_header": (
                "id",
                "name",
                "type",
                "has_unit",
                "parent",
                "parent_id",
                "insdate",
                "upddate",
            ),
            "c_header": (
                "id",
                "pos",
                "name",
                "unit",
                "value",
                "min_value",
                "max_value",
                "spec_table_id",
                "insdate",
                "upddate",
            ),
        }


def _get_multicol_spectable_headers(st_items: tuple, has_unit: bool) -> tuple:
    headers = ["", "Name"]
    if has_unit:
        headers.append("Unit")
    for sti in st_items:
        p_split = str(sti.pos).split(";")
        if int(p_split[0]) == 0:
            headers.append(sti.name)
    return [headers]


def _get_multicol_query_data(st_items: tuple, has_unit: bool) -> tuple:
    qd = []
    nrows, ncols, has_row_headers, _ = _get_number_of_rows_and_cols(
        "multicol", st_items
    )
    for ix, rr in enumerate(st_items[:nrows]):
        qdd = []
        if not has_row_headers:
            qdd.append(ix + 1)
        qdd.append(rr.name)
        if has_unit:
            qdd.append(isnull(rr.unit, " - "))
        if not has_row_headers:
            for iy in range(ncols):
                qdd.append(st_items[iy * nrows + ix].value)
        else:
            for iy in range(1, ncols):
                qdd.append(st_items[iy * nrows + ix].value)
        qd.append(qdd)
    return qd


def collect_article_overview_spectable(engine=None, article_id: int = None):
    if not engine:
        engine = mdb_engine
    with Session(engine) as session:
        statement = (
            select(CSpecTable.id, CSpecTable.name, CArticle.id, CArticle.article)
            .join(CArticle, CArticle.id == CSpecTable.parent_id)
            .where(CArticle.id == article_id)
            .where(CSpecTable.type == "overview")
            .where(CSpecTable.parent == "article")
        )
        results = session.exec(statement)
        overview = []
    for r in results:
        st = {}
        st["query_data"] = []
        st["table_headers"] = [
            ["", "Name", "Unit", "Value", "min. Value", "max. Value"]
        ]
        st["heading"] = r[1]
        res = _get_spectable_items(spectable_id=r[0])
        for rr in res:
            st["query_data"].append(
                [
                    rr.pos,
                    rr.name,
                    isnull(rr.unit, " - "),
                    isnull(rr.value, ""),
                    isnull(rr.min_value, ""),
                    isnull(rr.max_value, ""),
                ]
            )
        st["hrefs"] = ["" for hr in st["table_headers"][0]]
        overview.append(st)
    return overview


def _get_spectable_items(engine=None, spectable_id: int = None) -> List[CSpecTableItem]:
    if not engine:
        engine = mdb_engine
    with Session(engine) as session:
        statement = (
            select(CSpecTableItem)
            .where(CSpecTableItem.spec_table_id == spectable_id)
            .order_by(text("cast(substring_index(cspectableitem.pos,';',-1) as int)"))
            .order_by(text("cast(substring_index(cspectableitem.pos,';',1) as int)"))
        )
        res = session.exec(statement).all()
    return res


def _get_number_of_rows_and_cols(st_type, res):
    if st_type in ("overview", "singlecol"):
        return len(res), 1, False, True
    n_cols = 0
    n_rows = 0
    has_col_headers = False
    has_row_headers = False
    if st_type in ("multicol", "free"):
        r_tuple = []
        c_tuple = []
        for r in res:
            r_s = r.pos.split(";")
            if len(r_s) > 1:
                r_tuple.append(int(r_s[0]))
                c_tuple.append(int(r_s[1]))
            else:
                r_tuple.append(int(r_s[0]))
        r_tuple = _remove_duplicates_from_tuple(r_tuple)
        c_tuple = _remove_duplicates_from_tuple(c_tuple)
        try:
            n_rows = max(r_tuple)
        except:
            n_rows = 1
        try:
            n_cols = max(c_tuple)
        except:
            n_cols = 1
        # print(r_tuple)
        # print(c_tuple)
        if 0 in r_tuple:
            n_rows += 1
            has_col_headers = True
        if 0 in c_tuple:
            n_cols += 1
            has_row_headers = True
        # print(n_rows, n_cols)
    return n_rows, n_cols, has_row_headers, has_col_headers


def _build_article_href_str(
    instr: str = None, article_id: int = None, table_header_hrefs: bool = True
):
    if table_header_hrefs:
        return (
            f'<a href="/article?article_id={article_id}" alt="article ID={article_id}">'
            + instr
            + "</a>"
        )
    return instr


def _remove_duplicates_from_tuple(in_t: tuple) -> tuple:
    out_t = []
    for r in in_t:
        if r not in out_t:
            out_t.append(r)
    return out_t


def create_spectable(spectable: CSpecTable) -> CSpecTable:
    if not spectable:
        return
    with Session(mdb_engine) as session:
        session.add(spectable)
        session.commit()
        statement = (
            select(CSpecTable)
            .where(CSpecTable.name == spectable.name)
            .where(CSpecTable.parent == spectable.parent)
            .where(CSpecTable.parent_id == spectable.parent_id)
        )
        return session.exec(statement=statement).one_or_none()


def create_spectable_item(
    spectable_item: CSpecTableItem, spectable: CSpecTable
) -> CSpecTableItem:
    if not spectable_item:
        return
    with Session(mdb_engine) as session:
        session.add(spectable_item)
        session.commit()
        if not CSpecTable:
            return
        statement = (
            select(CSpecTableItem)
            .join(CSpecTable, CSpecTable.id == CSpecTableItem.spec_table_id)
            .where(CSpecTableItem.pos == spectable_item.pos)
            .where(CSpecTableItem.spec_table_id == spectable_item.spec_table_id)
            .where(CSpecTableItem.spec_table_id == spectable_item.spec_table_id)
            .where(CSpecTable.parent == spectable.parent)
            .where(CSpecTable.parent_id == spectable.parent_id)
        )
        return session.exec(statement=statement).one_or_none()


def delete_spectable(spectable: CSpecTable, delete_connected_items: bool = True):
    if delete_connected_items:
        _delete_spectable_items_from_spectable(
            spectable=spectable, delete_connected_items=True
        )
    with Session(mdb_engine) as session:
        session.delete(spectable)
        session.commit()


def _delete_spectable_items_from_spectable(
    spectable: CSpecTable, delete_connected_items: bool = True
):
    with Session(mdb_engine) as session:
        statement = select(CSpecTableItem).where(
            CSpecTableItem.spec_table_id == spectable.id
        )
        res = session.exec(statement)
        for sti in res.all():
            session.delete(sti)
        session.commit()


def _spectable_item_position_exists(
    spectable_items: List[CSpecTableItem], position: str
):
    for spectable_item in spectable_items:
        if spectable_item.pos == position:
            return True
    return False

def _get_next_position_from_spectable_items(stis: list[CSpecTableItem]):
    max_pos = -1
    for sti in stis:
        if int(sti.pos)>max_pos:
            max_pos=int(sti.pos)
    return str(max_pos+1)


def insert_spectable_item_at_position(
    spectable: CSpecTable, spectable_item: CSpecTableItem, position: str|None
):
    """Fügt einen SpecTableItem an einer Position ein und verschiebt die Items dahinter weiter nach hinten. Bislang nicht im Einsatz"""
    spectable_items = _get_spectable_items(spectable_id=spectable.id)
    if not position:
        position = _get_next_position_from_spectable_items(stis = spectable_items)
    with Session(mdb_engine) as session:
        if _spectable_item_position_exists(spectable_items, position):
            if ";" in position:
                # Umgang mit MultiCol Spectables muss noch definiert werden
                pass
            else:
                for s_item in spectable_items:
                    pos_int = int(s_item.pos)
                    if pos_int >= int(position):
                        s_item.pos = str(pos_int + 1)
                        session.add(s_item)
        spectable_item.spec_table_id = spectable.id
        spectable_item.pos = position

        print(spectable_item)
        session.add(spectable_item)
        session.commit()


def main()->None:
    pass

if __name__=="__main__":
    main()