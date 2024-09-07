"""Taxref 9 specific module"""

from collections import namedtuple
from enum import Enum, auto


class Taxref9(Enum):
    """
    Taxref 9 specification.
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
    CD_SUP = auto()
    CD_REF = auto()
    RANG = auto()
    LB_NOM = auto()
    LB_AUTEUR = auto()
    NOM_COMPLET = auto()
    NOM_COMPLET_HTML = auto()
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


Taxref9_tuple = namedtuple('Taxref9_tuple', [v.name.lower() for v in Taxref9])


def to_taxref9_tuple(single) -> Taxref9_tuple:
    """
    Builds a namedtuple from a panda row.
    """
    return Taxref9_tuple(regne=single[Taxref9.REGNE.name],
                         phylum=single[Taxref9.PHYLUM.name],
                         classe=single[Taxref9.CLASSE.name],
                         ordre=single[Taxref9.ORDRE.name],
                         famille=single[Taxref9.FAMILLE.name],
                         group1_inpn=single[Taxref9.GROUP1_INPN.name],
                         group2_inpn=single[Taxref9.GROUP2_INPN.name],
                         cd_nom=single.name,
                         cd_taxsup=single[Taxref9.CD_TAXSUP.name],
                         cd_sup=single[Taxref9.CD_SUP.name],
                         cd_ref=single[Taxref9.CD_REF.name],
                         rang=single[Taxref9.RANG.name],
                         lb_nom=single[Taxref9.LB_NOM.name],
                         lb_auteur=single[Taxref9.LB_AUTEUR.name],
                         nom_complet=single[Taxref9.NOM_COMPLET.name],
                         nom_complet_html=single[Taxref9.NOM_COMPLET_HTML.name],
                         nom_valide=single[Taxref9.NOM_VALIDE.name],
                         nom_vern=single[Taxref9.NOM_VERN.name],
                         nom_vern_eng=single[Taxref9.NOM_VERN_ENG.name],
                         habitat=single[Taxref9.HABITAT.name],
                         fr=single[Taxref9.FR.name],
                         gf=single[Taxref9.GF.name],
                         mar=single[Taxref9.MAR.name],
                         gua=single[Taxref9.GUA.name],
                         sm=single[Taxref9.SM.name],
                         sb=single[Taxref9.SB.name],
                         spm=single[Taxref9.SPM.name],
                         may=single[Taxref9.MAY.name],
                         epa=single[Taxref9.EPA.name],
                         reu=single[Taxref9.REU.name],
                         taaf=single[Taxref9.TAAF.name],
                         pf=single[Taxref9.PF.name],
                         nc=single[Taxref9.NC.name],
                         wf=single[Taxref9.WF.name],
                         cli=single[Taxref9.CLI.name],
                         url=single[Taxref9.URL.name]
                         )
