import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

from toolbox.colormaps import *
from toolbox.climate_and_emissions import ghg, gwp


LUs = {
    'crops' : 'Cropland',
    'pastr' : 'Pastures',
    'primf' : 'Primary Forest',
    'secdf' : 'Secondary Forest',
    'primn' : 'Primary Non-forest',
    'secdn' : 'Secondary\nNon-forest',
    'urban' : 'Urban'
}

lvst = {
    'LVST_milk'    : 'Milk' ,
    'LVST_beef'    : 'Beef' ,
    'LVST_eggs'    : 'Eggs' ,
    'LVST_pork'    : 'Pork' ,
    'LVST_poultry' : 'Poultry',
    'LVST_shoat'   : '"Shoat"',
}


def plot_landuse(gdx_data: dict, year:int, set_title: str="") -> any:
    """
    Plot the distribution of land use by land use type for a selected year. You can optionally set an alternative title.
    """
    try:
        plot_data = gdx_data['LU_AreaByUse'].set_index('year').loc[year].set_index('landuse')
        #plot_data.index = [LUs[ind] for ind in plot_data.index]
    except:
        print(f"Year {year} not found in data.")
        return

    plot_data.plot.pie(y='value', legend=False, figsize=(6,6),
                    colors=viridis[7],
                    wedgeprops = { 'linewidth' : 2, 'edgecolor' : 'white' },
                    autopct='%.0f%%',
                    pctdistance=0.85
                    )

    if set_title:
        plt.title(set_title)
    else:
        plt.title(f"Land Use in {year}")
    plt.ylabel('')
    return


def plot_secondary_forest(gdx_data: dict, year: int, set_title: str="") -> any:
    """
    Plot the distribution of secondary forest by biome for a selected year. You can optionally set an alternative title.
    """
    gdx_data['LU_Area_SecdF']['age']  = gdx_data['LU_Area_SecdF'].age.astype('category')

    try:
        plot_data = gdx_data['LU_Area_SecdF'].set_index('year').loc[year].pivot(index='age',columns='biome',values='level')
    except:
        print(f"Year {year} not found in data.")
        return

    plot_data = plot_data [[
    'TropicalHumid',
    'TropicalDry',
    'TemperateHumid',
    'TemperateDry',
    'Boreal',
    'Tundra',
    'Semiarid',
    'Desert',
    'DesertCold',
    'Unproductive'
    ]]

    colors = ["#eaf6e0", "#c2e6b4", "#9ad78a", "#71c85f", "#4fb844", "#2d9e2d", "#1f7a1f"]
    forestgreen_cmap = LinearSegmentedColormap.from_list("forestgreen_shades", colors, N=15)

    # Generate 15 colors from the custom colormap
    color_steps = [forestgreen_cmap(i/14) for i in range(15)]

    plot_data.transpose().plot(kind='bar', stacked=True, color=color_steps)
    plt.legend(bbox_to_anchor=(1.2,1), frameon=False)

    plt.ylabel('mln. km$^2$')
    plt.xlabel('Biome')
    if set_title:
        plt.title(set_title)
    else:
        plt.title(f"Secondary Forest Distribution in {year}")
    return

def add_cumulative_sum(df, groupby='process'):
    pd.set_option('future.no_silent_downcasting', True)
    
    try:
        period = df[['year']].replace(dict(zip(['2020','2030','2040','2050','2060','2070','2080','2090','2100'],[5,10,10,10,10,10,10,10,5])))
    except:
        period = df[['year']].replace(dict(zip(list(np.arange(2020,2110,10)),[5,10,10,10,10,10,10,10,5])))
    
    df['cumsum'] = (df['level'] * period['year']).astype(float)
    df['cumsum'] =  df[[groupby,'cumsum']].groupby(groupby).cumsum()
    
    return

def plot_clearing_primary_forest(gdx_data, set_title: str="") -> any:
    """
    Plot the cumulative cut-down of primary forest by biome. You can optionally set an alternative title.
    """
    add_cumulative_sum(gdx_data['LU_clear_pri'], groupby='biome')
    primf_cleared = gdx_data['LU_clear_pri'].pivot(index='year', columns='biome', values='cumsum')
    primf_cleared = primf_cleared[['TropicalHumid','TropicalDry','TemperateHumid','TemperateDry','Boreal','Tundra','Semiarid','Desert','DesertCold','Unproductive']]

    colors = [color_map.get(lbl,'gray')  for lbl in primf_cleared.columns]

    plt.stackplot(range(2020,2110,10), [primf_cleared[col] for col in primf_cleared],
                labels = primf_cleared.columns,
                colors = colors
                )
    plt.title(set_title if set_title else 'Cumulative cut-down primary forest (pristine, unmanaged forest)')
    plt.legend(bbox_to_anchor=(1.0, 1), frameon=False)
    plt.xlim(2020,2100)
    plt.ylabel('mln. km$^2$')
    return


def plot_livestock_production(gdx_data: dict) -> any:
    """
    Plot annual livestock production by product. Milk separated from other products since it is produced at a much higher volume.
    """
    plot_data = gdx_data['LVST_product_output'].pivot(index='year',columns='lvst_products',values='level')
    plot_data_no_milk = plot_data.loc[:, plot_data.columns != 'LVST_milk']
    colors = [color_map.get(lbl,'gray')  for lbl in plot_data_no_milk.columns]
    plot_data.columns = [lvst[i] for i in plot_data.columns]
    #colors = ["#9b59b6", "#e74c3c", "#34495e", "#2ecc71", "#2ecc71", "#2ecc71"]

    fig, (ax0, ax1) = plt.subplots(1, 2, dpi=150, figsize=(7,4), gridspec_kw={'width_ratios': [1, 2]})

    ax0.stackplot(plot_data.index, plot_data['Milk'], colors=[color_map['LVST_milk']])
    ax0.set_xlim(2020,2100)
    ax0.set_ylabel(f"Mt / year")
    ax0.set_xlabel("Year").set_visible(False)
    ax0.set_title("Milk Production")

    nonmilk = plot_data.loc[:, plot_data.columns != 'Milk']
    ax1.stackplot(nonmilk.index, [nonmilk[i] for i in nonmilk], colors=colors)
    ax1.set_xlim(2020,2100)
    ax1.set_xlabel("Year").set_visible(False)
    ax1.set_title("Livestock production, stacked")
    #ax0.legend(nonmilk.columns, bbox_to_anchor=(1, 0.9), frameon=False)

    ax1.legend(nonmilk.columns, bbox_to_anchor=(1, 0.9), frameon=False)
    return