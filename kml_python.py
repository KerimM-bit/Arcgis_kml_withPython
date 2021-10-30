#!/usr/bin/env python
# coding: utf-8

# In[1]:


import geopandas as gpd
import matplotlib.pyplot as plt
#geopandas don't support kml files so we have to add it manually
gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'


# In[2]:


data = gpd.read_file("data\Fatih.shp")

mh = ('data\districts.kml')
bina = (r'data\buildings.kml')

poly_mh = gpd.read_file(mh, driver='KML')
poly_mh.head()


# In[3]:


poly_bina = gpd.read_file(bina, driver='KML')
poly_bina.head()


# In[4]:


import pandas as pd


# In[5]:


binalar = poly_bina.copy()


# In[6]:


bina_in_mh = []

for i, poly in poly_mh.iterrows():
    bina_in_this_poly = []
    
    for j, bn in binalar.iterrows():
        if poly.geometry.contains(bn.geometry):
            bina_in_this_poly.append(bn.geometry)
            binalar = binalar.drop([j])
    bina_in_mh.append(len(bina_in_this_poly))
poly_mh['Bina sayi'] = gpd.GeoSeries(bina_in_mh)


# In[7]:


poly_mh.sort_values(by='Bina sayi', ascending=False)


# In[8]:


# We are going to choose distircts with highest number of buildings.
top_3 = poly_mh[poly_mh['Name'].isin(['AYVANSARAY', 'BALAT', 'KOCAMUSTAFAPAŞA'])]
top_3.reset_index(drop=False, inplace=True)


# In[9]:


top_3


# In[10]:


get_ipython().run_line_magic('matplotlib', 'inline')


#Plotting graph
ax = poly_mh.plot(facecolor='gray');
top_3.plot(ax=ax, facecolor='red');
poly_bina.plot(ax=ax, color='yellow', markersize=5);

plt.tight_layout()


# In[11]:


import shapely.speedups
shapely.speedups.enable()


# In[12]:


top3_mask = poly_mh.within(top_3.loc[0, 'geometry'])
top3_data = poly_mh.loc[top3_mask]


# In[13]:


ax = poly_mh.plot(facecolor='gray', figsize=(20,15))
top_3.plot(ax=ax,facecolor='red', figsize=(20,15))
top3_data.plot(ax=ax, color='gold', markersize=2, figsize=(20,15))


# In[ ]:




