"""Taxref 8 specific module"""

from collections import namedtuple
from enum import Enum, auto


class Taxref8(Enum):
    """
    Taxref 8 specification.
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


Taxref8_tuple = namedtuple('Taxref8_tuple', [v.name.lower() for v in Taxref8])


def to_taxref8_tuple(single) -> Taxref8_tuple:
    """
    Builds a namedtuple from a panda row.
    """
    return Taxref8_tuple(regne=single[Taxref8.REGNE.name],
                         phylum=single[Taxref8.PHYLUM.name],
                         classe=single[Taxref8.CLASSE.name],
                         ordre=single[Taxref8.ORDRE.name],
                         famille=single[Taxref8.FAMILLE.name],
                         group1_inpn=single[Taxref8.GROUP1_INPN.name],
                         group2_inpn=single[Taxref8.GROUP2_INPN.name],
                         cd_nom=single.name,
                         cd_taxsup=single[Taxref8.CD_TAXSUP.name],
                         cd_ref=single[Taxref8.CD_REF.name],
                         rang=single[Taxref8.RANG.name],
                         lb_nom=single[Taxref8.LB_NOM.name],
                         lb_auteur=single[Taxref8.LB_AUTEUR.name],
                         nom_complet=single[Taxref8.NOM_COMPLET.name],
                         nom_complet_html=single[Taxref8.NOM_COMPLET_HTML.name],
                         nom_valide=single[Taxref8.NOM_VALIDE.name],
                         nom_vern=single[Taxref8.NOM_VERN.name],
                         nom_vern_eng=single[Taxref8.NOM_VERN_ENG.name],
                         habitat=single[Taxref8.HABITAT.name],
                         fr=single[Taxref8.FR.name],
                         gf=single[Taxref8.GF.name],
                         mar=single[Taxref8.MAR.name],
                         gua=single[Taxref8.GUA.name],
                         sm=single[Taxref8.SM.name],
                         sb=single[Taxref8.SB.name],
                         spm=single[Taxref8.SPM.name],
                         may=single[Taxref8.MAY.name],
                         epa=single[Taxref8.EPA.name],
                         reu=single[Taxref8.REU.name],
                         taaf=single[Taxref8.TAAF.name],
                         pf=single[Taxref8.PF.name],
                         nc=single[Taxref8.NC.name],
                         wf=single[Taxref8.WF.name],
                         cli=single[Taxref8.CLI.name],
                         url=single[Taxref8.URL.name]
                         )
