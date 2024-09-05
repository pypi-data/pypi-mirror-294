import subprocess
from multiprocessing import Pool
import ExtractResults as eRes
import pandas as pd
from functools import partial
import psutil
import OrcFxAPI
import os
import time
import random
import sys
from pathlib import Path

def runSingle(criteria, varName, unstableSettingRetry, sleepTime, licenseRetry, file):
    temp = changedExtensionFileName(os.path.join(os.path.dirname(file), 'temp', os.path.basename(file)), '.csv')

    if os.path.exists(temp):
        print('Reading temporary file')
        df = pd.read_csv(temp, index_col=0)

    elif os.path.exists(changedExtensionFileName(file, '.sim')):
        for attempt in range(licenseRetry):
            try:
                time.sleep(random.random() * sleepTime)
                singleModel = OrcFxAPI.Model(threadCount=1)
            except Exception as e:
                if e.status == OrcFxAPI.StatusCode.LicensingError:
                    print('A licensing error occurred, retrying...')
                    continue
                else:
                    print('An unexpected error occurred, see the error message: \n' + e.msg)
                    sys.exit()
            else:
                print(changedExtensionFileName(file, '.sim'), 'already exists, continuing with analysis')
                singleModel.LoadSimulation(changedExtensionFileName(file, '.sim'))
                df = eRes.ExtractSingleCaseResults(singleModel, criteria, varName)
                df.to_csv(temp)
                break
        else:
            print('All attempts to retrieve the license failed after ' + licenseRetry + ' tries. Execution aborted.')
            sys.exit()

    elif os.path.exists(changedExtensionFileName(file, '_UNSTABLE.sim')):
        print(changedExtensionFileName(file, '_UNSTABLE.sim'), 'already exists, ignoring this one')
        df = pd.DataFrame()

    else:
        for attempt in range(licenseRetry):
            try:
                time.sleep(random.random() * sleepTime)
                singleModel = OrcFxAPI.Model(threadCount=1)
            except Exception as e:
                if e.status == OrcFxAPI.StatusCode.LicensingError:
                    print('A licensing error occurred, retrying...')
                    continue
                else:
                    print('An unexpected error occurred, see the error message: \n' + e.msg)
                    sys.exit()
            else:
                singleModel.LoadData(file)
                print('Started calculating:', file)
                singleModel.RunSimulation()

                if not singleModel.simulationComplete:

                    while unstableSettingRetry > 0:

                        unstableSettingRetry -= 1
                        print('Simulation', file, 'unstable, retrying with smaller time step')
                        dt = singleModel.general.ImplicitConstantTimeStep
                        singleModel.general.ImplicitConstantTimeStep = dt / 2
                        singleModel.RunSimulation()

                        if singleModel.simulationComplete:

                            print('Save', file)
                            singleModel.SaveSimulation(changedExtensionFileName(file, '.sim'))

                            print('Extract results from:', file)
                            df = eRes.ExtractSingleCaseResults(singleModel, criteria, varName)

                            df.to_csv(temp)

                            break

                    if not singleModel.simulationComplete:
                        print('Simulation failed again, too bad..., continuing with the rest')
                        print('Save', file)
                        singleModel.SaveSimulation(changedExtensionFileName(file, '_UNSTABLE.sim'))

                        df = pd.DataFrame()

                else:
                    print('Save', file)
                    singleModel.SaveSimulation(changedExtensionFileName(file, '.sim'))

                    print('Extract results from:', file)
                    df = eRes.ExtractSingleCaseResults(singleModel, criteria, varName)

                    df.to_csv(temp)
                break

        else:
            print('All attempts to retrieve the license failed after ' + licenseRetry + ' tries. Execution aborted.')
            sys.exit()

    return df


def get_files(directory, pattern):
    for path in Path(directory).rglob(pattern):
        yield path.absolute()


def changedExtensionFileName(oldFileName, newExtension):
    return ''.join((os.path.splitext(oldFileName)[0], newExtension))


def runBatch(directory, pattern, threads, criteria, varName, unstableSettingRetry, sleepTime, licenseRetry):
    # Decide how many proccesses will be created
    # sum_size = 0
    if threads <= 0:
        num_cpus = psutil.cpu_count(logical=False) - 2
    else:
        num_cpus = threads

    batchFiles = []

    # Get files based on pattern and their sum of size
    for file in get_files(directory, pattern):
        batchFiles.append(file)

    # Create the pool
    process_pool = Pool(processes=num_cpus)

    # Start processes in the pool
    part = partial(runSingle, criteria, varName, unstableSettingRetry, sleepTime, licenseRetry)

    dfs = process_pool.imap(part, batchFiles)
    # Concat dataframes to one dataframe
    data = pd.concat(dfs, ignore_index=True)

    process_pool.close()
    process_pool.join()

    resultsName = ''.join(['results_It', str(directory.split('_')[1]), '.xlsx'])

    data.to_excel(os.path.join(directory, resultsName))

    return data

