"""Taxref 4 specific module"""

from collections import namedtuple
from enum import Enum, auto


class Taxref4(Enum):
    """
    Taxref 4 specification.
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
    APHIA_ID = auto()


Taxref4_tuple = namedtuple('Taxref4_tuple', [v.name.lower() for v in Taxref4])


def to_taxref4_tuple(single) -> Taxref4_tuple:
    """
    Builds a namedtuple from a panda row.
    """
    return Taxref4_tuple(regne=single[Taxref4.REGNE.name],
                         phylum=single[Taxref4.PHYLUM.name],
                         classe=single[Taxref4.CLASSE.name],
                         ordre=single[Taxref4.ORDRE.name],
                         famille=single[Taxref4.FAMILLE.name],
                         cd_nom=single.name,
                         cd_taxsup=single[Taxref4.CD_TAXSUP.name],
                         cd_ref=single[Taxref4.CD_REF.name],
                         rang=single[Taxref4.RANG.name],
                         lb_nom=single[Taxref4.LB_NOM.name],
                         lb_auteur=single[Taxref4.LB_AUTEUR.name],
                         nom_complet=single[Taxref4.NOM_COMPLET.name],
                         nom_valide=single[Taxref4.NOM_VALIDE.name],
                         nom_vern=single[Taxref4.NOM_VERN.name],
                         nom_vern_eng=single[Taxref4.NOM_VERN_ENG.name],
                         habitat=single[Taxref4.HABITAT.name],
                         fr=single[Taxref4.FR.name],
                         gf=single[Taxref4.GF.name],
                         mar=single[Taxref4.MAR.name],
                         gua=single[Taxref4.GUA.name],
                         sm=single[Taxref4.SM.name],
                         sb=single[Taxref4.SB.name],
                         spm=single[Taxref4.SPM.name],
                         may=single[Taxref4.MAY.name],
                         epa=single[Taxref4.EPA.name],
                         reu=single[Taxref4.REU.name],
                         taaf=single[Taxref4.TAAF.name],
                         pf=single[Taxref4.PF.name],
                         nc=single[Taxref4.NC.name],
                         wf=single[Taxref4.WF.name],
                         cli=single[Taxref4.CLI.name],
                         aphia_id=single[Taxref4.APHIA_ID.name]
                         )
