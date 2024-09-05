# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 10:19:06 2020

@author: n.deruiter
"""

import os.path
import glob
import pandas as pd
import numpy as np
import OrcFxAPI as orc
import yaml
import itertools

flatten = itertools.chain.from_iterable

if __name__ == '__main__':    
    #Input
    outputDir = 'Iteration_0'              # Folder name of simulation files
    criteriaFile = 'Criteria.xlsx'                          # Excel file containing criteria
    excelFile = 'Iteration_0_results.xlsx'                   # Output Excel file name of results
    percentiles = 'meanstd'

    criteria = pd.read_excel(criteriaFile, header=3, skiprows=[4]).drop(columns=['name','cell','cell.1']).rename(columns={'name.1': 'name'})
    
    varName = [None]*len(criteria)
    
    for i in range(len(criteria)):
        varName[i] = ''.join([criteria.Label[i],' (',criteria.Command[i],')'])
    



def ExtractSingleCaseResults(fileName, criteria, varName):
# This function extracts the results for a single simulation file
    
    if isinstance(fileName, str): 
        model = orc.Model(threadCount=1)
        print('Processing', fileName)
        model.LoadSimulation(fileName)
    else:
        model = fileName
 

    # Create empty dictionary
    results = {}  
    results['Criteria met'] = True
    results['Exceeded criteria'] = ''
    
    # Get enviroment data
    env = model.environment
    
    objects = [a.name for a in model.objects]
    
    if not str(model.state) == 'InStaticState':  
        
        results['Significant wave height [m]'] = env.WaveHs
        results['Wave spectrum peak period [s]'] = env.WaveTp
        results['Wave direction [deg]'] = env.WaveDirection
        results['Current velocity [m/s]'] = env.RefCurrentSpeed
        results['Current direction [deg]'] = env.RefCurrentDirection
        results['Seed [-]'] = env.WaveSeed
        
    else:
        results['Significant wave height [m]'] = '-'
        results['Wave spectrum peak period [s]'] = '-'
        results['Wave direction [deg]'] = '-'
        results['Current velocity [m/s]'] = env.RefCurrentSpeed
        results['Current direction [deg]'] = env.RefCurrentDirection
        results['Seed [-]'] = '-'        
        
        
    modelEndTime = model.simulationTimeStatus.CurrentTime
           
    
    if yaml.safe_load(model.general.comments) is not None:
        results.update(yaml.safe_load(model.general.comments))   
    
    
    for i in range(len(criteria)):
        
        if criteria.period[i] == 'Whole simulation':
            period = orc.pnWholeSimulation
        elif 'to' in str(criteria.period[i]):
            period = orc.SpecifiedPeriod(float(criteria.period[i].split()[0]),float(criteria.period[i].split()[2]))
        elif criteria['period'][i] == 'Static state' or np.isnan(float(criteria['period'][i])): 
            period = orc.pnStaticState            
        elif isinstance(criteria.period[i],int) or isinstance(criteria.period[i],np.integer) or isinstance(criteria.period[i],float):
            period = int(criteria.period[i])
        elif criteria.period[i] == 'End':
            period = orc.SpecifiedPeriod(0,modelEndTime)
        
        if not criteria.name[i] in objects:
            results[varName[i]] = np.nan
        
        elif criteria.Command[i] == 'Get data':
            results[varName[i]] = eval(''.join(['model[criteria.name[i]].',criteria.Variable[i]]))
        
        elif criteria.Command[i] == 'Range graph min':
            if criteria['period'][i] == 'Static state' or np.isnan(float(criteria['period'][i])): 
                results[varName[i]] = min(model[criteria.name[i]].RangeGraph(criteria.Variable[i],period=period,arclengthRange=orc.arSpecifiedSections(criteria.data[i], criteria.data[i])).Mean)
            else:
                results[varName[i]] = min(model[criteria.name[i]].RangeGraph(criteria.Variable[i],period=period,arclengthRange=orc.arSpecifiedSections(criteria.data[i], criteria.data[i])).Min)

        elif criteria.Command[i] == 'Static result':        
            if pd.isnull(criteria.data)[i]:
                results[varName[i]] = model[criteria.name[i]].StaticResult(criteria.Variable[i])                
            else:
                if model[criteria.name[i]].typeName == '6D buoy':
                    point = ''.join(['orc.oeBuoy([', ','.join(criteria.data[i].split(';')),'])'])
                elif criteria.Variable[i] == 'Whole line clearance':
                    point = ''.join(['orc.oeLine(ClearanceLineName="', criteria.data[i].split('; ')[1] ,'")'])
                else:
                    point = ''.join(['orc.oe',criteria.data[i].split()[0],criteria.data[i].split()[1]])
                
                results[varName[i]] = model[criteria.name[i]].StaticResult(criteria.Variable[i], eval(point))

         
        elif pd.isnull(criteria.data)[i]:
            if criteria.Command[i] == 'Standard deviation':
                results[varName[i]] = np.std(model[criteria.name[i]].TimeHistory(criteria.Variable[i],period=period))
            else:    
                results[varName[i]] = float(eval(criteria.Command[i].lower())(model[criteria.name[i]].TimeHistory(criteria.Variable[i],period=period)))
            
        else:
            if model[criteria.name[i]].typeName == '6D buoy':
                point = ''.join(['orc.oeBuoy([', ','.join(criteria.data[i].split(';')),'])'])
            elif 'ArcLength' in criteria.data[i]:
                point = ''.join(['orc.oeArcLength(',criteria.data[i].split()[1],')'])
            elif criteria.Variable[i] == 'Whole line clearance':
                point = ''.join(['orc.oeLine(ClearanceLineName="', criteria.data[i].split('; ')[1] ,'")'])
            else:
                point = ''.join(['orc.oe',criteria.data[i].split('; ')[0].split()[0],criteria.data[i].split('; ')[0].split()[1]])
                
            if criteria.Command[i] == 'Standard deviation':  
                results[varName[i]] = np.std(model[criteria.name[i]].TimeHistory([criteria.Variable[i]],period=period,objectExtra = eval(point)))
                
                
            elif criteria.Command[i] == 'Rayleigh extremes':
        
                rayleighInput = criteria.data[i].split('; ')
            
                if any('StormDuration' in string for string in rayleighInput):
                    stormDuration = float([string for string in rayleighInput if 'StormDuration' in string][0].split('=')[1])
                else:
                    stormDuration = 3
                    
                if any('RiskFactor' in string for string in rayleighInput): 
                    riskFactor = float([string for string in rayleighInput if 'RiskFactor' in string][0].split('=')[1])
                else:
                    riskFactor = 1
                
                if any('ExtremesToAnalyse' in string for string in rayleighInput):
                    spec = orc.RayleighStatisticsSpecification(orc.exLowerTail) # read tail from Excel
                else:
                    spec = orc.RayleighStatisticsSpecification(orc.exUpperTail)
                    
                query = orc.RayleighStatisticsQuery(stormDuration, riskFactor) 
                
                
                stats = model[criteria.name[i]].ExtremeStatistics(criteria.Variable[i], period=period, objectExtra=eval(point)) # read orc.oeEndA from Excel
                
                stats.Fit(spec)
                extremes = stats.Query(query)
                
                
                results[varName[i]] = extremes.MostProbableExtremeValue
            
            else:
                results[varName[i]] = float(eval(criteria.Command[i].lower())(flatten(model[criteria.name[i]].TimeHistory([criteria.Variable[i]],period=period,objectExtra = eval(point)))))
        
        
        
        if not pd.isnull(criteria.Criteria)[i]:
            if not eval(' '.join([str(results[varName[i]]),criteria.Criteria[i]])):
                results['Criteria met'] = False
                if results['Exceeded criteria'] == '':
                    results['Exceeded criteria'] = varName[i]
                else:
                    results['Exceeded criteria'] = ' / '.join([results['Exceeded criteria'],varName[i]])
        

    # Generate index name
    index = "Hs = " + str(results['Significant wave height [m]']) + " Tp = " + str(results['Wave spectrum peak period [s]']) + " Dir = " + str(results['Wave direction [deg]'])                    
    # Generate dataframe
    df = pd.DataFrame(results, index = [index]) 
        
    
    return df

def GetAllCases(outputDir, criteria, varName):
# This function looks up all simulation files in the folder and gets results
# for each of these files
# The results are stored in a pandas DataFrame, which can be easily 
# written to Excel
    df = pd.DataFrame()

    for index, fileName in enumerate(glob.glob(os.path.join(outputDir, '*.sim'))):
    
        if not 'UNSTABLE' in fileName:     
            results = ExtractSingleCaseResults(fileName, criteria, varName)               
            df = pd.concat([df,results])
                
    return df

def CalcPercentiles(output, criteria, varName, percentiles):  # output can either be dataframe with results or a folder containing simulation files
    
    if isinstance(output, str):
        df = GetAllCases(outputDir, criteria, varName)
    else:
        df = output
    multi_index = df.set_index(['Wave direction [deg]', 'Significant wave height [m]', 'Wave spectrum peak period [s]',
                                'Current velocity [m/s]', 'Current direction [deg]'])
    print("Calculating percentiles")
    # Get all unique environments
    env = df.loc[:,'Significant wave height [m]':'Current direction [deg]'].drop_duplicates().reset_index(drop='True')
    
    
    # Create dataframe for results
    res = pd.DataFrame()
    index = 0
    for ind in range(0,len(env)):
        resultsbib = {}
        resultsbib['Wave direction [deg]'] = env.loc[ind,'Wave direction [deg]']
        resultsbib['Significant wave height [m]'] = env.loc[ind,'Significant wave height [m]']
        resultsbib['Wave spectrum peak period [s]'] = env.loc[ind,'Wave spectrum peak period [s]']  
        resultsbib['Current velocity [m/s]'] = env.loc[ind,'Current velocity [m/s]']
        resultsbib['Current direction [deg]'] = env.loc[ind,'Current direction [deg]']         
        resultsbib['Seeds [-]'] = len(multi_index.loc[(resultsbib['Wave direction [deg]'], resultsbib['Significant wave height [m]'], resultsbib['Wave spectrum peak period [s]'], resultsbib['Current velocity [m/s]'], resultsbib['Current direction [deg]'])])
        resultsbib['Criteria met'] = True
        resultsbib['Exceeded criteria'] = ''
        
        for i in range(len(criteria)):
            spds = multi_index.loc[(resultsbib['Wave direction [deg]'], resultsbib['Significant wave height [m]'], resultsbib['Wave spectrum peak period [s]'], resultsbib['Current velocity [m/s]'], resultsbib['Current direction [deg]']), varName[i]]
            if 'min' in varName[i] or 'Min' in varName[i]:
                if isinstance(spds, pd.Series) and spds.ndim > 0:
                    if spds.shape[0] > 1:
                        if percentiles == 'meanstd':
                            resultsbib[varName[i]] = spds.mean() - 0.45 * spds.std()
                        elif percentiles == 'p10p90':
                            resultsbib[varName[i]] = spds.quantile(0.1)
                    else:
                        resultsbib[varName[i]] = spds.iloc[0]
                else:
                    resultsbib[varName[i]] = spds
            else:
                if isinstance(spds, pd.Series) and spds.ndim > 0:
                    if spds.shape[0] > 1:
                        if percentiles == 'meanstd':
                            resultsbib[varName[i]] = spds.mean() + 0.45 * spds.std()
                        elif percentiles == 'p10p90':
                            resultsbib[varName[i]] = spds.quantile(0.9)
                    else:
                        resultsbib[varName[i]] = spds.iloc[0]
                else:
                    resultsbib[varName[i]] = spds
            
            if not pd.isnull(criteria.Criteria)[i]:          
                if not eval(' '.join([str(resultsbib[varName[i]]),criteria.Criteria[i]])):
                    resultsbib['Criteria met'] = False
                    if resultsbib['Exceeded criteria'] == '':
                        resultsbib['Exceeded criteria'] = varName[i]
                    else:
                        resultsbib['Exceeded criteria'] = ' / '.join([resultsbib['Exceeded criteria'], varName[i]])
            
            
            
        
        
        res1 = pd.DataFrame(resultsbib, index=[index])
        index += 1
        
        res = pd.concat([res, res1])
        
    return res, df
 
if __name__ == '__main__':    

    res, df = CalcPercentiles(outputDir, criteria, varName, percentiles)
    
    
    # Write all results to Excel
    # Write to a different Excel sheet than input otherwise 
    # the input file is OVERWRITTEN!
    print("Results to excel file")
    with pd.ExcelWriter(excelFile, 
                            engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='All results', index=False)
        res.to_excel(writer, sheet_name='Results', index=False)  