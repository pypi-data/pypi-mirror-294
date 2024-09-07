"""Taxref 3 specific module"""

from collections import namedtuple
from enum import Enum, auto


class Taxref3(Enum):
    """
    Taxref 3 specification.
    """
    REGNE = auto()
    PHYLUM = auto()
    CLASSE = auto()
    ORDRE = auto()
    FAMILLE = auto()
    CD_NOM = auto()
    CD_TAXSUP = auto()
    CD_REF = auto()
    RANG = auto()
    LB_NOM = auto()
    LB_AUTEUR = auto()
    NOM_COMPLET = auto()
    NOM_VERN = auto()
    NOM_VERN_ENG = auto()
    HABITAT = auto()
    FR = auto()
    GF = auto()
    MAR = auto()
    GUA = auto()
    SMSB = auto()
    SPM = auto()
    MAY = auto()
    EPA = auto()
    REU = auto()
    TAAF = auto()
    NC = auto()
    WF = auto()
    PF = auto()
    CLI = auto()


Taxref3_tuple = namedtuple('Taxref3_tuple', [v.name.lower() for v in Taxref3])


def to_taxref3_tuple(single) -> Taxref3_tuple:
    """
    Builds a namedtuple from a panda row.
    """
    return Taxref3_tuple(regne=single[Taxref3.REGNE.name],
                         phylum=single[Taxref3.PHYLUM.name],
                         classe=single[Taxref3.CLASSE.name],
                         ordre=single[Taxref3.ORDRE.name],
                         famille=single[Taxref3.FAMILLE.name],
                         cd_nom=single.name,
                         cd_taxsup=single[Taxref3.CD_TAXSUP.name],
                         cd_ref=single[Taxref3.CD_REF.name],
                         rang=single[Taxref3.RANG.name],
                         lb_nom=single[Taxref3.LB_NOM.name],
                         lb_auteur=single[Taxref3.LB_AUTEUR.name],
                         nom_complet=single[Taxref3.NOM_COMPLET.name],
                         nom_vern=single[Taxref3.NOM_VERN.name],
                         nom_vern_eng=single[Taxref3.NOM_VERN_ENG.name],
                         habitat=single[Taxref3.HABITAT.name],
                         fr=single[Taxref3.FR.name],
                         gf=single[Taxref3.GF.name],
                         mar=single[Taxref3.MAR.name],
                         gua=single[Taxref3.GUA.name],
                         smsb=single[Taxref3.SMSB.name],
                         spm=single[Taxref3.SPM.name],
                         may=single[Taxref3.MAY.name],
                         epa=single[Taxref3.EPA.name],
                         reu=single[Taxref3.REU.name],
                         taaf=single[Taxref3.TAAF.name],
                         nc=single[Taxref3.NC.name],
                         wf=single[Taxref3.WF.name],
                         pf=single[Taxref3.PF.name],
                         cli=single[Taxref3.CLI.name]
                         )
