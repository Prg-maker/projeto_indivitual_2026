from sqlalchemy import Column, Integer, String, JSON , ForeignKey
from connection import Base


class DocumentoProcessado(Base):
    __tablename__ = "documentos_processados"

    id = Column(
        String(64),
        primary_key=True
    )
class RelatorioExtraido(Base):
    __tablename__ = "relatorios_extraidos"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    documento_id = Column(
        String(64),
        ForeignKey("documentos_processados.id")
    )

    empresa = Column(String(50))

    ano = Column(Integer)

    trimestre = Column(Integer)

    indicadores = Column(JSON)