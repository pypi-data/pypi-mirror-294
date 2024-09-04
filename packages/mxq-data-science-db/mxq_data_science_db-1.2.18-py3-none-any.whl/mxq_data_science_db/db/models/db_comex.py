"""SQL models for db_comex
"""

from datetime import datetime
import logging

import pandas as pd
from sqlalchemy import delete

from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa

from mxq_data_science_db.db.db import SQLConnection
from mxq_data_science_db.db.models.base import BaseModel

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

Base = declarative_base()
metadata = Base.metadata


class NCM(Base, BaseModel):
    """Table with NCMs data"""

    __tablename__ = "ncm"
    ncm = sa.Column(sa.String(20), primary_key=True)
    pais = sa.Column(sa.String(2), primary_key=True)
    classificacao = sa.Column(sa.String(50), primary_key=True)
    descricao = sa.Column(sa.String(300), primary_key=True)
    material = sa.Column(sa.String(30), primary_key=True)
    parte = sa.Column(sa.Integer())
    multiplicador = sa.Column(sa.Float())


class MMIComexSicori(Base, BaseModel):
    """Table for processed data for MMI BR Siscori (tab destaques)"""

    __tablename__ = "mmi_comex_br_siscori"
    numero_de_ordem = sa.Column(sa.String(20), primary_key=True)
    resina = sa.Column(sa.String(3), primary_key=True)
    anomes = sa.Column(sa.Integer, primary_key=True)
    cod_ncm = sa.Column(sa.String(10), primary_key=True)
    descricao_do_codigo_ncm = sa.Column(sa.String(50))
    pais_de_origem = sa.Column(sa.String(50))
    pais_de_aquisicao = sa.Column(sa.String(50))
    unidade_de_medida = sa.Column(sa.String(50))
    unidade_comerc = sa.Column(sa.String(50))
    descricao_do_produto = sa.Column(sa.String(700))
    qtde_estatistica = sa.Column(sa.Float)
    peso_liquido = sa.Column(sa.Float)
    vmle_dolar = sa.Column(sa.Float)
    vl_frete_dolar = sa.Column(sa.Float)
    vl_seguro_dolar = sa.Column(sa.Float)
    valor_un_prod_dolar = sa.Column(sa.Float)
    qtd_comercial = sa.Column(sa.Float)
    tot_un_prod_dolar = sa.Column(sa.Float)
    unidade_desembarque = sa.Column(sa.String(50))
    unidade_desembaraco = sa.Column(sa.String(50))
    incoterm = sa.Column(sa.String(3))
    nat_informacao = sa.Column(sa.String(50))
    situacao_do_despacho = sa.Column(sa.String(50))
    preco_total = sa.Column(sa.Float)
    frete_ponderado = sa.Column(sa.Float)
    seguro_ponderado = sa.Column(sa.Float)
    vmle_dolar_ponderado = sa.Column(sa.Float)
    peso_liquido_ponderado = sa.Column(sa.Float)
    tipo = sa.Column(sa.String(200))
    fornecedor = sa.Column(sa.String(200))
    aplicacao = sa.Column(sa.String(50))
    produtor = sa.Column(sa.String(50))
    processo = sa.Column(sa.String(100))
    updated_at = sa.Column(
        sa.DATETIME(), nullable=False, default=sa.text("CURRENT_TIMESTAMP")
    )
    sa.Index("mmi_comex_br_siscori_IDX", anomes, resina)

    @classmethod
    def delete_before_insert(cls, df: pd.DataFrame):
        """Delete all records for resina

        Args:
            df (pd.DataFrame): dataframe
        """
        list_resina = list(set(df[cls.resina.name]))

        assert len(list_resina) != 0, "No resina set"
        assert len(list_resina) == 1, "Only one resina can be updated per time"

        resina = list_resina[0]

        with SQLConnection() as con:
            logger.info(f"Delete before upsert, resina={resina}")
            stmt = delete(cls).where(cls.resina == resina)
            con.execute(stmt)
        cls.bulk_insert(df, chuck_size=10**3)

class ComexReleaseCalendar(Base, BaseModel):
    """Table for release caledar from MMI comex"""

    __tablename__ = "comex_release_calendar"
    period_ref = sa.Column(sa.DATETIME(), primary_key=True)
    updated_at = sa.Column(sa.DATETIME())
    next_update_at = sa.Column(sa.DATETIME())
    released_at = sa.Column(sa.DATETIME())
    updated_at = sa.Column(
        sa.DATETIME(), nullable=False, default=sa.text("CURRENT_TIMESTAMP")
    )
    @classmethod
    def upinsert(cls, df: pd.DataFrame):

        cls.bulk_upsert(df, chuck_size=10**3, columns_not_update=["released_at"])


class MMIComexBRProcessed(Base, BaseModel):
    """Table for processed data for MMI BR"""

    __tablename__ = "mmi_comex_br_processed"
    ncm = sa.Column(sa.String(10), primary_key=True)
    fluxo = sa.Column(sa.String(3), primary_key=True)
    data = sa.Column(sa.DATETIME(), primary_key=True)
    ano = sa.Column(sa.Integer(), primary_key=True)
    mes = sa.Column(sa.Integer(), primary_key=True)
    pais = sa.Column(sa.String(2), primary_key=True)
    uf = sa.Column(sa.String(2), primary_key=True)
    via = sa.Column(sa.String(30), primary_key=True)
    urf = sa.Column(sa.String(80), primary_key=True)
    resina = sa.Column(sa.String(10), primary_key=True)
    kg_liquido = sa.Column(sa.Float())
    vl_fob = sa.Column(sa.Float())
    updated_at = sa.Column(
        sa.DATETIME(), nullable=False, default=sa.text("CURRENT_TIMESTAMP")
    )
    sa.Index("mmi_comex_br_processed_data_IDX", data, fluxo, resina)
    sa.Index("mmi_comex_br_processed_data_pais_IDX", data, fluxo, pais, resina)

    @classmethod
    def delete_before_insert(cls, df: pd.DataFrame):
        """Delete all records for the years in the DF

        Args:
            df (pd.DataFrame): dataframe
        """
        list_ano = list(set(df[cls.ano.name]))

        assert len(list_ano) != 0, "No year set"
        assert len(list_ano) == 1, "Only one year can be updated per time"

        ano = list_ano[0]

        with SQLConnection() as con:
            logger.info(f"Delete before upsert, ano={ano}")
            stmt = delete(cls).where(cls.ano == ano)
            con.execute(stmt)

        cls.bulk_upsert(df, chuck_size=10**4)


class MMOComexProcessed(Base, BaseModel):
    """Table for processed data for MMO"""

    __tablename__ = "mmo_comex_processed"
    data = sa.Column(sa.DATETIME(), primary_key=True)
    ano = sa.Column(sa.Integer(), primary_key=True)
    mes = sa.Column(sa.Integer(), primary_key=True)
    fluxo = sa.Column(sa.String(3), primary_key=True)
    pais_origem = sa.Column(sa.String(2), primary_key=True)
    pais_destino = sa.Column(sa.String(2), primary_key=True)
    pais_relatorio = sa.Column(sa.String(2), primary_key=True)
    ncm_relatorio = sa.Column(sa.String(20), primary_key=True)
    resina = sa.Column(sa.String(10), primary_key=True)
    peso_kg = sa.Column(sa.Float())
    fob_usd = sa.Column(sa.Float())
    updated_at = sa.Column(
        sa.DATETIME(), nullable=False, default=sa.text("CURRENT_TIMESTAMP")
    )

    @classmethod
    def delete_before_insert(cls, df: pd.DataFrame):
        """Delete all records for the years in the DF

        Args:
            df (pd.DataFrame): dataframe
        """
        # Check ano
        list_ano = list(set(df[cls.ano.name]))

        assert len(list_ano) != 0, "No year set"
        assert len(list_ano) == 1, "Only one year can be updated per time"

        # Check pais relatorio
        list_pais = list(set(df[cls.pais_relatorio.name]))

        assert len(list_pais) != 0, "No pais_relatorio set"
        assert len(list_pais) == 1, "Only pais_relatorio can be updated per time"

        # Check ncm
        list_ncm = list(set(df[cls.ncm_relatorio.name]))

        assert len(list_ncm) != 0, "No ncm_relatorio set"
        assert len(list_ncm) == 1, "Only one ncm_relatorio can be updated per time"

        ano = list_ano[0]
        pais_relatorio = list_pais[0]
        ncm_relatorio = list_ncm[0]

        with SQLConnection() as con:
            logger.info(
                f"Delete before upsert, ano={ano}, pais_relatorio={pais_relatorio}, ncm_relatorio={ncm_relatorio}"
            )
            stmt = delete(cls).where(
                cls.ano == ano,
                cls.pais_relatorio == pais_relatorio,
                cls.ncm_relatorio == ncm_relatorio,
            )
            con.execute(stmt)

        cls.bulk_upsert(df, chuck_size=10**4)


class MMOComexRegion(Base, BaseModel):
    """Table for regions MMO"""

    __tablename__ = "mmo_comex_region"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    region = sa.Column(sa.String(100), primary_key=True)
    latitude = sa.Column(sa.Float, nullable=False)
    longitude = sa.Column(sa.Float, nullable=False)


class MMOComexCountry(Base, BaseModel):
    """Table for countries MMO"""

    __tablename__ = "mmo_comex_country"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    country_simbol = sa.Column(sa.String(2), primary_key=True)
    country = sa.Column(sa.String(100))
    region = sa.Column(sa.Integer, sa.ForeignKey("mmo_comex_region.id"), nullable=False)
    latitude = sa.Column(sa.Float, nullable=False)
    longitude = sa.Column(sa.Float, nullable=False)


class MMOComexBrasilConsumoDetalhado(Base, BaseModel):
    """Table for MMO with data about: brasil consumo detalhado"""

    __tablename__ = "mmo_comex_brasil_consumo_detalhado"
    resina = sa.Column(sa.String(10), primary_key=True)
    pais = sa.Column(sa.String(100), primary_key=True)
    pais_simbolo = sa.Column(sa.String(2), primary_key=True)
    medida = sa.Column(sa.String(100), primary_key=True)
    segmentacao = sa.Column(sa.String(100), primary_key=True)
    detalhe = sa.Column(sa.String(200), primary_key=True)
    ano = sa.Column(sa.Integer, primary_key=True)
    valor = sa.Column(sa.Float)


class MMOComexPlantas(Base, BaseModel):
    """Table for MMO: localidade das empresas/plantas"""

    __tablename__ = "mmo_comex_planta"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    pais = sa.Column(sa.String(100))
    pais_simbolo = sa.Column(sa.String(2), primary_key=True)
    empresa = sa.Column(sa.String(100))
    localizacao = sa.Column(sa.String(100))
    latitude = sa.Column(sa.Float, nullable=False)
    longitude = sa.Column(sa.Float, nullable=False)


class MMOComexCapacidadeInstalada(Base, BaseModel):
    """Table for MMO with data about: capacidade instalada por planta e ano"""

    __tablename__ = "mmo_comex_capacidade_instalada"
    resina = sa.Column(sa.String(10), primary_key=True)
    planta = sa.Column(
        sa.Integer(),
        sa.ForeignKey("mmo_comex_planta.id"),
        nullable=False,
        primary_key=True,
    )
    ano = sa.Column(sa.Integer, primary_key=True)
    valor = sa.Column(sa.Float)


class MMOComexConsumoAparente(Base, BaseModel):
    """Table for MMO with data about: consumo aparente por pais e ano"""

    __tablename__ = "mmo_comex_consumo_aparente"
    resina = sa.Column(sa.String(10), primary_key=True)
    pais = sa.Column(sa.String(100), primary_key=True)
    pais_simbolo = sa.Column(sa.String(2), primary_key=True)
    ano = sa.Column(sa.Integer, primary_key=True)
    capacidade_efetiva = sa.Column(sa.Float)
    perc_operacional = sa.Column(sa.Float)
    producao = sa.Column(sa.Float)
    consumo_aparente = sa.Column(sa.Float)
