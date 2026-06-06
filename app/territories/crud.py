from typing import Any, List, Optional

from geoalchemy2.elements import WKTElement
from sqlalchemy import delete, func, select
from sqlalchemy.engine.row import Row
from sqlalchemy.orm import Session

from app.territories.models import Territory, TerritoryMetric
from app.territories.schemas import (
    TerritoryCreate,
    TerritoryMetricCreate,
    TerritoryMetricUpdate,
    TerritoryUpdate,
)


def _territory_select() -> Any:
    return select(
        Territory.id,
        Territory.name,
        TerritoryType := Territory.territory_type,
        Territory.level,
        Territory.description,
        func.ST_AsText(Territory.geom).label("geom_wkt"),
        Territory.created_at,
    )


def get_territory(db: Session, territory_id: int) -> Optional[Row]:
    stmt = _territory_select().where(Territory.id == territory_id)
    return db.execute(stmt).first()


def list_territories(db: Session, limit: int = 100, offset: int = 0) -> List[Row]:
    stmt = _territory_select().order_by(Territory.id).limit(limit).offset(offset)
    return db.execute(stmt).all()


def create_territory(db: Session, data: TerritoryCreate) -> Optional[Row]:
    spatial_geom = WKTElement(data.geom_wkt, srid=4326)
    db_territory = Territory(
        name=data.name,
        territory_type=data.territory_type,
        level=data.level,
        description=data.description,
        geom=spatial_geom,
    )
    db.add(db_territory)
    db.commit()
    db.refresh(db_territory)
    return get_territory(db, db_territory.id)


def update_territory(
    db: Session, territory_id: int, data: TerritoryUpdate
) -> Optional[Row]:
    db_territory = db.get(Territory, territory_id)
    if not db_territory:
        return None

    update_data = data.model_dump(exclude_unset=True)

    if "geom_wkt" in update_data:
        wkt_str = update_data.pop("geom_wkt")
        db_territory.geom = WKTElement(wkt_str, srid=4326)

    for key, value in update_data.items():
        setattr(db_territory, key, value)

    db.commit()
    db.refresh(db_territory)

    return get_territory(db, db_territory.id)


def delete_territory(db: Session, territory_id: int) -> bool:
    db_territory = db.get(Territory, territory_id)
    if not db_territory:
        return False

    db.delete(db_territory)
    db.commit()
    return True


def list_intersecting_territories(
    db: Session, wkt: str, limit: int = 100, offset: int = 0
) -> List[Row]:
    search_geom = WKTElement(wkt, srid=4326)
    stmt = (
        _territory_select()
        .where(func.ST_Intersects(Territory.geom, search_geom))
        .order_by(Territory.id)
        .limit(limit)
        .offset(offset)
    )
    return db.execute(stmt).all()


def create_metric(
    db: Session, territory_id: int, data: TerritoryMetricCreate
) -> TerritoryMetric:
    db_metric = TerritoryMetric(territory_id=territory_id, **data.model_dump())
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric


def list_metrics_by_territory(db: Session, territory_id: int) -> List[TerritoryMetric]:
    stmt = (
        select(TerritoryMetric)
        .where(TerritoryMetric.territory_id == territory_id)
        .order_by(TerritoryMetric.year)
    )
    return list(db.scalars(stmt).all())


def update_metric(
    db: Session, metric_id: int, data: TerritoryMetricUpdate
) -> Optional[TerritoryMetric]:
    db_metric = db.get(TerritoryMetric, metric_id)
    if not db_metric:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_metric, key, value)

    db.commit()
    db.refresh(db_metric)
    return db_metric


def delete_metric(db: Session, metric_id: int) -> bool:
    db_metric = db.get(TerritoryMetric, metric_id)
    if not db_metric:
        return False

    db.delete(db_metric)
    db.commit()
    return True
