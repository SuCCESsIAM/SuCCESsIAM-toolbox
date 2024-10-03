import gdxpds as gdx, re


def gdx_remove_emtpy(input_dict: dict) -> dict:
    """
    Remove empty dataframes from the gdx data.
    """
    keys = list(input_dict.keys())
    
    for key in keys:
        
        if input_dict[key].empty:
            del input_dict[key]
        else:
            pass
        
    return input_dict


def gdx_remove_junk_data(input_dict: dict) -> dict:
    """
    Remove the Equations, input data and other aid parameters used to produce the SuCCESs results from the gdx. 
    The function takes a dictionary as input and delivers a cleaned dictionary.
    """
    # 1 
    patterns = [re.compile("EQ_*"), re.compile("data_*")]
    
    for pattern in patterns:
        matched_keys = {key for key, value in input_dict.items() if pattern.match(key)}
        
        for key in matched_keys:
            input_dict.pop(key, None)
    
    #2
    junk_data    = 'Objective,CLIM_TOCEAN,CLIM_tocean0,path,tstep,timestep,weekk,hourr,hour_last,SpecifiedDemandProfile,DaysInDayType,Conversionls,Conversionlh,Conversionld,CommodityHasEqualityBalance,YearSplit,t,tt,TIMESLICE,l,SEASON,ls,lsls,DAYTYPE,ld,ldld,DAILYTIMEBRACKET,lh,lhlh,p,c,e,m,s,r,rr,box,boxx,boxxx,i,z'.split(',')
    for junk in junk_data:
        try:
            del input_dict[junk]
        except:
            pass
    
    return input_dict


def gdx_remove_junk_columns(input_dict: dict) -> dict:
    """
    Remove uncesessary columns from the tables of the gdx data.
    """
    
    keys         = list(input_dict.keys())
    junk_columns = ['Marginal', 'Lower', 'Upper','Scale']
    
    for key in keys:
        try:
            input_dict[key] = input_dict[key].drop(columns=junk_columns, axis=1)
        except:
            pass
        
    return input_dict



# reduce to essential success outputs
def filter_essential_outputs(input_dict: dict) -> dict:
    
    with open('toolbox/essential_outputs.txt') as f:
        essentials = f.read().splitlines()
    
    to_clear = set(input_dict.keys()).difference(essentials)
    for key in to_clear:
        del input_dict[key]
    
    return input_dict


# exported import function
def import_gdx_file(gdx_filename: str, gdx_folder_path:str = "", only_essential_outputs: bool=True) -> dict:
    """
    Imports data form a .gdx file. 
    - "gdx_filename" should state the name of the file
    - "gdx_folder_path" the path to the file folder, if not in the same directory as the script
    - "only_essential_outputs" if only the essential (i.e. main) outputs should be included in the imported dictionary.
    """
    # Add file extension to file name if not included
    if not gdx_filename.split(".")[-1] == "gdx":
        return import_gdx_file(gdx_filename=f"{gdx_filename}.gdx", gdx_path=gdx_folder_path)
    
    # Form str for path
    if not gdx_folder_path:
        path_to_gdx_file = f"{gdx_filename}"
    else:
        path_to_gdx_file = f"{gdx_folder_path}/{gdx_filename}"
    
    # Import data and return
    #try:
    print(f"Trying to read: {path_to_gdx_file}")
    response = gdx.read_gdx.to_dataframes(path_to_gdx_file, gams_dir=None)
    
    print('Cleaning up data.')
    # Remove empty dataframes from the imported data
    response = gdx_remove_emtpy(response)
    # Remove equations, inputdata and aid parameters
    response = gdx_remove_junk_data(response)
    # Remove junk columns from dataframes
    response = gdx_remove_junk_columns(response)
    # Filter such that only essential outputs remain
    if only_essential_outputs:
        response = filter_essential_outputs(response)
    
    # make all column names lowercase
    for key in response:
        columns = list(response[key].columns)
        columns_lowercase = [el.lower() for el in columns]
        response[key].rename(columns=dict(zip(columns, columns_lowercase)), inplace=True)
        response[key].rename(columns=dict(zip(['t','time','r','pool','use'], ['year','year','region','biome','landuse'])), inplace=True)
        try:
            response[key]["year"] = response[key]["year"].astype(int)
        except:
            pass
    
    # further specific cleaning-up
    # converting age class to number
    for var in ['LU_Area_SecdF','LU_clear_sec']:
        response[var]['age'] = response[var].age.astype(str).str.lstrip('age').astype(int)
    
    
    print(f"Data fetch from {gdx_filename} successful.")
    return response