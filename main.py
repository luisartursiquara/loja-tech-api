from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from database import SessionLocal, engine, Base
import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TechStore API",
    description="API Back-End do projeto TechStore",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PedidoCreate(BaseModel):
    total: float

class PedidoUpdate(BaseModel):
    status: str

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.get("/")
def inicio():
    return {
        "mensagem": "TechStore API está a funcionar!"
    }


@app.get("/status")
def status():
    return {
        "status": "online"
    }

@app.post("/pedidos")
def criar_pedido(
    pedido: PedidoCreate,
    db: Session = Depends(get_db)
):
    novo_pedido = models.Pedido(
        total=pedido.total,
        status="pendente"
    )

    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)

    return novo_pedido

@app.get("/pedidos")
def listar_pedidos(db: Session = Depends(get_db)):

    pedidos = db.query(models.Pedido).all()

    return pedidos

@app.get("/pedidos/{pedido_id}")
def obter_pedido(
    pedido_id: int,
    db: Session = Depends(get_db)
):
    pedido = db.query(models.Pedido).filter(
        models.Pedido.id == pedido_id
    ).first()

    if pedido is None:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    return pedido

@app.patch("/pedidos/{pedido_id}")
def atualizar_pedido(
    pedido_id: int,
    dados: PedidoUpdate,
    db: Session = Depends(get_db)
):
    pedido = db.query(models.Pedido).filter(
        models.Pedido.id == pedido_id
    ).first()

    if pedido is None:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    pedido.status = dados.status

    db.commit()
    db.refresh(pedido)

    return pedido

@app.delete("/pedidos/{pedido_id}")
def eliminar_pedido(
    pedido_id: int,
    db: Session = Depends(get_db)
):
    pedido = db.query(models.Pedido).filter(
        models.Pedido.id == pedido_id
    ).first()

    if pedido is None:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    db.delete(pedido)
    db.commit()

    return {
        "mensagem": "Pedido eliminado com sucesso"
    }