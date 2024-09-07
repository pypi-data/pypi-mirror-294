"""Taxref 5 specific module"""

from collections import namedtuple
from enum import Enum, auto


class Taxref5(Enum):
    """
    Taxref 5 specification.
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
    NOM_VALIDE = auto()
    NOM_VERN = auto()
    NOM_VERN_ENG = auto()
    HABITAT = auto()
    FR = auto()
    GF = auto()
    MAR = auto()
    GUA = auto()
    SM = auto()
    SB = auto()
    SPM = auto()
    MAY = auto()
    EPA = auto()
    REU = auto()
    TAAF = auto()
    PF = auto()
    NC = auto()
    WF = auto()
    CLI = auto()
    URL = auto()


Taxref5_tuple = namedtuple('Taxref5_tuple', [v.name.lower() for v in Taxref5])


def to_taxref5_tuple(single) -> Taxref5_tuple:
    """
    Builds a namedtuple from a panda row.
    """
    return Taxref5_tuple(regne=single[Taxref5.REGNE.name],
                         phylum=single[Taxref5.PHYLUM.name],
                         classe=single[Taxref5.CLASSE.name],
                         ordre=single[Taxref5.ORDRE.name],
                         famille=single[Taxref5.FAMILLE.name],
                         cd_nom=single.name,
                         cd_taxsup=single[Taxref5.CD_TAXSUP.name],
                         cd_ref=single[Taxref5.CD_REF.name],
                         rang=single[Taxref5.RANG.name],
                         lb_nom=single[Taxref5.LB_NOM.name],
                         lb_auteur=single[Taxref5.LB_AUTEUR.name],
                         nom_complet=single[Taxref5.NOM_COMPLET.name],
                         nom_valide=single[Taxref5.NOM_VALIDE.name],
                         nom_vern=single[Taxref5.NOM_VERN.name],
                         nom_vern_eng=single[Taxref5.NOM_VERN_ENG.name],
                         habitat=single[Taxref5.HABITAT.name],
                         fr=single[Taxref5.FR.name],
                         gf=single[Taxref5.GF.name],
                         mar=single[Taxref5.MAR.name],
                         gua=single[Taxref5.GUA.name],
                         sm=single[Taxref5.SM.name],
                         sb=single[Taxref5.SB.name],
                         spm=single[Taxref5.SPM.name],
                         may=single[Taxref5.MAY.name],
                         epa=single[Taxref5.EPA.name],
                         reu=single[Taxref5.REU.name],
                         taaf=single[Taxref5.TAAF.name],
                         pf=single[Taxref5.PF.name],
                         nc=single[Taxref5.NC.name],
                         wf=single[Taxref5.WF.name],
                         cli=single[Taxref5.CLI.name],
                         url=single[Taxref5.URL.name]
                         )
