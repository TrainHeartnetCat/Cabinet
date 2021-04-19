
# coding:utf-8
import pickle
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np
import pickle
import math
def get_activation_and_reaction_energy_from_formation_energy(
        mol_to_energy_map_pred,# 物种名称到预测值的映射字典
        mol_to_energy_map_true # 物种名称到DFT计算值的映射字典
):

    # 反应对
    reaction_pair = [
        'H*_h +H*_h -> H2_g  + *_h + *_h',
        'CO_g +*_s  -> CO*_s',
        'H*_h +O*_s <->   O-H*_s     + *_h -> OH*_s  + *_h',
        'H*_h +OH*_s <->  H-OH*_s     + *_h -> H2O_g  + *_h + *_s',
        'H*_h +C*_s <->   C-H*_s     + *_h -> CH*_s  + *_h',
        'H*_h +CH*_s <->   CH-H*_s     + *_h -> CH2*_s  + *_h',
        'H*_h +CH2*_s <->  CH2-H*_s      + *_h -> CH3*_s  + *_h',
        'H*_h +CH3*_s <->  CH3-H*_s      + *_h ->CH4_g   + *_h + *_s',
        'H*_h +CO*_s <->    H-CO*_s    + *_h -> CHO*_s  + *_h',
        'H*_h +CO*_s <->   CO-H*_s      + *_h -> COH*_s  + *_h',
        'H*_h +CHO*_s <->  H-CHO*_s      + *_h -> CH2O*_s  + *_h',
        'H*_h +CHO*_s <->   CHO-H*_s     + *_h -> CHOH*_s  + *_h',
        'H*_h +CH2O*_s <->  H-CH2O*_s      + *_h -> CH3O*_s  + *_h',
        'H*_h +CH2O*_s <->   CH2O-H*_s     + *_h -> CH2OH*_s  + *_h',
        'H*_h +CO2_g <->    H-COO*_s  -> HCOO*_s ',
        'H*_h +CO2_g <->   COO-H*_s    -> COOH*_s  ',
        'H*_h +COOH*_s <->  H-COOH*_s       + *_h -> HCOOH*_s  + *_h',
        'H*_h +COOH*_s <->   H-OCOH*_s      + *_h -> HOCOH*_s  + *_h',
        'H*_h +HCOO*_s <->  H-CHOO*_s      + *_h -> CH2OO*_s  + *_h',
        'H*_h +CH2OO*_s <->  CH2OO-H*_s      + *_h -> CH2OOH*_s  + *_h',
        'H*_h +CCO*_s <->   H-CCO*_s     + *_h -> CHCO*_s  + *_h',
        'H*_h +CCO*_s <-> CC(-H)O*_s       + *_h -> CCHO*_s  + *_h',
        'H*_h +CCO*_s <->   CCO-H*_s     + *_h -> CCOH*_s  + *_h',
        'H*_h +CCHO*_s <->  H-CCHO*_s      + *_h -> CHCHO*_s  + *_h',
        'H*_h +CCHO*_s <->  CCH(-H)O*_s      + *_h -> CCH2O*_s  + *_h',
        'H*_h +CCHO*_s <->  CCHO-H*_s      + *_h -> CCHOH*_s  + *_h',
        'H*_h +CCOH*_s <->    H-CCOH*_s     + *_h -> CHCOH*_s  + *_h',
        'H*_h +CHCO*_s <->  H-CHCO*_s      + *_h -> CH2CO*_s  + *_h',
        'H*_h +CCH2O*_s <-> H-CCH2O*_s       + *_h -> CHCH2O*_s  + *_h',
        'H*_h +CCH2O*_s <-> CCH2O-H*_s       + *_h -> CCH2OH*_s  + *_h',
        'H*_h +CCHOH*_s <->  H-CCHOH*_s        + *_h -> CHCHOH*_s  + *_h',
        'H*_h +CH2CO*_s <->  H-CH2CO*_s      + *_h -> CH3CO*_s  + *_h',
        'H*_h +CH2CO*_s <->  CH2C(-H)O*_s       + *_h -> CH2CHO*_s  + *_h',
        'H*_h +CH2CO*_s <->  CH2CO-H*_s       + *_h -> CH2COH*_s  + *_h',
        'H*_h +CCH2OH*_s <->  H-CCH2OH*_s      + *_h -> CHCH2OH*_s  + *_h',
        'H*_h +CH2CHO*_s <->   H-CH2CHO*_s      + *_h -> CH3CHO*_s  + *_h',
        'H*_h +CH2CHO*_s <->   CH2CH(-H)O*_s      + *_h -> CH2CH2O*_s  + *_h',
        'H*_h +CH2CHO*_s <->    CH2CHO-H*_s     + *_h -> CH2CHOH*_s  + *_h',
        'H*_h +CH2COH*_s <-> H-CH2COH*_s       + *_h -> CH3COH*_s  + *_h',
        'H*_h +CH2CH2O*_s <-> H-CH2CH2O*_s       + *_h -> CH3CH2O*_s  + *_h',
        'H*_h +CH2CH2O*_s <->  CH2CH2O-H*_s       + *_h -> CH2CH2OH*_s  + *_h',
        'H*_h +CH2CHOH*_s <->  H-CH2CHOH*_s      + *_h -> CH3CHOH*_s  + *_h',
        'H*_h +CCOO*_s <->  H-CCOO*_s      + *_h -> CHCOO*_s  + *_h',
        'H*_h +CCOO*_s <->   CCOO-H*_s     + *_h -> CCOOH*_s  + *_h',
        'H*_h +CCOOH*_s <->  H-CCOOH*_s      + *_h -> CHCOOH*_s  + *_h',
        'H*_h +CCOOH*_s <->  CC(-H)OOH*_s      + *_h -> CCHOOH*_s  + *_h',
        'H*_h +CHCOO*_s <->  H-CHCOO*_s      + *_h -> CH2COO*_s  + *_h',
        'H*_h +OCCHO*_s <-> H-OCCHO*_s         + *_h -> HOCCHO*_s  + *_h',
        'H*_h +OCCHO*_s <->  OC(-H)CHO*_s      + *_h -> OCHCHO*_s  + *_h',
        'H*_h +OCCHO*_s <->  COCH(-H)O*_s      + *_h -> COCH2O*_s  + *_h',
        'H*_h +OCCHO*_s <->  OCCHO-H*_s      + *_h -> OCCHOH*_s  + *_h',
        'H*_h +OCCOH*_s <->   H-OCCOH*_s      + *_h -> HOCCOH*_s  + *_h',
        'H*_h +OCCOH*_s <-> OC(-H)COH*_s       + *_h -> HOCCHO*_s  + *_h',
        'H*_h +OCCOH*_s <->   OCC(-H)OH*_s      + *_h -> OCCHOH*_s  + *_h',
        'H*_h +CCHOOH*_s <->  H-CCHOOH*_s       + *_h -> CHCHOOH*_s  + *_h',
        'H*_h +CH2COO*_s <->  H-CH2COO*_s      + *_h -> CH3COO*_s  + *_h',
        'H*_h +CH2COO*_s <-> CH2COO-H*_s       + *_h -> CH2COOH*_s  + *_h',
        'H*_h +COCH2O*_s <->   H-OCCH2O*_s     + *_h -> HOCCH2O*_s  + *_h',
        'H*_h +COCH2O*_s <-> OCCH2O-H*_s       + *_h -> OCCH2OH*_s  + *_h',
        'H*_h +HOCCHO*_s <->   HOCCHO-H*_s     + *_h -> HOCCHOH*_s  + *_h',
        'H*_h +OCCHOH*_s <->  OC(-H)CHOH*_s      + *_h -> OCHCHOH*_s  + *_h',
        'H*_h +OCHCHO*_s <->   OCH(-H)CHO*_s     + *_h -> OCH2CHO*_s  + *_h',
        'H*_h +CH2CHOO*_s <->  CH2(-H)CHOO*_s      + *_h -> CH3CHOO*_s  + *_h',
        'H*_h +CH2CHOO*_s <->  CH2CHOO-H*_s      + *_h -> CH2CHOOH*_s  + *_h',
        'H*_h +CH2COOH*_s <->  H-CH2COOH*_s      + *_h -> CH3COOH*_s  + *_h',
        'H*_h +HOCCH2O*_s <->  HOCCH2O-H*_s       + *_h -> HOCCH2OH*_s  + *_h',
        'H*_h +HOCCHOH*_s <->  HOC(-H)CHOH*_s      + *_h -> HOCHCHOH*_s  + *_h',
        'H*_h +OCCH2OH*_s <->  OC(-H)CH2OH*_s      + *_h -> OCHCH2OH*_s  + *_h',
        'H*_h +OCH2CHO*_s <->  OCH2CH(-H)O*_s      + *_h -> OCH2CH2O*_s  + *_h',
        'H*_h +OCH2CHO*_s <->  OCH2CHO-H*_s       + *_h -> OCH2CHOH*_s  + *_h',
        'H*_h +CH2CHOOH*_s <->  H-CH2CHOOH*_s      + *_h -> CH3CHOOH*_s  + *_h',
        'H*_h +HOCHCHOH*_s <->   HOCH(-H)CHOH*_s      + *_h -> HOCH2CHOH*_s  + *_h',
        'H*_h +OCH2CH2O*_s <->    OCH2CH2O-H*_s     + *_h -> OCH2CH2OH*_s  + *_h',
        'H*_h +HOCH2CHOH*_s <->   HOCH2CH(-H)OH*_s     + *_h -> HOCH2CH2OH*_s  + *_h',
        'H*_h +CHCOH*_s <->    H-CHCOH*_s     + *_h -> CH2COH*_s  + *_h',
        'H*_h +CHCOH*_s <-> CHC(-H)OH*_s       + *_h -> CHCHOH*_s  + *_h',
        'H*_h +CH3O*_s <->  CH3O-H*_s      + *_h -> CH3OH_g  + *_h + *_s',
        'H*_h +CHCO*_s <->  CHCO-H*_s     + *_h -> CHCOH*_s  + *_h',
        'H*_h +COH*_s <->   H-COH*_s     + *_h -> CHOH*_s  + *_h',
        'H*_h +HCOO*_s <->    HCOO-H*_s      + *_h -> HCOOH*_s  + *_h',
        'H*_h +CH2COH*_s <->  CH2C(-H)OH      + *_h -> CH2CHOH*_s  + *_h',
        'H*_h +CH3CO*_s <->  CH3C(-H)O*_s      + *_h -> CH3CHO*_s  + *_h',
        'H*_h +CH3CO*_s <->   CH3CO-H*_s      + *_h -> CH3COH*_s  + *_h',
        'H*_h +CHCH2O*_s <->   CH(-H)CH2O*_s     + *_h -> CH2CH2O*_s  + *_h',
        'H*_h +CHCOOH*_s <->  H-CHCOOH*_s      + *_h -> CH2COOH*_s  + *_h',
        'H*_h +CHCOOH*_s <->  CHC(-H)OOH*_s      + *_h -> CHCHOOH*_s  + *_h',
        'H*_h +CHCH2O*_s <->  CHCH2O-H*_s      + *_h -> CHCH2OH*_s  + *_h',
        'H*_h +CHCHOH*_s <-> H-CHCHOH*_s       + *_h -> CH2CHOH*_s  + *_h',
        'H*_h +HOCCHO*_s <->  HOCCH(-H)O*_s      + *_h -> HOCCH2O*_s  + *_h',
        'H*_h +CHCHOH*_s <->   CHCH(-H)OH*_s      + *_h -> CHCH2OH*_s  + *_h',
        'H*_h +HOCCOH*_s <->  HOCC(-H)OH*_s       + *_h -> HOCCHOH*_s  + *_h',
        'H*_h +CHOH*_s <->   H-CHOH*_s     + *_h -> CH2OH*_s  + *_h',
        'H*_h +COCH2O*_s <->   OCCH2O-H*_s     + *_h -> OCCH2OH*_s  + *_h',
        'H*_h +OCCHOH*_s <->  H-OCCHOH*_s      + *_h -> HOCCHOH*_s  + *_h',
        'H*_h +CCHOH*_s <->   CCH(-H)OH*_s     + *_h -> CCH2OH*_s  + *_h',
        'H*_h +OCCHOH*_s <->   OCCH(-H)OH*_s     + *_h -> OCCH2OH*_s  + *_h',
        'H*_h +HCOOH*_s <->   H-CHOOH*_s     + *_h -> CH2OOH*_s  + *_h',
        'H*_h +OCHCHO*_s <->  OCHCHO-H*_s      + *_h -> OCHCHOH*_s  + *_h',
        'H*_h +HOCCHO*_s <->   OCHC(-H)OH*_s      + *_h -> OCHCHOH*_s  + *_h',
        'H*_h +CH2CHOH*_s <-> CH2CH(-H)OH*_s        + *_h -> CH2CH2OH*_s  + *_h',
        'H*_h +CH3CHO*_s <->   CH3CH(-H)O*_s      + *_h -> CH3CH2O*_s  + *_h',
        'H*_h +CH3CHO*_s <->   CH3CHO-H*_s      + *_h -> CH3CHOH*_s  + *_h',
        'H*_h +CH2COOH*_s <->   CH2C(-H)OOH*_s     + *_h -> CH2CHOOH*_s  + *_h',
        'H*_h +CH3COO*_s <->   CH3COO-H*_s     + *_h -> CH3COOH*_s  + *_h',
        'H*_h +CHCHOOH*_s <->  CH(-H)CHOOH*_s        + *_h -> CH2CHOOH*_s  + *_h',
        'H*_h +CH3COH*_s <->   CH3C(-H)OH*_s     + *_h -> CH3CHOH*_s  + *_h',
        'H*_h +CHCH2OH*_s <->  CH(-H)CH2OH*_s      + *_h -> CH2CH2OH*_s  + *_h',
        'H*_h +HOCCHOH*_s <->  HOCCH(-H)OH*_s      + *_h -> HOCCH2OH*_s  + *_h',
        'H*_h +OCCH2OH*_s <->   H-OCCH2OH*_s     + *_h -> HOCCH2OH*_s  + *_h',
        'H*_h +CH2CH2OH*_s <->  H-CH2CH2OH*_s      + *_h -> CH3CH2OH_g  + *_h + *_s',
        'H*_h +CH3CH2O*_s <->  CH3CH2O-H*_s      + *_h -> CH3CH2OH_g  + *_h + *_s',
        'H*_h +CH3CHOH*_s <->  CH3CH(-H)OH*_s      + *_h -> CH3CH2OH_g  + *_h + *_s',
        'H*_h +OCHCHOH*_s <->   H-OCHCHOH*_s     + *_h -> HOCHCHOH*_s  + *_h',
        'H*_h +OCHCHOH*_s <->  OCH(-H)CHOH*_s      + *_h -> OCH2CHOH*_s  + *_h',
        'H*_h +OCHCHOH*_s <->  OCHCH(-H)OH*_s      + *_h -> OCHCH2OH*_s  + *_h',
        'H*_h +CH2OH*_s <->   H-CH2OH*_s     + *_h -> CH3OH_g  + *_h + *_s',
        'H*_h +CH3CHOO*_s <-> CH3CHOO-H*_s       + *_h -> CH3CHOOH*_s  + *_h',
        'H*_h +CH3COOH*_s <->  CH3C(-H)OOH*_s      + *_h -> CH3CHOOH*_s  + *_h',
        'H*_h +CCOH*_s <->   CC(-H)OH*_s     + *_h -> CCHOH*_s  + *_h',
        'H*_h +CHCHO*_s <->  H-CHCHO*_s      + *_h -> CH2CHO*_s  + *_h',
        'H*_h +OCH2CHOH*_s <->  H-OCH2CHOH*_s      + *_h -> HOCH2CHOH*_s  + *_h',
        'H*_h +OCH2CHOH*_s <->  OCH2CH(-H)OH*_s      + *_h -> OCH2CH2OH*_s  + *_h',
        'H*_h +OCHCH2OH*_s <->   OCH(-H)CH2OH*_s      + *_h -> OCH2CH2OH*_s  + *_h',
        'H*_h +CHCHO*_s <->  CHCH(-H)O*_s      + *_h -> CHCH2O*_s  + *_h',
        'H*_h +OCH2CH2OH*_s <->   H-OCH2CH2OH*_s     + *_h -> HOCH2CH2OH*_s  + *_h',
        'H*_h +CHCHO*_s <->  CHCHO-H*_s      + *_h -> CHCHOH*_s  + *_h',
        'H*_h +CHCOO*_s <->  CHCOO-H*_s      + *_h -> CHCOOH*_s  + *_h',
        'CO_g +*_s  -> CO*_s',
        'CH3CHO_g +*_s  -> CH3CHO*_s',
        'O*_s +CCO*_s <->  CCO-O*_s      + *_s -> CCOO*_s  + *_s',
        'O*_s +C*_s <->  C-O*_s      + *_s -> CO*_s  + *_s',
        'O*_s +CH*_s <->  CH-O*_s      + *_s -> CHO*_s  + *_s',
        'O*_s +CH2*_s <->  CH2-O*_s       + *_s -> CH2O*_s  + *_s',
        'O*_s +CH3*_s <->  CH3-O*_s       + *_s -> CH3O*_s  + *_s',
        'O*_s +CO*_s <->  CO-O*_s      + *_s -> CO2_g  + 2*_s',
        'O*_s +CHO*_s <->  CHO-O*_s      + *_s -> HCOO*_s  + *_s',
        'O*_s +CH2O*_s <->  O-CH2O*_s      + *_s -> CH2OO*_s  + *_s',
        'O*_s +CCOH*_s <->  O-CCOH*_s      + *_s -> OCCOH*_s  + *_s',
        'O*_s +CHCO*_s <->  CHCO-O*_s      + *_s -> CHCOO*_s  + *_s',
        'O*_s +CHCO*_s <->   O-CHCO*_s      + *_s -> OCCHO*_s  + *_s',
        'O*_s +CCH2O*_s <-> O-CCH2O*_s       + *_s -> COCH2O*_s  + *_s',
        'O*_s +CCHOH*_s <->  O-CCHOH*_s       + *_s -> OCCHOH*_s  + *_s',
        'O*_s +CH2CO*_s <->  CH2CO-O*_s      + *_s -> CH2COO*_s  + *_s',
        'O*_s +CH2CO*_s <->  O-CH2CO*_s      + *_s -> COCH2O*_s  + *_s',
        'O*_s +CHCHO*_s <->  O-CHCHO*_s      + *_s -> OCHCHO*_s  + *_s',
        'O*_s +CHCOH*_s <->  O-CHCOH*_s       + *_s -> HOCCHO*_s  + *_s',
        'O*_s +CCH2OH*_s <->   O-CCH2OH*_s     + *_s -> OCCH2OH*_s  + *_s',
        'O*_s +CH2CHO*_s <->   O-CH2CHO*_s     + *_s -> OCH2CHO*_s  + *_s',
        'O*_s +CH2CHO*_s <->  CH2CHO-O*_s      + *_s -> CH2CHOO*_s  + *_s',
        'O*_s +CH2COH*_s <->   HOCCH2-O*_s     + *_s -> HOCCH2O*_s  + *_s',
        'O*_s +CH3CO*_s <->   CH3CO-O*_s     + *_s -> CH3COO*_s  + *_s',
        'O*_s +CHCH2O*_s <->   O-CHCH2O*_s      + *_s -> OCH2CHO*_s  + *_s',
        'O*_s +CHCHOH*_s <->  O-CHCHOH*_s      + *_s -> OCHCHOH*_s  + *_s',
        'O*_s +CH2CH2O*_s <->   O-CH2CH2O*_s      + *_s -> OCH2CH2O*_s  + *_s',
        'O*_s +CH2CHOH*_s <-> O-CH2CHOH*_s       + *_s -> OCH2CHOH*_s  + *_s',
        'O*_s +CH3CHO*_s <->   CH3CHO-O*_s      + *_s -> CH3CHOO*_s  + *_s',
        'O*_s +CHCH2OH*_s <->   O-CHCH2OH*_s     + *_s -> OCHCH2OH*_s  + *_s',
        'O*_s +CH2CH2OH*_s <->   O-CH2CH2OH*_s      + *_s -> OCH2CH2OH*_s  + *_s',
        'OH*_s +C*_s <-> C-OH*_s         + *_s -> COH*_s  + *_s',
        'OH*_s +CH*_s <->   CH-OH*_s      + *_s -> CHOH*_s  + *_s',
        'OH*_s +CH2*_s <->  CH2-OH*_s      + *_s -> CH2OH*_s  + *_s',
        'OH*_s +CH3*_s <->   CH3-OH*_s       + *_s -> CH3OH_g  + 2*_s',
        'OH*_s +CO*_s <->   CO-OH*_s     + *_s -> COOH*_s  + *_s',
        'OH*_s +CHO*_s <->   HCO-OH*_s     + *_s -> HCOOH*_s  + *_s',
        'OH*_s +COH*_s <->     HO-COH*_s   + *_s -> HOCOH*_s  + *_s',
        'OH*_s +CH2O*_s <->   CH2O-OH*_s      + *_s -> CH2OOH*_s  + *_s',
        'OH*_s +CCO*_s <->   CCO-OH*_s     + *_s -> CCOOH*_s  + *_s',
        'OH*_s +CCO*_s <->   OCC-OH*_s     + *_s -> OCCOH*_s  + *_s',
        'OH*_s +CCHO*_s <->  HO-CCHO*_s       + *_s -> HOCCHO*_s  + *_s',
        'OH*_s +CCHO*_s <->     CCHO-OH*_s     + *_s -> CCHOOH*_s  + *_s',
        'OH*_s +CCHO*_s <->  OCHC-OH*_s      + *_s -> HOCCHO*_s  + *_s',
        'OH*_s +CCOH*_s <->  HO-CCOH*_s      + *_s -> HOCCOH*_s  + *_s',
        'OH*_s +CHCO*_s <->  CHCO-OH*_s      + *_s -> CHCOOH*_s  + *_s',
        'OH*_s +CHCO*_s <->  OCCH-OH*_s      + *_s -> OCCHOH*_s  + *_s',
        'OH*_s +CCH2O*_s <->  HO-CCH2O*_s       + *_s -> HOCCH2O*_s  + *_s',
        'OH*_s +CCHOH*_s <->  HO-CCHOH*_s      + *_s -> HOCCHOH*_s  + *_s',
        'OH*_s +CH2CO*_s <->   CH2CO-OH*_s     + *_s -> CH2COOH*_s  + *_s',
        'OH*_s +CH2CO*_s <->  OCCH2-OH*_s      + *_s -> OCCH2OH*_s  + *_s',
        'OH*_s +CHCHO*_s <->  CHCHO-OH*_s      + *_s -> CHCHOOH*_s  + *_s',
        'OH*_s +CHCHO*_s <->  OCHCH-OH*_s      + *_s -> OCHCHOH*_s  + *_s',
        'OH*_s +CHCOH*_s <->   HOCCH-OH*_s     + *_s -> HOCCHOH*_s  + *_s',
        'OH*_s +CCH2OH*_s <-> HO-CCH2OH*_s      + *_s -> HOCCH2OH*_s  + *_s',
        'OH*_s +CH2CHO*_s <->  CH2CHO-OH*_s      + *_s -> CH2CHOOH*_s  + *_s',
        'OH*_s +CH2CHO*_s <->  OCHCH2-OH*_s      + *_s -> OCHCH2OH*_s  + *_s',
        'OH*_s +CH2COH*_s <->   HOCCH2-OH*_s     + *_s -> HOCCH2OH*_s  + *_s',
        'OH*_s +CH3CO*_s <->   CH3CO-OH*_s      + *_s -> CH3COOH*_s  + *_s',
        'OH*_s +CHCH2O*_s <->   OCH2CH-OH*_s      + *_s -> OCH2CHOH*_s  + *_s',
        'OH*_s +CHCHOH*_s <->  HOCHCH-OH*_s      + *_s -> HOCHCHOH*_s  + *_s',
        'OH*_s +CH2CH2O*_s <-> OCH2CH2-OH*_s       + *_s -> OCH2CH2OH*_s  + *_s',
        'OH*_s +CH2CHOH*_s <->   HO-CH2CHOH*_s     + *_s -> HOCH2CHOH*_s  + *_s',
        'OH*_s +CH3CHO*_s <->   CH3CHO-OH*_s     + *_s -> CH3CHOOH*_s  + *_s',
        'OH*_s +CHCH2OH*_s <->   HO-CHCH2OH*_s     + *_s -> HOCH2CHOH*_s  + *_s',
        'OH*_s +CH2CH2OH*_s <->  HOCH2CH2-OH*_s      + *_s -> HOCH2CH2OH*_s  + *_s',
        'C*_s +CO*_s <->   C-CO*_s     + *_s -> CCO*_s  + *_s',
        'C*_s +CHO*_s <->  C-CHO*_s      + *_s -> CCHO*_s  + *_s',
        'C*_s +COH*_s <->    C-COH*_s    + *_s -> CCOH*_s  + *_s',
        'C*_s +CH2O*_s <->  C-CH2O*_s       + *_s -> CCH2O*_s  + *_s',
        'C*_s +CHOH*_s <->    C-CHOH*_s     + *_s -> CCHOH*_s  + *_s',
        'C*_s +CH2OH*_s <->   C-CH2OH*_s       + *_s -> CCH2OH*_s  + *_s',
        'C*_s +CO2_g <->    C-COO*_s    -> CCOO*_s ',
        'C*_s +COOH*_s <->   C-COOH*_s     + *_s -> CCOOH*_s  + *_s',
        'C*_s +HCOOH*_s <->    C-CHOOH*_s     + *_s -> CCHOOH*_s  + *_s',
        'CH*_s +CO*_s <->   CH-CO*_s     + *_s -> CHCO*_s  + *_s',
        'CH*_s +CHO*_s <->   CH-CHO*_s     + *_s -> CHCHO*_s  + *_s',
        'CH*_s +COH*_s <->    CH-COH*_s     + *_s -> CHCOH*_s  + *_s',
        'CH*_s +CH2O*_s <->   CH-CH2O*_s       + *_s -> CHCH2O*_s  + *_s',
        'CH*_s +CHOH*_s <->   CH-CHOH*_s     + *_s -> CHCHOH*_s  + *_s',
        'CH*_s +CH2OH*_s <->  CH-CH2OH*_s       + *_s -> CHCH2OH*_s  + *_s',
        'CH*_s +CO2_g <->   CH-COO*_s     -> CHCOO*_s  ',
        'CH*_s +COOH*_s <->  CH-COOH*_s       + *_s -> CHCOOH*_s  + *_s',
        'CH*_s +HCOOH*_s <->   CH-CHOOH*_s        + *_s -> CHCHOOH*_s  + *_s',
        'CH2*_s +CO*_s <->  CH2-CO*_s       + *_s -> CH2CO*_s  + *_s',
        'CH2*_s +CHO*_s <->  CH2-CHO*_s      + *_s -> CH2CHO*_s  + *_s',
        'CH2*_s +COH*_s <->   CH2-COH*_s     + *_s -> CH2COH*_s  + *_s',
        'CH2*_s +CH2O*_s <->   CH2-CH2O*_s     + *_s -> CH2CH2O*_s  + *_s',
        'CH2*_s +CHOH*_s <->   CH2-CHOH*_s       + *_s -> CH2CHOH*_s  + *_s',
        'CH2*_s +CH2OH*_s <->  CH2-CH2OH*_s      + *_s -> CH2CH2OH*_s  + *_s',
        'CH2*_s +CO2_g <->   CH2-COO*_s     -> CH2COO*_s ',
        'CH2*_s +COOH*_s <-> CH2-COOH*_s      + *_s -> CH2COOH*_s  + *_s',
        'CH2*_s +HCOO*_s <->    CH2-CHOO*_s     + *_s -> CH2CHOO*_s  + *_s',
        'CH2*_s +HCOOH*_s <->  CH2-CHOOH*_s      + *_s -> CH2CHOOH*_s  + *_s',
        'CH3*_s +CO*_s <->     CH3-CO*_s    + *_s -> CH3CO*_s  + *_s',
        'CH3*_s +CHO*_s <->    CH3-CHO*_s      + *_s -> CH3CHO*_s  + *_s',
        'CH3*_s +COH*_s <->   CH3-COH*_s       + *_s -> CH3COH*_s  + *_s',
        'CH3*_s +CH2O*_s <->  CH3-CH2O*_s     + *_s -> CH3CH2O*_s  + *_s',
        'CH3*_s +CHOH*_s <->   CH3-CHOH*_s     + *_s -> CH3CHOH*_s  + *_s',
        'CH3*_s +COOH*_s <->  CH3-COOH*_s       + *_s -> CH3COOH*_s  + *_s',
        'CH3*_s +HCOO*_s <->   CH3-CHOO*_s     + *_s -> CH3CHOO*_s  + *_s',
        'CH3*_s +HCOOH*_s <-> CH3-CHOOH*_s       + *_s -> CH3CHOOH*_s  + *_s',
        'CO*_s +CHO*_s <->  OC-CHO*_s        + *_s -> OCCHO*_s  + *_s',
        'CO*_s +COH*_s <->   OC-COH*_s      + *_s -> OCCOH*_s  + *_s',
        'CO*_s +CH2O*_s <->  CO-CH2O*_s       + *_s -> COCH2O*_s  + *_s',
        'CO*_s +CHOH*_s <->   OC-CHOH*_s     + *_s -> OCCHOH*_s  + *_s',
        'CHO*_s +COH*_s <->   OCH-COH*_s     + *_s -> HOCCHO*_s  + *_s',
        'CHO*_s +COH*_s <->  HOC-CHO*_s      + *_s -> HOCCHO*_s  + *_s',
        'CHO*_s +CH2O*_s <->    OCH2-CHO*_s     + *_s -> OCH2CHO*_s  + *_s',
        'CHO*_s +CHOH*_s <->   OCH-CHOH*_s      + *_s -> OCHCHOH*_s  + *_s',
        'COH*_s +CHOH*_s <->   HOC-CHOH*_s       + *_s -> HOCCHOH*_s  + *_s',
        'CH2O*_s +CHOH*_s <->     OCH2-CHOH*_s     + *_s -> OCH2CHOH*_s  + *_s',
        'CH2O*_s +CH2OH*_s <-> OCH2-CH2OH*_s       + *_s -> OCH2CH2OH*_s  + *_s',
        'CHOH*_s +CH2OH*_s <->  HOCH2-CHOH*_s      + *_s -> HOCH2CHOH*_s  + *_s',
        'COH*_s+O*_s <-> O-COH*_s  + *_s  ->   COOH*_s + *_s',
        'CHOH*_s +O*_s <-> O-CHOH*_s  + *_s  -> HCOOH*_s + *_s',
        'CH2OH*_s + O*_s  <-> O-CH2OH*_s  + *_s -> CH2OOH*_s + *_s',
        'O*_s +CCHO*_s <->  O-CCHO*_s  + *_s -> OCCHO*_s  + *_s',
        'H*_h +CH3COO*_s <->   CH3C(-H)OO*_s + *_h -> CH3CHOO*_s  + *_h',
        'CH3*_s +CH2OH*_s <->  CH3-CH2OH*_s     + *_s -> CH3CH2OH_g  + *_s +*_s',
        'CO*_s +CH2OH*_s <->  OC-CH2OH*_s   + *_s -> OCCH2OH*_s  + *_s', ]



    def trans_string_to_species_list(string: str):
        species = string.split("+")
        species = [s.strip().replace("2*_s", "").replace("*_s", "").replace("H*_h", "H") for s in species]
        while "" in species: species.remove("")
        while "*_h" in species: species.remove("*_h")
        return species

    # 处理反应对，形成反应物-过渡态-产物，去除*_s等
    specie_pair = []
    for rxn in reaction_pair:
        if "_g" in rxn:
         # print("pass gas", rxn);continue
         	continue
        if "<->" in rxn:
            reactant, other = rxn.split("<->")
            transition, result = other.split("->")
            reactant = trans_string_to_species_list(reactant)
            transition = trans_string_to_species_list(transition)
            result = trans_string_to_species_list(result)
        else:
            transition = []
            reactant, result = rxn.split("->")
            reactant = trans_string_to_species_list(reactant)
            result = trans_string_to_species_list(result)
        #print(reactant, ",", transition, ",", result)
        specie_pair.append((reactant, transition, result))

    # 从反应对中得到reaction energy和activation energy
    def get_reaction_energy_and_TS_energy_pair(specie_pair,mol_to_energy_map):
        '''
        输入 energy pair，给出reaction energy作为X，以及TS energy作为Y
        :param specie_pair:
        :return:
        '''
        X = []
        Y = []
        label = []
        used_pair = []
        # print(specie_pair)
        # print(mol_to_energy_map)
        for pair in specie_pair:
            try:
                if len(pair) < 3: continue # 没有过渡态的不要
                reactant, TS, product = pair# pair中以此为例(['H', 'O'], ['O-H'], ['OH'])
                # 过渡态能量
                # 看起来用的就是formation energy
                tsE = mol_to_energy_map[TS[0]]
                # 反应物能量
                # 反应物的总能量
                rE = 0
                for r in reactant:
                    rE += mol_to_energy_map[r]
                # 产物能量
                # 反应产物总能量
                pE = 0
                for p in product:
                    pE += mol_to_energy_map[p]
                # X是reaction energy， Y是activation energy
                X.append(pE-rE)
                Y.append(tsE-rE)
                label.append(",".join(TS))
                used_pair.append(pair)
                # if tsE - rE < 0:
                #     print("活化能为负： ",pair
                #           ,",反应物分别能量: ",
                #           [mol_to_energy_map[s]for s in reactant],
                #           "反应物总能量: ",
                #           rE,
                #           "TS能量: ",
                #           tsE,
                #           ",产物分别能量: ",
                #           [mol_to_energy_map[s] for s in product],
                #           "产物总能量: ",
                #           pE)
            except KeyError:continue
        return X, Y,label,used_pair

    # 这里设置使用什么反应组合
    TARGET_REACTION = specie_pair # 所有的

    pred_reaction_energy,pred_activation_energy,pred_label,pair = get_reaction_energy_and_TS_energy_pair(
        TARGET_REACTION,mol_to_energy_map_pred)
    true_reaction_energy,true_activation_energy,true_label,pair = get_reaction_energy_and_TS_energy_pair(
        TARGET_REACTION,mol_to_energy_map_true)


    RMSE_of_activation_energy = np.sqrt(mean_squared_error(pred_activation_energy,true_activation_energy))
    error_of_activation_energy = list(np.array(pred_activation_energy) - np.array(true_activation_energy))
    # print("RMSE of activation energy: ",RMSE_of_activation_energy)
    # print('pred_activation_energy: ',pred_activation_energy)
    # print('true_activation_energy: ',true_activation_energy)

    RMSE_of_reaction_energy = np.sqrt(mean_squared_error(pred_reaction_energy, true_reaction_energy))
    error_of_reaction_energy = list(np.array(pred_reaction_energy) - np.array(true_reaction_energy))
    # print("RMSE of activation energy: ", RMSE_of_reaction_energy)# 这里应该是reaction energy
    # print("RMSE of reaction energy: ", RMSE_of_reaction_energy)# 这里应该是reaction energy
    # print('pred_reaction_energy: ',pred_reaction_energy)
    # print('true_reaction_energy: ',true_reaction_energy)


    # return RMSE_of_reaction_energy,RMSE_of_activation_energy
    return error_of_reaction_energy, error_of_activation_energy, pred_activation_energy, true_activation_energy, pred_reaction_energy, true_reaction_energy, RMSE_of_reaction_energy, RMSE_of_activation_energy
