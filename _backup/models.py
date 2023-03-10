from sqlmodel import SQLModel,Field
from typing import Optional


class Multipli2(SQLModel,table=True):
    
    __tablename__ = "multipli2"

    primary:Optional[int]=Field(default=None,primary_key=True)
    id:int
    anno:int
    settore:str
    EnterpriseValue_ratio_Sales :float
    EnterpriseValue_ratio_Ebitda :float
    EnterpriseValue_ratio_Ebit :float	
    Price_ratio_Earning :float
    Price_ratio_BookValue :float	
    Beta_activity :float
    Operazioniautoliquidanti :float
    Operazioni_scadenza_entro_anno :float
    Operazioni_scadenza_1_5_anni :float
    Operazioni_scadenza_oltre_5_anni :float
    Operazioni_revoca :float
    BTP15anni :float
    BTP10anni :float
    BTP5anni :float
    Premio_rischio_suggerito_perc :float
    Descrizione_settore:str



class Medie2(SQLModel,table=True):
    
    __tablename__ = "medie2"

    primary:Optional[int]=Field(default=None,primary_key=True)
    riferimento:int
    settore:str
    anno:int	
    classe:str
    Roe_perc:float
    Roi_perc:float
    Ros_perc:float
    Indice_liq_primaria:float
    Indice_margine:float
    Rapporto_indebitamento:float
    Oneri_finanziari_div_Valore_produzione_perc:float
    Durata_scorte_giorni:float
    Valore_aggiunto_per_addetto:float
    Rotazione_capitale_investito:float
    Descrizione_settore:str

class Fasce2(SQLModel,table=True):

    __tablename__ = "fasce2"

    primary:Optional[int]=Field(default=None,primary_key=True)
    anno:int
    settore:str
    riferimento:str
    Ricavi_netti: float
    Addetti: float
    Roi_perc: float
    Ebitda_su_Ricavi: float
    Ebit_su_Ricavi: float
    Rapporto_indebitamento: float
    Indice_liquidita_primaria: float
    Aziende_considerate: float
    Valore_produzione: float
    di_cui_Ricavi_netti: float
    Totale_costi_operativi: float
    Consumi: float
    Costi_servizi_godimento_bt: float
    Costo_lavoro: float
    Ammortamenti_accantonamenti: float
    Reddito_operativo_car: float
    Valore_produzione_: float
    di_cui_Ricavi_netti_: float
    Consumi_: float
    Costi_servizi_godimento_bt_: float
    Valore_aggiunto: float
    Costo_lavoro_: float
    Margine_operativo_lordo_Ebitda: float
    Ammortamenti_accantonamenti_: float
    Totale_costi_operativi_: float
    Reddito_operativo_caratteristico_Ebit: float
    Proventi_accessori: float
    Saldo_ricavi_oneri_diversi: float
    Reddito_operativo_globale: float
    Oneri_finanziari: float
    Reddito_competenza: float
    Risultato_gestione_straordinaria: float
    Reddito_pre_imposte: float
    Imposte: float
    Reddito_netto_esercizio: float
    Disponibilita_Liquide: float
    Attivita_finanziarie_non_immobilizzate: float
    Liquidita_immediate: float
    Crediti_commerciali_bte: float
    Crediti_diversi_breve_termine: float
    Liquidita_differite: float
    Rimanenze_finali: float
    Attivo_corrente : float
    Immobilizzazioni_immateriali: float
    Immobilizzazioni_materiali: float
    di_cui_Terreni_fabbricati: float
    Partecipazioni_titoli: float
    Crediti_commerciali_lungo_termine: float
    Crediti_diversi_lungotermine: float
    Immobilizzazioni_finanziarie: float
    Attivo_immobilizzato: float
    Capitale_investito: float
    Debiti_finanziari_bter: float
    Debiti_commerciali_bter: float
    Debiti_diversi_breve_termine: float
    Fondo_rischi_oneri: float
    Passivo_corrente: float
    Debiti_finanziari_lungotermine: float
    Debiti_commerciali_lungotermine: float
    Debiti_diversi_lungotermine: float
    FondoTFR: float
    Passivo_consolidato: float
    Capitale : float
    Riserve: float
    Azioni_proprie: float
    Risultato_esercizio : float
    Patrimonio_netto: float
    Passivo_e_netto : float
    Var_perc_Ricavi: float
    Var_perc_Capitale_investito: float
    Var_perc_Addetti: float
    Roe_perc: float
    Roi_perc_: float
    Roi_tipico_perc: float
    Ros_perc: float
    Redditivita_gestione_acc: float
    Tigec: float
    Ricavi_per_addetto: float
    Valore_aggiunto_per_addetto: float
    Costo_lavoro_per_addetto: float
    Rotazione_capitale_investito: float
    Rotazione_crediti_commerciali: float
    Rotazione_scorte: float
    Rotazione_debiti_commerciali: float
    Grado_leva_operativa: float
    Rapporto_corrente: float
    Indice_liquidita_primaria_: float
    Indice_margine_struttura: float
    Indice_margine_struttura_all: float
    Rapporto_indebitamento_: float
    Oneri_finanziari_su_Reddito_op_glob_perc: float
    Durata_crediti_commerciali_g: float
    Durata_scorte_g: float
    Durata_debiti_commerciali_g: float
    Durata_ciclo_finanziario_g: float
    Descrizione_settore:str

class Multipli4(SQLModel,table=True):
    
    __tablename__ = "multipli4"

    primary:Optional[int]=Field(default=None,primary_key=True)
    id:int
    anno:int
    settore:str
    EnterpriseValue_ratio_Sales :float
    EnterpriseValue_ratio_Ebitda :float
    EnterpriseValue_ratio_Ebit :float	
    Price_ratio_Earning :float
    Price_ratio_BookValue :float	
    Beta_activity :float
    Operazioniautoliquidanti :float
    Operazioni_scadenza_entro_anno :float
    Operazioni_scadenza_1_5_anni :float
    Operazioni_scadenza_oltre_5_anni :float
    Operazioni_revoca :float
    BTP15anni :float
    BTP10anni :float
    BTP5anni :float
    Premio_rischio_suggerito_perc :float
    Descrizione_settore:str


class Medie4(SQLModel,table=True):
    
    __tablename__ = "medie4"

    primary:Optional[int]=Field(default=None,primary_key=True)
    riferimento:int
    settore:str
    anno:int	
    classe:str
    Roe_perc:float
    Roi_perc:float
    Ros_perc:float
    Indice_liq_primaria:float
    Indice_margine:float
    Rapporto_indebitamento:float
    Oneri_finanziari_div_Valore_produzione_perc:float
    Durata_scorte_giorni:float
    Valore_aggiunto_per_addetto:float
    Rotazione_capitale_investito:float
    Descrizione_settore:str

class Fasce4(SQLModel,table=True):

    __tablename__ = "fasce4"

    primary:Optional[int]=Field(default=None,primary_key=True)
    anno:int
    settore:str
    riferimento:str
    Ricavi_netti: float
    Addetti: float
    Roi_perc: float
    Ebitda_su_Ricavi: float
    Ebit_su_Ricavi: float
    Rapporto_indebitamento: float
    Indice_liquidita_primaria: float
    Aziende_considerate: float
    Valore_produzione: float
    di_cui_Ricavi_netti: float
    Totale_costi_operativi: float
    Consumi: float
    Costi_servizi_godimento_bt: float
    Costo_lavoro: float
    Ammortamenti_accantonamenti: float
    Reddito_operativo_car: float
    Valore_produzione_: float
    di_cui_Ricavi_netti_: float
    Consumi_: float
    Costi_servizi_godimento_bt_: float
    Valore_aggiunto: float
    Costo_lavoro_: float
    Margine_operativo_lordo_Ebitda: float
    Ammortamenti_accantonamenti_: float
    Totale_costi_operativi_: float
    Reddito_operativo_caratteristico_Ebit: float
    Proventi_accessori: float
    Saldo_ricavi_oneri_diversi: float
    Reddito_operativo_globale: float
    Oneri_finanziari: float
    Reddito_competenza: float
    Risultato_gestione_straordinaria: float
    Reddito_pre_imposte: float
    Imposte: float
    Reddito_netto_esercizio: float
    Disponibilita_Liquide: float
    Attivita_finanziarie_non_immobilizzate: float
    Liquidita_immediate: float
    Crediti_commerciali_bte: float
    Crediti_diversi_breve_termine: float
    Liquidita_differite: float
    Rimanenze_finali: float
    Attivo_corrente : float
    Immobilizzazioni_immateriali: float
    Immobilizzazioni_materiali: float
    di_cui_Terreni_fabbricati: float
    Partecipazioni_titoli: float
    Crediti_commerciali_lungo_termine: float
    Crediti_diversi_lungotermine: float
    Immobilizzazioni_finanziarie: float
    Attivo_immobilizzato: float
    Capitale_investito: float
    Debiti_finanziari_bter: float
    Debiti_commerciali_bter: float
    Debiti_diversi_breve_termine: float
    Fondo_rischi_oneri: float
    Passivo_corrente: float
    Debiti_finanziari_lungotermine: float
    Debiti_commerciali_lungotermine: float
    Debiti_diversi_lungotermine: float
    FondoTFR: float
    Passivo_consolidato: float
    Capitale : float
    Riserve: float
    Azioni_proprie: float
    Risultato_esercizio : float
    Patrimonio_netto: float
    Passivo_e_netto : float
    Var_perc_Ricavi: float
    Var_perc_Capitale_investito: float
    Var_perc_Addetti: float
    Roe_perc: float
    Roi_perc_: float
    Roi_tipico_perc: float
    Ros_perc: float
    Redditivita_gestione_acc: float
    Tigec: float
    Ricavi_per_addetto: float
    Valore_aggiunto_per_addetto: float
    Costo_lavoro_per_addetto: float
    Rotazione_capitale_investito: float
    Rotazione_crediti_commerciali: float
    Rotazione_scorte: float
    Rotazione_debiti_commerciali: float
    Grado_leva_operativa: float
    Rapporto_corrente: float
    Indice_liquidita_primaria_: float
    Indice_margine_struttura: float
    Indice_margine_struttura_all: float
    Rapporto_indebitamento_: float
    Oneri_finanziari_su_Reddito_op_glob_perc: float
    Durata_crediti_commerciali_g: float
    Durata_scorte_g: float
    Durata_debiti_commerciali_g: float
    Durata_ciclo_finanziario_g: float
    Descrizione_settore:str







