# # -*- coding: utf-8 -*-

# =============================================================================
# Modules - Libraries
# =============================================================================

from pathlib import Path
import zipfile
import tempfile
import pandas as pd
import numpy as np
from arcgis import GIS
from arcgis.features import FeatureLayerCollection
from arcgis import features as fs
import logging


##
#############################################################
# FUNCTIONS
#############################################################
def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """Set up a simple logger -
    https://engineeringfordatascience.com/posts/python_logging/"""
    
    log = logging.getLogger(__name__)
    console = logging.StreamHandler()
    log.addHandler(console)
    log.setLevel(level)
    return log

def df_to_temp_csv_zip(df: pd.DataFrame, base_name="data"):
    """
    Write a pandas DataFrame to a temporary CSV file, zip it, 
    and return (zip_path, tmpdir) so you can use it and clean up later.
    """
    tmpdir = tempfile.TemporaryDirectory()
    tmp_path = Path(tmpdir.name)

    csv_path = tmp_path / f"{base_name}.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8")

    # Uncomment below if zip file is wanted
    # zip_path = tmp_path / f"{base_name}.zip"
    # with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    #     zf.write(csv_path, arcname=csv_path.name)

    return csv_path, tmpdir

def wfs_agol(agol_user, agol_pass, wck_act_data, item_id):
    """This function updates the AGOL feature layer for the Activation
    data using the values from the WCK API

    Args:
        agol_user (str): AGOL user credentials
        agol_pass (str): AGOL user password
        wck_act_data (pd.dataframe): pandas dataframe with WCK activation data
    """
    
    # Connecting to AGOL
    gis = GIS(r'https://wckorg.maps.arcgis.com', 
            username = agol_user, 
            password = agol_pass)
    log.info(f"\n --- \nConnected to: \n"
             f"{gis.properties.portalHostname} as \n"
             f"{gis.users.me.username}\n --- \n")
    
    # Get the item by ID - Will need to hide this
    item = gis.content.get(
        item_id # this is the csv file
        )
    
    # Set the layer needed. It is only one layer
    flayer = item.layers[-1]
    flc = FeatureLayerCollection.fromitem(item)

    # Find the original data item (the file the service was published from)
    # This will ensuere the csv file has the correct name which is need it to overwrite
    data_items = item.related_items("Service2Data")  # returns [Item]
    if not data_items:
        raise RuntimeError("No source data item found (Service2Data).")
    
    # Make sure the right name is used. THe name comes from AGOL
    src_agol_name = data_items[0]
    src_agol_name = src_agol_name.title.removesuffix(".csv")

    log.info(f"\n --- \n The current number of records in AGOL is:"
             f"{flayer.query(return_count_only=True)}\n --- \n")
    
    # BigQuery response to dataframe to ger rid of records without coordiantes
    # (drop rows missing coords, optional)    
    
    df2 = wck_act_data.dropna(subset=["latitude", "longitude"]).copy()
    
    csv_path, tmpdir = df_to_temp_csv_zip(df2, base_name=src_agol_name)
    
    # Ovewrite data
    # Helpful assertions before calling overwrite:
    if csv_path.exists():
        
        flc.manager.overwrite(str(csv_path))
        
        log.info(f"\n --- \n "
             f"{flc.manager.overwrite(str(csv_path))}\n --- \n")
    else:
        "n/a"
    
    # When done clear temp dir:
    tmpdir.cleanup() 
    
    
# Set log level to info
log = setup_logging()