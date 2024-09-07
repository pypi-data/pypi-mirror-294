"""Taxref 10 specific module"""

from collections import namedtuple
from enum import Enum, auto


class Taxref10(Enum):
    """
    Taxref 10 specification.
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
    SA = auto()
    TA = auto()
    TAAF = auto()
    PF = auto()
    NC = auto()
    WF = auto()
    CLI = auto()
    URL = auto()


Taxref10_tuple = namedtuple('Taxref10_tuple', [v.name.lower() for v in Taxref10])


def to_taxref10_tuple(single) -> Taxref10_tuple:
    """
    Builds a namedtuple from a panda row.
    """
    return Taxref10_tuple(regne=single[Taxref10.REGNE.name],
                          phylum=single[Taxref10.PHYLUM.name],
                          classe=single[Taxref10.CLASSE.name],
                          ordre=single[Taxref10.ORDRE.name],
                          famille=single[Taxref10.FAMILLE.name],
                          group1_inpn=single[Taxref10.GROUP1_INPN.name],
                          group2_inpn=single[Taxref10.GROUP2_INPN.name],
                          cd_nom=single.name,
                          cd_taxsup=single[Taxref10.CD_TAXSUP.name],
                          cd_sup=single[Taxref10.CD_SUP.name],
                          cd_ref=single[Taxref10.CD_REF.name],
                          rang=single[Taxref10.RANG.name],
                          lb_nom=single[Taxref10.LB_NOM.name],
                          lb_auteur=single[Taxref10.LB_AUTEUR.name],
                          nom_complet=single[Taxref10.NOM_COMPLET.name],
                          nom_complet_html=single[Taxref10.NOM_COMPLET_HTML.name],
                          nom_valide=single[Taxref10.NOM_VALIDE.name],
                          nom_vern=single[Taxref10.NOM_VERN.name],
                          nom_vern_eng=single[Taxref10.NOM_VERN_ENG.name],
                          habitat=single[Taxref10.HABITAT.name],
                          fr=single[Taxref10.FR.name],
                          gf=single[Taxref10.GF.name],
                          mar=single[Taxref10.MAR.name],
                          gua=single[Taxref10.GUA.name],
                          sm=single[Taxref10.SM.name],
                          sb=single[Taxref10.SB.name],
                          spm=single[Taxref10.SPM.name],
                          may=single[Taxref10.MAY.name],
                          epa=single[Taxref10.EPA.name],
                          reu=single[Taxref10.REU.name],
                          sa=single[Taxref10.SA.name],
                          ta=single[Taxref10.TA.name],
                          taaf=single[Taxref10.TAAF.name],
                          pf=single[Taxref10.PF.name],
                          nc=single[Taxref10.NC.name],
                          wf=single[Taxref10.WF.name],
                          cli=single[Taxref10.CLI.name],
                          url=single[Taxref10.URL.name]
                          )
