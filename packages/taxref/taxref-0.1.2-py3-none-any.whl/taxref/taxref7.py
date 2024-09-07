"""Taxref 7 specific module"""

from collections import namedtuple
from enum import Enum, auto


class Taxref7(Enum):
    """
    Taxref 7 specification.
    """
    REGNE = auto()
    PHYLUM = auto()
    CLASSE = auto()
    ORDRE = auto()
    FAMILLE = auto()
    GROUP1_INPN = auto()
    GROUP2_INPN = auto()
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


Taxref7_tuple = namedtuple('Taxref7_tuple', [v.name.lower() for v in Taxref7])


def to_taxref7_tuple(single) -> Taxref7_tuple:
    """
    Builds a namedtuple from a panda row.
    """
    return Taxref7_tuple(regne=single[Taxref7.REGNE.name],
                         phylum=single[Taxref7.PHYLUM.name],
                         classe=single[Taxref7.CLASSE.name],
                         ordre=single[Taxref7.ORDRE.name],
                         famille=single[Taxref7.FAMILLE.name],
                         group1_inpn=single[Taxref7.GROUP1_INPN.name],
                         group2_inpn=single[Taxref7.GROUP2_INPN.name],
                         cd_nom=single.name,
                         cd_taxsup=single[Taxref7.CD_TAXSUP.name],
                         cd_ref=single[Taxref7.CD_REF.name],
                         rang=single[Taxref7.RANG.name],
                         lb_nom=single[Taxref7.LB_NOM.name],
                         lb_auteur=single[Taxref7.LB_AUTEUR.name],
                         nom_complet=single[Taxref7.NOM_COMPLET.name],
                         nom_valide=single[Taxref7.NOM_VALIDE.name],
                         nom_vern=single[Taxref7.NOM_VERN.name],
                         nom_vern_eng=single[Taxref7.NOM_VERN_ENG.name],
                         habitat=single[Taxref7.HABITAT.name],
                         fr=single[Taxref7.FR.name],
                         gf=single[Taxref7.GF.name],
                         mar=single[Taxref7.MAR.name],
                         gua=single[Taxref7.GUA.name],
                         sm=single[Taxref7.SM.name],
                         sb=single[Taxref7.SB.name],
                         spm=single[Taxref7.SPM.name],
                         may=single[Taxref7.MAY.name],
                         epa=single[Taxref7.EPA.name],
                         reu=single[Taxref7.REU.name],
                         taaf=single[Taxref7.TAAF.name],
                         pf=single[Taxref7.PF.name],
                         nc=single[Taxref7.NC.name],
                         wf=single[Taxref7.WF.name],
                         cli=single[Taxref7.CLI.name],
                         url=single[Taxref7.URL.name]
                         )
