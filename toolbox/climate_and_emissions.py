import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from toolbox.colormaps import *

ghg = ['CO2', 'CH4', 'N2O']
gwp = [1, 28, 265]

def plot_deltaT(gdx_data: dict, set_title: str='') -> any:
    """
    Plot the global mean temperature change over the decade. You can optionally define an alternative title.
    """
    clim_deltaT = gdx_data["CLIM_DeltaT"][["year", "level"]]
    clim_deltaT.index = clim_deltaT["year"]
    clim_deltaT = clim_deltaT["level"]
    sns.lineplot(data=clim_deltaT, linewidth=3)
    plt.ylabel('ΔT (°C)')
    plt.xlabel([""]).set_visible(False)
    plt.xlim(2020,2100)
    plt.legend([""]).set_visible(False)
    plt.title(set_title if set_title else 'Global Mean Temperature Change')
    return


def plot_emissions(gdx_data: dict) -> any:
    """
    Plot all emissions in the gdx data. CO2 emissions are split into:
    - Fossil fuels and industry (FFI)
    - Managed lands and deforestation (LU)
    - Natural lands (excluding deforestation) (nat)
    """
    
    try:
        # if entire data dictionary is passed, 
        df = gdx_data['EmissionAnnual'].copy()
    except:
        df = gdx_data.copy()
    
    df = df.pivot(index='year', columns='emission', values='level')
    df['CO2sum'] = df.filter(regex='CO2', axis=1).sum(axis=1)

    
    # Plot
    fig,(ax0, ax1, ax2) = plt.subplots(3,1, dpi=150, figsize=(7,10))

    # CO2
    plot_data = df.filter(regex="CO2", axis=1)
    ax0.plot(plot_data/1000, linewidth=2)
    ax0.plot(pd.DataFrame([0]*len(plot_data), index=plot_data.index), linewidth=1, linestyle="--", color="black")
    ax0.set_xlim(2020,2100)
    ax0.set_title("CO$_2$ net emissions")
    ax0.legend(plot_data.columns, frameon=False)
    ax0.set_ylabel("Gt CO$_2$ / year")
    ax0.set_xlabel("Year").set_visible(False)

    # CH4
    plot_data = df.filter(regex="CH4", axis=1)
    sns.lineplot(plot_data, ax=ax1, linewidth=3)
    ax1.set_xlim(2020,2100)
    ax1.set_title("CH$_4$ net emissions")
    ax1.legend(frameon=False).set_visible(False)
    ax1.set_ylabel("Mt CH$_4$ / year")
    ax1.set_xlabel("Year").set_visible(False)


    # N2O
    plot_data = df.filter(regex="N2O", axis=1)
    sns.lineplot(plot_data, ax=ax2, linewidth=3)
    ax2.set_xlim(2020,2100)
    ax2.set_title("N$_2$O net emissions")
    ax2.legend(frameon=False).set_visible(False)
    ax2.set_ylabel("Mt N$_2$O / year")
    ax2.set_xlabel("Year").set_visible(False)
    
    fig.tight_layout()
    return


def calculate_total_netemissions_co2eq(gdx_data: dict, unit : str='Gt') -> any:
    """
    Calculates total CO2eq emissions from the gdx data. Alternatively you can scale the presented output by passing a unit between kg and Tt.
    """
    try:
        # if entire data dictionary is passed, 
        df = gdx_data['EmissionAnnual'].copy()
    except:
        df = gdx_data.copy()
        
    # scale it 
    for u,s in zip(['kg', 't', 'kt', 'mt', 'gt', 'tt'],[10**-9, 10**-6, 10**-3, 1, 10**3, 10**6]):
        if unit.lower() == u:
            scale=s
    
    df = df.pivot(index='year', columns='emission', values='level') / scale
    df['CO2sum'] = df.filter(regex='CO2', axis=1).sum(axis=1)
    
    result =  gwp[0] * df['CO2sum'] +\
              gwp[1] * df['CH4'] +\
              gwp[2] * df['N2O']
                 
                 
    return result

def plot_total_net_emissions_co2eq(gdx_data, set_title=None):
    """
    Plot the total net emissions in CO2eq. Optionally you can define an alternative title.
    """
    data = calculate_total_netemissions_co2eq(gdx_data['EmissionAnnual'])
    zeros = pd.DataFrame([0]*len(data), index=data.index)
    #zeros["zero"] = [0 for i in range(len(data))]
    plt.plot(data, linewidth=2)
    plt.plot(zeros, linewidth=1, linestyle="--", color="black")
    plt.ylabel('Gt CO$_2$-eq / year')
    plt.xlabel([""]).set_visible(False)
    plt.xlim(2020,2100)
    plt.legend([""]).set_visible(False)
    plt.title(set_title if set_title else 'Total net emissions (GtCO2eq)')
    return