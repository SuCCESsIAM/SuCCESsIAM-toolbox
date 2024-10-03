import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from toolbox.colormaps import *



def plot_electricity_production(gdx_data: dict, joules: bool=False) -> any:
    """
    Plot electricity production by source in a stackplot.
    """
    # define electricity generation list
    elec_gen_list = ['ELEC_Coal', 'ELEC_OilL', 'ELEC_GasT',
                    'ELEC_BioM', 'ELEC_Wste', 'ELEC_Fiss', 'ELEC_Hydr', 'ELEC_Wnd1',
                    'ELEC_SPV1', 'ELEC_BCCS', 'ELEC_CCCS', 'ELEC_GCCS']
    
    # structure data for plotting
    elec_gen = gdx_data['OutputAnnualByProcess'][gdx_data['OutputAnnualByProcess'].process.isin(elec_gen_list)]
    elec_gen = elec_gen[elec_gen.commodity == 'ELECGen']
    elec_gen.loc[:,'level'] = round(elec_gen.loc[:,'level'] /1000)
    elec_gen_grouped = elec_gen.groupby(["process", "year"])['level'].sum().unstack(level=0)
    elec_colors = [color_map[EL] for EL in elec_gen_grouped.columns]

    # plot stacked
    if joules:
        plt.stackplot(elec_gen_grouped.index,[elec_gen_grouped[col] for col in elec_gen_grouped.columns], labels=list([ i.split("ELEC_")[1] for i in elec_gen_grouped.columns]), colors=elec_colors )
        plt.ylabel('EJ / year')
    else:
        EJ_to_PWh = 0.27777777777778
        plt.stackplot(elec_gen_grouped.index,[elec_gen_grouped[col]*EJ_to_PWh for col in elec_gen_grouped.columns], labels=list([ i.split("ELEC_")[1] for i in elec_gen_grouped.columns]), colors=elec_colors )
        plt.ylabel('PWh / year')
    plt.title('Annual Electricity Generation')
    plt.legend(bbox_to_anchor=(1,1), frameon=False)
    plt.xlim(2020,2100)
    return



def print_all_commodities(gdx_data):
    "Lists all commodities produced annually"
    print("All commodities:")
    print(*np.sort(gdx_data["OutputAnnual"]["commodity"].unique()),sep=", ")
    return 



def plot_commodity_production(gdx_data: dict, commodities: list, stacked:bool = False, cumulative: bool = False, unit:str = "[unit]", scale_by:int = 1, set_title: str="") -> any:
    """
    Plot a commodity or commodities from the gdx data. You can optionally
    - make the plot stacked by setting "stacked" to True. Plot default is lineplot.
    - make the plot cumulative by setting "cumulative" to True.
    - specity "unit" for your plot (in most cases Mt)
    - specify "scale_by" to scale the y-axis by a factor (eg. 1000 would make Mt into Gt)
    - "set_title" either to False to hide the title or to your title.
    """
    if not set(commodities).issubset(gdx_data["OutputAnnual"]["commodity"].unique()):
        print("One or more commodities not found in the data. Check spelling and availability.")
        return False
    commodity_df = gdx_data["OutputAnnual"].groupby(["commodity", "year"])['level'].sum().unstack(level=0)
    commodity_df=commodity_df[commodities]/scale_by
    if stacked:
        if cumulative:
            multipliers = [5,10,10,10,10,10,10,10,5]
            if len(multipliers) != len(commodity_df.index):
                print("Number of multipliers does not match the number of years in the data.")
                return False
            cumulative_commodity_df = pd.DataFrame()
            for column in commodity_df.columns:
                column_data = commodity_df[column] * multipliers
                cumulative_commodity_df[column] = column_data.cumsum()
            commodity_df = cumulative_commodity_df
            plt.stackplot(commodity_df.index,[commodity_df[col] for col in commodity_df.columns], labels=list(commodity_df.columns) )
            plt.legend(bbox_to_anchor=(1,1), frameon=False)
        else:
            plt.stackplot(commodity_df.index,[commodity_df[col] for col in commodity_df.columns], labels=list(commodity_df.columns) )
            plt.legend(bbox_to_anchor=(1,1), frameon=False)
    else:
        if cumulative:
            multipliers = [5,10,10,10,10,10,10,10,5]
            if len(multipliers) != len(commodity_df.index):
                print("Number of multipliers does not match the number of years in the data.")
                return False
            cumulative_commodity_df = pd.DataFrame()
            for column in commodity_df.columns:
                column_data = commodity_df[column] * multipliers
                cumulative_commodity_df[column] = column_data.cumsum()
            commodity_df = cumulative_commodity_df
            sns.lineplot(data=commodity_df)
        else:
            sns.lineplot(data=commodity_df)
    plt.ylabel(f'Production ({unit}/year)')
    plt.xlabel("").set_visible(False)
    plt.xlim(2020,2100)
    # setting title
    if set_title:
        plt.title(set_title)
    else:
        if len(commodities) > 1:
            plt.title(f"Production of commodities {"stacked" if stacked else ""} {"cumulative" if cumulative else ""}")
        else:
            plt.title(f"Production of {commodities[0]} {"stacked" if stacked else ""} {"cumulative" if cumulative else ""}")
            plt.legend(bbox_to_anchor=(1,1), frameon=False).remove()
    return



def plot_commodity_by_process(gdx_data: dict, commodity: str, unit:str = "[unit]", scale_by:int = 1, set_title: str="") -> any:
    """
    Stacked plot of processes producing a commodity from the gdx data. You can optionally
    - specity "unit" for your plot (in most cases Mt)
    - specify "scale_by" to scale the y-axis by a factor (eg. 1000 would make Mt into Gt)
    - "set_title" either to False to hide the title or to your title.
    """
    #commodity = "CRUD"
    #scale_by = 1
    all_outputs = gdx_data["OutputAnnualByProcess"]
    commodity_data = all_outputs.loc[all_outputs["commodity"] == commodity]
    if len(commodity_data) < 1:
        print(f"No {commodity} found in commodity list.")
        return False
    commodity_data_grouped = commodity_data.groupby(["process", "year"])['level'].sum().unstack(level=0)
    commodity_data_grouped=commodity_data_grouped/scale_by
    commodity_data_grouped
    plt.stackplot(commodity_data_grouped.index,[commodity_data_grouped[col] for col in commodity_data_grouped.columns], labels=list(commodity_data_grouped.columns) )
    plt.legend(bbox_to_anchor=(1,1), frameon=False)
    plt.ylabel(f'Production ({unit}/year)')
    plt.xlabel("").set_visible(False)
    plt.xlim(2020,2100)
    # setting title
    if set_title:
        plt.title(set_title)
    else:
        plt.title(f"{commodity} production by process")
    return

