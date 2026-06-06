from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.common.db import get_db
from app.territories import crud
from app.territories.schemas import (
    TerritoryCreate,
    TerritoryMetricCreate,
    TerritoryMetricRead,
    TerritoryMetricUpdate,
    TerritoryRead,
    TerritoryUpdate,
)

router = APIRouter(prefix="/territories", tags=["territories"])


@router.post("/", response_model=TerritoryRead, status_code=status.HTTP_201_CREATED)
def create_territory(data: TerritoryCreate, db: Session = Depends(get_db)):
    return crud.create_territory(db=db, data=data)


@router.get("/", response_model=List[TerritoryRead])
def list_territories(
    limit: int = Query(100, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return crud.list_territories(db=db, limit=limit, offset=offset)


@router.get("/intersects", response_model=List[TerritoryRead])
def list_intersecting_territories(
    wkt: str = Query(...),
    limit: int = Query(100, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return crud.list_intersecting_territories(
        db=db, wkt=wkt, limit=limit, offset=offset
    )


@router.get("/{territory_id}", response_model=TerritoryRead)
def get_territory(territory_id: int, db: Session = Depends(get_db)):
    territory = crud.get_territory(db=db, territory_id=territory_id)
    if territory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Territory not found"
        )
    return territory


@router.patch("/{territory_id}", response_model=TerritoryRead)
def update_territory(
    territory_id: int, data: TerritoryUpdate, db: Session = Depends(get_db)
):
    territory = crud.update_territory(db=db, territory_id=territory_id, data=data)
    if territory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Territory not found"
        )
    return territory


@router.delete("/{territory_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_territory(territory_id: int, db: Session = Depends(get_db)):
    success = crud.delete_territory(db=db, territory_id=territory_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Territory not found"
        )
    return None


@router.post(
    "/{territory_id}/metrics",
    response_model=TerritoryMetricRead,
    status_code=status.HTTP_201_CREATED,
)
def create_metric(
    territory_id: int, data: TerritoryMetricCreate, db: Session = Depends(get_db)
):
    territory = crud.get_territory(db=db, territory_id=territory_id)
    if territory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Territory not found"
        )
    return crud.create_metric(db=db, territory_id=territory_id, data=data)


@router.get("/{territory_id}/metrics", response_model=List[TerritoryMetricRead])
def list_metrics_by_territory(territory_id: int, db: Session = Depends(get_db)):
    territory = crud.get_territory(db=db, territory_id=territory_id)
    if territory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Territory not found"
        )
    return crud.list_metrics_by_territory(db=db, territory_id=territory_id)


@router.patch("/{territory_id}/metrics/{metric_id}", response_model=TerritoryMetricRead)
def update_metric(
    territory_id: int,
    metric_id: int,
    data: TerritoryMetricUpdate,
    db: Session = Depends(get_db),
):
    territory = crud.get_territory(db=db, territory_id=territory_id)
    if territory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Territory not found"
        )

    metric = crud.update_metric(db=db, metric_id=metric_id, data=data)
    if metric is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Metric not found"
        )
    return metric


@router.delete(
    "/{territory_id}/metrics/{metric_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_metric(territory_id: int, metric_id: int, db: Session = Depends(get_db)):
    territory = crud.get_territory(db=db, territory_id=territory_id)
    if territory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Territory not found"
        )

    success = crud.delete_metric(db=db, metric_id=metric_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Metric not found"
        )
    return None
