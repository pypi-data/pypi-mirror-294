from .utils import SeedsCreateVariations as cVar
from .utils import ExtractResults as eRes
from .utils import multiProcess as multi
import pandas as pd
import OrcFxAPI as orc
import os.path
import shutil
import subprocess
import tkinter as tk
import sys
import argparse
import time
# 'Importing the numpy C-extensions failed.' error can be solved by running the following in Anaconda PowerShell prompt:
# conda install numpy --force-reinstall

def main():

    def LicenceErrHandler(action, licenceRetryAttempts=0):
        if action == orc.LicenceReconnectionAction.Begin:
            # First API call, set initial retry count.
            print("Licence fail, first retry attempt")
            time.sleep(10)  # wait a bit
            licenceRetryAttempts = 1
            return True  # Signal we want to keep retrying
        elif action == orc.LicenceReconnectionAction.Continue:
            # Subsequent retry calls land here.
            # Choose to continue retrying or give up.
            if licenceRetryAttempts > 10:
                print("Given up trying to get the licence.")
                return False  # Stop retrying, the API will raise an error.
            else:
                print(f"Licence fail, retry attempt {licenceRetryAttempts:d}")
                time.sleep(10)  # wait a bit
                licenceRetryAttempts += 1
                return True
        elif action == orc.LicenceReconnectionAction.End:
            # This action occurs after retry attempts are stopped
            # (successfully or not). Opportunity to reset any relevant data.
            return False

    orc.RegisterLicenceNotFoundHandler(LicenceErrHandler)

    parser = argparse.ArgumentParser()
    parser.add_argument('--nogui', action='store_true')
    args = parser.parse_args()
    
    if not args.nogui:
        # GUI
        def cancel():
            window.destroy()
            quit()
    
        def save():
            with open('settings.txt', 'w') as file:
                file.write(entries[0].get() + '\n' +
                           entries[1].get() + '\n' +
                           entries[2].get() + '\n' +
                           entries[3].get() + '\n' +
                           entries[4].get() + '\n' +
                           entries[5].get() + '\n' +
                           entries[6].get() + '\n' +
                           entries[7].get() + '\n' +
                           entries[8].get() + '\n' +
                           entries[9].get() + '\n' +
                           entries[10].get() + '\n' +
                           entries[11].get() + '\n' +
                           entries[12].get() + '\n' +
                           percentilesMode.get() + '\n' +
                           str(removeOldMode.get()) + '\n' +
                           str(runIterationsMode.get()) + '\n' +
                           str(unstableSettingRetryMode.get()) + '\n'
                           )
            print('Settings saved successfully as settings.txt')
    
        def restore():
            for id, entry in enumerate(entries):
                entry.delete(0, tk.END)
                if isinstance(defaults[id], str):
                    entry.insert(0, defaults[id])
            percentilesMode.set(defaults[13])  # default value for radio buttons
            removeOldMode.set(defaults[14])
            runIterationsMode.set(defaults[15])
            unstableSettingRetryMode.set(defaults[16])
    
        def run():
            global initialVarFile
            initialVarFile = entries[0].get()  # file specifying initial conditions
            global initialModel
            initialModel = entries[1].get()  # base OrcaFlex model
            global initialOutFolder
            initialOutFolder = entries[2].get()  # name of output folder for initial calculations
            global criteriaFile
            criteriaFile = entries[3].get()  # file defining criteria
            global pattern
            pattern = entries[4].get()  # extension used to scan for already completed simulations
            global completeIt
            completeIt = [int(num) for num in entries[5].get().split(',')] if entries[5].get() != '' else [] # Vector specifying any already (fully) completed iterations (results will be read from Excel)
            global maxHs
            maxHs = float(entries[6].get())  # Maximum allowable significant wave height
            global hsStep
            hsStep = float(entries[7].get())
            global nSeed
            nSeed = int(entries[8].get()) # Number of wave seeds
            global threads
            threads = int(entries[9].get())  # Number of parallel threads
            global minT
            minT = int(entries[10].get())  # Minimum wave period (spectrum is truncated)
            global sleepTime
            sleepTime = int(entries[11].get())
            global licenseRetry
            licenseRetry = int(entries[12].get())
            global percentiles
            percentiles = percentilesMode.get()  # meanstd or p90 or p10
            global removeOld
            removeOld = removeOldMode.get() # True or False, choose if you want to delete folders of iterations
            global runIterations
            runIterations = runIterationsMode.get()
            global unstableSettingRetry
            unstableSettingRetry = unstableSettingRetryMode.get()
    
            window.destroy()
    
        window = tk.Tk()
        window.title('Enter initial parameters')
        frm_form = tk.Frame(relief=tk.RAISED, borderwidth=1)
        frm_form.pack(fill=tk.BOTH, expand=True)
    
        labels = [
            'Variations file name:',
            'Model file name:',
            'Initial output folder name:',
            'Criteria file name:',
            'Pattern:',
            'Complete iterations (comma separated numbers):',
            'Max wave height:',
            'Wave height convergence step:',
            'Number of seeds:',
            'Number of threads:',
            'Min wave period:',
            'Sleep time [s]:',
            'Licensing error retries:',
            'Percentiles mode:',
            'Remove old iteration folders:',
            'Run iterations:',
            'Unstable simulations handling:',
        ]
    
        defaults = [
            'InputVariations.xlsx',
            'LC2S Splash zone.dat',
            'Iteration_0',
            'Criteria.xlsx',
            '*dat',
            '',
            '2.0',
            '0.25',
            '2',
            '2',
            '1',
            '120',
            '10',
            'meanstd',
            False,
            True,
            0,
        ]
    
        if not os.path.isfile('settings.txt'):
            settings = defaults
        else:
            settings = []
            with open('settings.txt', 'r') as sFile:
                for num, line in enumerate(sFile):
                    if num == 14 or num == 15:
                        v = line.strip()
                        if v == 'False':
                            settings.append(False)
                        else:
                            settings.append(True)
                    elif num == 16:
                        settings.append(int(line.strip()))
                    else:
                        settings.append(line.strip())
    
        percentilesMode = tk.StringVar(value=settings[13])
        removeOldMode = tk.BooleanVar(value=settings[14])
        runIterationsMode = tk.BooleanVar(value=settings[15])
        unstableSettingRetryMode = tk.IntVar(value=settings[16])
        entries = []
    
        for idx, text in enumerate(labels):
            frm_form.rowconfigure(idx, weight=1)
            frm_form.columnconfigure([0, 1], weight=1)
            label = tk.Label(master=frm_form, text=text)
            if text == 'Percentiles mode:':
                frm_radio = tk.Frame(master=frm_form)
                tk.Radiobutton(frm_radio, text='Mean +- standard deviation', variable=percentilesMode, value='meanstd').pack(side=tk.LEFT)
                tk.Radiobutton(frm_radio, text='P90 / P10', variable=percentilesMode, value='p10p90').pack(side=tk.LEFT)
                frm_radio.grid(row=idx, column=1, padx=5, pady=5, sticky='w')
            elif text == 'Remove old iteration folders:':
                frm_radio = tk.Frame(master=frm_form)
                tk.Radiobutton(frm_radio, text='Yes', variable=removeOldMode, value=True).pack(side=tk.LEFT)
                tk.Radiobutton(frm_radio, text='No', variable=removeOldMode, value=False).pack(side=tk.LEFT)
                frm_radio.grid(row=idx, column=1, padx=5, pady=5, sticky='w')
            elif text == 'Run iterations:':
                frm_radio = tk.Frame(master=frm_form)
                tk.Radiobutton(frm_radio, text='Yes', variable=runIterationsMode, value=True).pack(side=tk.LEFT)
                tk.Radiobutton(frm_radio, text='No', variable=runIterationsMode, value=False).pack(side=tk.LEFT)
                frm_radio.grid(row=idx, column=1, padx=5, pady=5, sticky='w')
            elif text == 'Unstable simulations handling:':
                frm_radio = tk.Frame(master=frm_form)
                tk.Radiobutton(frm_radio, text='Retry once', variable=unstableSettingRetryMode, value=1).pack(side=tk.LEFT)
                tk.Radiobutton(frm_radio, text='Retry twice', variable=unstableSettingRetryMode, value=2).pack(side=tk.LEFT)
                tk.Radiobutton(frm_radio, text='Retry thrice', variable=unstableSettingRetryMode, value=3).pack(side=tk.LEFT)
                tk.Radiobutton(frm_radio, text='Ignore', variable=unstableSettingRetryMode, value=0).pack(side=tk.LEFT)
                frm_radio.grid(row=idx, column=1, padx=5, pady=5, sticky='w')
            else:
                entry = tk.Entry(master=frm_form, width=50)
                entries.append(entry)
                entry.insert(0, settings[idx])
                entry.grid(row=idx, column=1, padx=5, pady=5)
            label.grid(row=idx, column=0, sticky='e', padx=5, pady=5)
    
        frm_buttons = tk.Frame()
        frm_buttons.pack(fill=tk.X, ipadx=5, ipady=5)
        btn_cancel = tk.Button(master=frm_buttons, text='Quit', command=cancel, width=30)
        btn_cancel.pack(side=tk.LEFT, expand=True)
        btn_save = tk.Button(master=frm_buttons, text='Save configuration', command=save, width=30)
        btn_save.pack(side=tk.LEFT, expand=True)
        btn_restore = tk.Button(master=frm_buttons, text='Restore defaults', command=restore, width=30)
        btn_restore.pack(side=tk.LEFT, expand=True)
        btn_run = tk.Button(master=frm_buttons, text='Run', command=run, width=30)
        btn_run.pack(side=tk.LEFT, expand=True)
    
        window.mainloop()
        
    else:
        settings = []
        with open('settings.txt', 'r') as sFile:
            for num, line in enumerate(sFile):
                if num == 14 or num == 15:
                    v = line.strip()
                    if v == 'False':
                        settings.append(False)
                    else:
                        settings.append(True)
                elif num == 16:
                    settings.append(int(line.strip()))
                else:
                    settings.append(line.strip())

        global initialVarFile
        initialVarFile = settings[0]  # file specifying initial conditions
        global initialModel
        initialModel = settings[1]  # base OrcaFlex model
        global initialOutFolder
        initialOutFolder = settings[2]  # name of output folder for initial calculations
        global criteriaFile
        criteriaFile = settings[3]  # file defining criteria
        global pattern
        pattern = settings[4]  # extension used to scan for already completed simulations
        global completeIt
        completeIt = [int(num) for num in settings[5].split(',')] if settings[5] != '' else []  # Vector specifying any already (fully) completed iterations (results will be read from Excel)
        global maxHs
        maxHs = float(settings[6])  # Maximum allowable significant wave height
        global hsStep
        hsStep = float(settings[7])
        global nSeed
        nSeed = int(settings[8])  # Number of wave seeds
        global threads
        threads = int(settings[9])  # Number of parallel threads
        global minT
        minT = int(settings[10])  # Minimum wave period (spectrum is truncated)
        global sleepTime
        sleepTime = int(settings[11])
        global licenseRetry
        licenseRetry = int(settings[12])
        global percentiles
        percentiles = settings[13]  # meanstd or p90 or p10
        global removeOld
        removeOld = settings[14]  # True or False, choose if you want to delete folders of iterations
        global runIterations
        runIterations = settings[15]
        global unstableSettingRetry
        unstableSettingRetry = settings[16]

    # Initialize
    if os.path.isfile('tempCriteria.xlsx'):
        os.remove('tempCriteria.xlsx')
    subprocess.call(['powershell.exe', 'copy ' + criteriaFile + ' tempCriteria.xlsx'])
    criteria = pd.read_excel('tempCriteria.xlsx', header=3, skiprows=[4]).drop(
        columns=['name', 'cell', 'cell.1']).rename(columns={'name.1': 'name'})

    try:
        singleModel = orc.Model(threadCount=1)
    except Exception as e:
        if e.status == orc.StatusCode.LicensingError:
            print('A licensing error occurred, please check whether the license is available and try again!')
            sys.exit()
        else:
            print('An unexpected error occurred, see the error message: \n' + e.msg)
            sys.exit()
    else:
        #  Check if all objects in criteria file are present
        singleModel.LoadData(initialModel)
        objects = singleModel.objects
        objectNames = [x.name for x in objects]
        critObjects = criteria['name'].unique().tolist()
        for objectName in critObjects:
            if objectName not in objectNames:
                print('Missing object ' + objectName + ' from criteria list in the provided model! Aborting...')
                quit()

        if os.path.isfile('tempVariations.xlsx'):
            os.remove('tempVariations.xlsx')
        subprocess.call(['powershell.exe', 'copy ' + initialVarFile + ' tempVariations.xlsx'])
        initialVar = pd.read_excel('tempVariations.xlsx')
        limitingSeas = pd.DataFrame(columns=initialVar.columns)
        critName = [None] * len(criteria)

        for i in range(len(criteria)):
            critName[i] = ''.join([criteria.Label[i], ' (', criteria.Command[i],
                                   ')'])  #'_'.join([criteria.name[i],criteria.Variable[i],'_'.join(criteria.Command[i].split())])

        limitingSeas = pd.concat([pd.DataFrame(columns=['Governing criteria']), limitingSeas, pd.DataFrame(columns=critName)], axis=1)

        if os.path.isdir(initialOutFolder) and removeOld:
            shutil.rmtree(initialOutFolder)
            os.mkdir(initialOutFolder)
            os.mkdir(os.path.join(initialOutFolder, 'temp'))
        elif not os.path.isdir(initialOutFolder):
            os.mkdir(initialOutFolder)
            os.mkdir(os.path.join(initialOutFolder, 'temp'))

        # Create and run initial variations
        if 0 in completeIt:
            print('Initial calculations already completed, loading results')
            batchRes = pd.read_excel(os.path.join(initialOutFolder, 'results.xlsx'))
        else:
            cVar.CreateVariationFiles(initialModel, initialOutFolder, initialVar.hs, initialVar.tp, initialVar.dir, nSeed,
                                      minT)

            print('Running initial calculations')

            batchRes = multi.runBatch(initialOutFolder, pattern, threads, criteria, critName, unstableSettingRetry, sleepTime, licenseRetry)

            print('Finished initial calculations')

        # Process initial calculations
        res, df = eRes.CalcPercentiles(batchRes, criteria, critName, percentiles)

        res.to_excel(os.path.join(initialOutFolder, 'percentiles_It0.xlsx'), index=False)

        itVar = initialVar.astype(float)
        allConverged = False
        it = 1

        while not allConverged and runIterations:
            print('Check if criteria are met')

            critCheck = res['Criteria met']
            allConverged = True
            itVarN = pd.DataFrame(columns=initialVar.columns, dtype=float)
            prevCritT = pd.Series([], name=critCheck.name, dtype=float)
            row = 0

            if it == 1:
                prevCrit = critCheck
                prevRes = res

            for ind in range(len(critCheck)):
                if (prevCrit[ind] and not critCheck[ind]):
                    itVar['hs'].iloc[ind] -= hsStep

                    index = itVar.iloc[[ind]].index
                    a = itVar.iloc[[ind]].reset_index(drop=True)
                    b = prevRes[critName][(prevRes['Wave direction [deg]'] == float(itVar.dir.iloc[[ind]])) & (
                                prevRes['Significant wave height [m]'] == float(itVar.hs.iloc[[ind]])) & (
                                                      round(prevRes['Wave spectrum peak period [s]'], 2) == round(
                                                  float(itVar.tp.iloc[[ind]]), 2))].reset_index(drop=True)
                    lCrit = res['Exceeded criteria'][(res['Wave direction [deg]'] == float(itVar.dir.iloc[[ind]])) & (
                                res['Significant wave height [m]'] == float(itVar.hs.iloc[[ind]])) & (
                                                      round(res['Wave spectrum peak period [s]'], 2) == round(
                                                  float(itVar.tp.iloc[[ind]]), 2))].reset_index(drop=True).rename('Governing criteria')
                    c = pd.concat([lCrit, a, b], axis=1).set_index(index)

                    limitingSeas = pd.concat([limitingSeas, c])
                elif (not prevCrit[ind] and critCheck[ind]):
                    index = itVar.iloc[[ind]].index
                    a = itVar.iloc[[ind]].reset_index(drop=True)
                    b = res[critName][(res['Wave direction [deg]'] == float(itVar.dir.iloc[[ind]])) & (
                                res['Significant wave height [m]'] == float(itVar.hs.iloc[[ind]])) & (
                                                  round(res['Wave spectrum peak period [s]'], 2) == round(
                                              float(itVar.tp.iloc[[ind]]), 2))].reset_index(drop=True)
                    lCrit = prevRes['Exceeded criteria'][
                        (prevRes['Wave direction [deg]'] == float(itVar.dir.iloc[[ind]])) & (
                                res['Significant wave height [m]'] == float(itVar.hs.iloc[[ind]])) & (
                                round(prevRes['Wave spectrum peak period [s]'], 2) == round(
                            float(itVar.tp.iloc[[ind]]), 2))].reset_index(drop=True).rename('Governing criteria')
                    c = pd.concat([lCrit, a, b], axis=1).set_index(index)

                    limitingSeas = pd.concat([limitingSeas, c])
                elif (itVar['hs'].iloc[[ind]].values >= maxHs) and critCheck[ind]:
                    index = itVar.iloc[[ind]].index
                    a = itVar.iloc[[ind]].reset_index(drop=True)
                    b = res[critName][(res['Wave direction [deg]'] == float(itVar.dir.iloc[[ind]])) & (
                                res['Significant wave height [m]'] == float(itVar.hs.iloc[[ind]])) & (
                                                  round(res['Wave spectrum peak period [s]'], 2) == round(
                                              float(itVar.tp.iloc[[ind]]), 2))].reset_index(drop=True)
                    lCrit = prevRes['Exceeded criteria'][
                        (prevRes['Wave direction [deg]'] == float(itVar.dir.iloc[[ind]])) & (
                                prevRes['Significant wave height [m]'] == float(itVar.hs.iloc[[ind]])) & (
                                round(prevRes['Wave spectrum peak period [s]'], 2) == round(
                            float(itVar.tp.iloc[[ind]]), 2))].reset_index(drop=True).rename('Governing criteria')
                    c = pd.concat([lCrit, a, b], axis=1).set_index(index)

                    limitingSeas = pd.concat([limitingSeas, c])
                elif critCheck[ind]:
                    itVar['hs'].iloc[[ind]] += hsStep
                    itVarN = pd.concat([itVarN, itVar.iloc[[ind]]])
                    prevCritT[row] = critCheck[ind]
                    allConverged = False
                    row += 1
                else:
                    itVar['hs'].iloc[[ind]] -= hsStep
                    itVarN = pd.concat([itVarN, itVar.iloc[[ind]]])
                    prevCritT[row] = critCheck[ind]
                    allConverged = False
                    row += 1

            itVar = itVarN
            prevCrit = prevCritT
            prevRes = res

            if not allConverged:

                itFolder = ''.join(['Iteration_', str(it)])

                if os.path.isdir(itFolder) and removeOld:
                    shutil.rmtree(itFolder)
                    os.mkdir(itFolder)
                    os.mkdir(os.path.join(itFolder, 'temp'))
                elif not os.path.isdir(itFolder):
                    os.mkdir(itFolder)
                    os.mkdir(os.path.join(itFolder, 'temp'))

                if it in completeIt:
                    print('Iteration', str(it), 'already completed, loading results')
                    batchRes = pd.read_excel(os.path.join(itFolder, 'results.xlsx'))
                else:
                    print('Creating simulation files for iteration', str(it), ':')

                    cVar.CreateVariationFiles(initialModel, itFolder, itVar.hs.tolist(), itVar.tp.tolist(),
                                              itVar.dir.tolist(), nSeed, minT)

                    print('Running simulations for iteration ', str(it))
                    batchRes = multi.runBatch(itFolder, pattern, threads, criteria, critName, unstableSettingRetry, sleepTime, licenseRetry)

                res, df = eRes.CalcPercentiles(batchRes, criteria, critName, percentiles)

                res.to_excel(os.path.join(itFolder, ''.join(['percentiles_It', str(it), '.xlsx'])), index=False)

                it += 1

        print('Finished calculations, exporting results to Excel')
        limitingSeas.to_excel('limitingSeas.xlsx')
        if os.path.isfile('tempCriteria.xlsx'):
            os.remove('tempCriteria.xlsx')
        if os.path.isfile('tempVariations.xlsx'):
            os.remove('tempVariations.xlsx')
        with open('completed.txt', 'w') as f:
            f.write('Calculation finished!')
