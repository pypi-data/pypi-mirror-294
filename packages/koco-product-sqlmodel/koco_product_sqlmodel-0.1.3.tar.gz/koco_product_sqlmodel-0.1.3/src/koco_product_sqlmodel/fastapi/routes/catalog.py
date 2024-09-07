from typing import Annotated
from fastapi import APIRouter, Depends, Request

import koco_product_sqlmodel.fastapi.routes.security as sec
import koco_product_sqlmodel.dbmodels.definition_reduced as sqmr
import koco_product_sqlmodel.mdb_connect.catalogs as mdb_cat
import koco_product_sqlmodel.mdb_connect.mdb_connector as mdb_con

router = APIRouter(dependencies=[Depends(sec.get_current_active_user)])

@router.get("/")
def get_catalogs():
    catalogs = mdb_cat.collect_catalogs_db_items()
    return catalogs

@router.get("/{id}/")
def get_catalog_by_id(id):
    catalog = mdb_cat.collect_catalog_by_id(id)
    return catalog

@router.post("/", dependencies=[Depends(sec.has_post_rights)])
def create_catalog(catalog: sqmr.CCatalog) -> mdb_cat.CCatalog:
    new_catalog = mdb_cat.create_catalog(
        mdb_cat.CCatalog(
            supplier=catalog.supplier, year=catalog.year, status=catalog.status, user_id=1
        )
    )
    print(catalog)
    return new_catalog

@router.delete("/{id}/", dependencies=[Depends(sec.has_post_rights)])
def delete_catalog_by_id(request: Request, id: int, delete_recursive: bool=False):
    """
    Delete a catalog item by ccatalog.id. 
    Request parameter: delete_recursive=1
    If set all subitems contained in given catalog will be removed from database to avoid orphaned data
    """
    print(delete_recursive)
    if delete_recursive==True:
        delete_recursive=True
    mdb_con.delete_catalog_by_id(catalog_id=id, delete_connected_items=delete_recursive)
    return {'ok': True}
    

def main():
    pass

if __name__=="__main__":
    main()