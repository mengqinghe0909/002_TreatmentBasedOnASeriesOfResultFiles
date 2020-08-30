import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

filenameslist = os.listdir()
surfacefiles = []
listnames = []
data3 = []

'''
由于只有一列的dataframe会降维，所以必须传两列及以上的dataframe才可以正常合并
'''
def main():

    for items in filenameslist:
        if items.find('surface_flow') != -1:
            surfacefiles.append(items)
            data0 = ProcessFile(items)

            if len(surfacefiles) == 1:
                df = data0
            else:
                df.loc[:,str(len(surfacefiles))] = data0.loc[:, 'drag']
    x = df['theta'].values
    friction_df = df.drop(['theta'], axis=1)
    y = friction_df.mean(1).values

    plt.style.use('ggplot')
    plt.plot(x, y)
    plt.savefig('friction01plus.png')
    plt.close('all')

def ProcessFile(items):
    with open(items) as filename:
        data = pd.read_csv(filename)
        data1 = data.sort_values(by='x').loc[(data['z'] <= 0.0109)&(data['z'] >= 0.01)&(data['y'] >= 0), ['x','Skin_Friction_Coefficient_x',\
                                                                             'Skin_Friction_Coefficient_y']]
        data2 = ProcessTransition(data1)
        return data2

def ProcessTransition(data1):
    data1['theta'] = data1['x'].map(lambda x: math.acos(x/(-0.05))*(180/math.pi))
    #data1['drag'] = data1.apply(lambda x: -1*x['Skin_Friction_Coefficient_x']*math.sin(x['theta'])\
    #                            -x['Skin_Friction_Coefficient_y']*math.cos(x['theta']), axis=1)
    data1['drag'] = data1.apply(lambda x: x['Skin_Friction_Coefficient_x']+x['Skin_Friction_Coefficient_y'], axis=1)


    return data1[['theta', 'drag']]


if __name__ == '__main__':
    main()