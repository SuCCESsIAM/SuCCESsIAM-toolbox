import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from toolbox.colormaps import color_map


def plot_passenger_transportation(gdx_data: dict, set_title: str="") -> any:
    """
    Plots passenger transportation by mode of transport. Optinally you can set an alternative title
    """
    passenger_transportation = gdx_data['OutputAnnualByProcess'][gdx_data['OutputAnnualByProcess'].process.str.contains('TRAN_PASS')].reset_index(drop=True).pivot(index='year', columns='process', values='level')/1000000

    # reorder
    passenger_transportation = passenger_transportation[[
    'TRAN_PASS_BusDiesel',
    'TRAN_PASS_BusBEV',
    'TRAN_PASS_CarGasoline',
    'TRAN_PASS_CarDiesel',
    'TRAN_PASS_CarHEV',
    'TRAN_PASS_CarPHEV',
    'TRAN_PASS_CarBEV',
    'TRAN_PASS_RailDiesel',
    'TRAN_PASS_RailElectric',
    'TRAN_PASS_AviationJetfuel_Int',
    'TRAN_PASS_AviationJetfuel_Dom',
    'TRAN_PASS_AviationBiofuel_Int',
    'TRAN_PASS_AviationBiofuel_Dom'
    ]]

    labels = [el[10:] for el in passenger_transportation.columns]
    colors = [color_map.get(lbl,'gray')  for lbl in labels]

    plt.stackplot(range(2020,2110,10), [passenger_transportation[col] for col in passenger_transportation],
                labels = labels,
                colors = colors
                )
    plt.title(set_title if set_title else 'Annual Passenger Transportation')
    plt.legend(bbox_to_anchor=(1.0, 1), frameon=False)
    plt.xlim(2020,2100)
    plt.ylabel('10$^{12}$ passenger-km')
    return


def plot_freight_transportation(gdx_data: dict, set_title: str=""):
    """
    Plots freight transportation by mode of transport. Optinally you can set an alternative title. Tonne-km refers to tonnes transported over a distance of 1 km.
    """
    freight_transportation   = gdx_data['OutputAnnualByProcess'][gdx_data['OutputAnnualByProcess'].process.str.contains('TRAN_FRGT')].reset_index(drop=True).pivot(index='year', columns='process', values='level')/1000000

    # reorder
    freight_transportation = freight_transportation[[
    'TRAN_FRGT_ShipsHFO',
    'TRAN_FRGT_ShipsMDO',
    'TRAN_FRGT_ShipsLNG',
    'TRAN_FRGT_ShipsBio',
    'TRAN_FRGT_RailDiesel',
    'TRAN_FRGT_RailElectric',
    'TRAN_FRGT_TruckDiesel',
    'TRAN_FRGT_TruckBEV',
    'TRAN_FRGT_VanDiesel',
    'TRAN_FRGT_VanBEV'
    ]]

    labels = [el[10:] for el in freight_transportation.columns]
    colors = [color_map.get(lbl,'gray')  for lbl in labels]

    plt.stackplot(range(2020,2110,10), [freight_transportation[col] for col in freight_transportation],
                labels = labels,
                colors = colors
                )
    plt.title(set_title if set_title else 'Annual Freight Transportation')
    plt.legend(bbox_to_anchor=(1.0, 1), frameon=False)
    plt.xlim(2020,2100)
    plt.ylabel('10$^{12}$ tonne-km')
    return