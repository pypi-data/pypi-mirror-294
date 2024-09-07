"""Taxref 15 specific module"""
from collections import namedtuple
from enum import Enum, auto


class Taxref15(Enum):
    """
    Taxref 15 specification.
    """
    REGNE = auto()
    PHYLUM = auto()
    CLASSE = auto()
    ORDRE = auto()
    FAMILLE = auto()
    SOUS_FAMILLE = auto()
    TRIBU = auto()
    GROUP1_INPN = auto()
    GROUP2_INPN = auto()
    GROUP3_INPN = auto()
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


Taxref15_tuple = namedtuple('Taxref15_tuple', [v.name.lower() for v in Taxref15])


def to_taxref15_tuple(single) -> Taxref15_tuple:
    """
    Builds a namedtuple from a panda row.
    """
    return Taxref15_tuple(regne=single[Taxref15.REGNE.name],
                          phylum=single[Taxref15.PHYLUM.name],
                          classe=single[Taxref15.CLASSE.name],
                          ordre=single[Taxref15.ORDRE.name],
                          famille=single[Taxref15.FAMILLE.name],
                          sous_famille=single[Taxref15.SOUS_FAMILLE.name],
                          tribu=single[Taxref15.TRIBU.name],
                          group1_inpn=single[Taxref15.GROUP1_INPN.name],
                          group2_inpn=single[Taxref15.GROUP2_INPN.name],
                          group3_inpn=single[Taxref15.GROUP3_INPN.name],
                          cd_nom=single.name,
                          cd_taxsup=single[Taxref15.CD_TAXSUP.name],
                          cd_sup=single[Taxref15.CD_SUP.name],
                          cd_ref=single[Taxref15.CD_REF.name],
                          rang=single[Taxref15.RANG.name],
                          lb_nom=single[Taxref15.LB_NOM.name],
                          lb_auteur=single[Taxref15.LB_AUTEUR.name],
                          nom_complet=single[Taxref15.NOM_COMPLET.name],
                          nom_complet_html=single[Taxref15.NOM_COMPLET_HTML.name],
                          nom_valide=single[Taxref15.NOM_VALIDE.name],
                          nom_vern=single[Taxref15.NOM_VERN.name],
                          nom_vern_eng=single[Taxref15.NOM_VERN_ENG.name],
                          habitat=single[Taxref15.HABITAT.name],
                          fr=single[Taxref15.FR.name],
                          gf=single[Taxref15.GF.name],
                          mar=single[Taxref15.MAR.name],
                          gua=single[Taxref15.GUA.name],
                          sm=single[Taxref15.SM.name],
                          sb=single[Taxref15.SB.name],
                          spm=single[Taxref15.SPM.name],
                          may=single[Taxref15.MAY.name],
                          epa=single[Taxref15.EPA.name],
                          reu=single[Taxref15.REU.name],
                          sa=single[Taxref15.SA.name],
                          ta=single[Taxref15.TA.name],
                          taaf=single[Taxref15.TAAF.name],
                          pf=single[Taxref15.PF.name],
                          nc=single[Taxref15.NC.name],
                          wf=single[Taxref15.WF.name],
                          cli=single[Taxref15.CLI.name],
                          url=single[Taxref15.URL.name]
                          )
