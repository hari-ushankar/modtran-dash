from io import StringIO
import csv
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import re
import json
from pathlib import Path
import numpy as np
import attr
import pdb
import json


grabnum = re.compile(r"mod_(\d+)_co2\_(\d+).*") ## change this to reflect adding dataset for altitude

def parse_sound(sound_text,colnames):
    first_sound = str.strip(sound_text)
    theFile = StringIO(first_sound)
    reader = csv.reader(theFile)
    line1 = next(reader)
    file1 = []
    for theLine in reader:
        try:
            vals = theLine[0].split()
            theLine = [float(item) for item in vals]
            print(f"{len(theLine)} ++++++ {len(colnames)}")
            if len(theLine) == len(colnames):
                file1.append(theLine)
        except:
            print("bad: ", theLine)
    profiles_df = pd.DataFrame.from_records(file1, columns=colnames)
    return profiles_df

def parse_file(filename):
    theProfile = re.compile('ATMOSPHERIC PROFILES')
    theRadiance = re.compile(r'RADIANCE(WATTS/CM2-STER-XXX)')
    theFile = open(filename, 'r')
    theLines = theFile.read()
    three_profiles = re.split(theProfile, theLines)
    colnames_1 = ('I     Z       P       T        N2 '
                  'CNTMSLF MOL_SCAT     N-1     O3  O2')
    units_1 = ('(-)        (KM)    (MB)    (K)            (MOL/CM2 KM) '
               '(-)       (-)  (ATM_CM/KM) (ATM_CM/KM)')
    units_1 = units_1.lower().split()
    colnames_1 = colnames_1.lower().split()
    units_o3_dict = dict(zip(colnames_1,units_1))
    profiles1_df = parse_sound(three_profiles[1],colnames_1)
    colnames_2 =    ('   I     Z       P       T      CNTMFRN '
                     'HNO3    AEROSOL_1 AEROSOL_2 AEROSOL_3 AEROSOL_4 '
                     'AER1*RH   CIRRUS         RH')
    units_2 = ('(-)       (KM)    (MB)    (K)   MOL/CM2 KM ATM_CM/KM'
               '(-)       (-)       (-)       (-)       (-)       (-)'
               ' (PERCNT)')
    units_2 = units_2.lower().split()
    colnames_2 = colnames_2.lower().split()
    units_aero_dict = dict(zip(colnames_2,units_2))
    profiles2_df = parse_sound(three_profiles[2],colnames_2)
    colnames_3 = ('I      Z       P       T      H2O '
                  'O3       CO2      CO       CH4      N2O '
                  'O2       NH3      NO       NO2      SO2')
    colnames_3 = colnames_3.lower().split()
    units_3 = ('(-)  (KM)   (MB)    (K)  ATM_CM/KM ATM_CM/KM ATM_CM/KM '
              'ATM_CM/KM ATM_CM/KM ATM_CM/KM ATM_CM/KM ATM_CM/KM ATM_CM/KM '
              'ATM_CM/KM ATM_CM/KM')
    units_3 = units_3.lower().split()
    units_mol_dict = dict(zip(colnames_3,units_3))
    profiles3_df = parse_sound(three_profiles[3], colnames_3)
    #pdb.set_trace()
    
    rad_parts = re.split(re.compile(r'RADIANCE\(WATTS\/CM2-STER-XXX\)'),
                         theLines)
    print(len(rad_parts))
    spectrum = []
    colnames = (
        'FREQ_invcm   WAVLEN_um    PATH_THERMAL_cm PATH_THERMAL_mum  SURFACE_EMISSION_cm '
        'SURFACE_EMISSION_umu   SURFACE_REFLECTED_cm SURFACE_REFLECTED_mum   '
        'TOTAL_RADIANCE_cm TOTAL_RADIANCE_mum   INTEGRAL_cm    TOTAL_trans')
    colnames = colnames.lower().split()
    for segment in rad_parts:
        theLines = segment.split('\n')
        for item in theLines:
            try:
                theNums = [float(aNum) for aNum in item.split()]
                if len(theNums) == 12:
                    spectrum.append(theNums)
            except:
                pass
    spectrum_df = pd.DataFrame.from_records(spectrum, columns=colnames)
    df_class = attr.make_class("attr_df_out", ["o3_prof", "aero_prof","mol_prof",
                                              "rad_spectrum"])
    df_out=df_class(profiles1_df,profiles2_df,profiles3_df,spectrum_df)
    units_class = attr.make_class("attr_units_out", ["o3_units", "aero_units","mol_units"])
    units_out = units_class(units_o3_dict,units_aero_dict,units_mol_dict)
    return df_out, units_out

def make_dir(filename):
    filename = str(filename)
    new_name = filename.replace('.txt', '_dir')
    new_dir = Path(new_name)
    new_dir.mkdir(parents=True, exist_ok=True)
    return new_dir

def make_planck(column, df, the_dir):
    co2 = grabnum.search(str(the_dir)).group(1)
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    the_rad = df['total_radiance_mum']*np.pi*1.e4
    the_wave= df['wavlen_um']
    ax.plot(the_wave,the_rad)
    ax.set_xlim([4, 40])
    ax.set_title(f"CO2 = {co2} ppm")
    ax.set_ylabel("flux in W/m^2/micron")
    ax.set_xlabel("wavelength (microns)")
    ax.grid(True)
    filename = the_dir / f"{column}.png"
    print(f"saving fig in {filename}")
    fig.savefig(filename)

def make_trans_plot(column, df, the_dir):
    co2 = grabnum.search(str(the_dir)).group(1)
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.plot('wavlen_um', 'total_trans', data=df)
    ax.set_xlim([4, 25])
    ax.set_title(f"CO2 = {co2} ppm")
    ax.set_xlabel("wavelength (microns)")
    ax.set_ylabel("transmission (height=70 km)")
    ax.grid(True)
    filename = the_dir / f"{column}.png"
    print(f"saving fig in {filename}")
    fig.savefig(filename)

if __name__ == "__main__":
    keep_dict = {}
    files = list(Path().glob("*co2*.txt"))
    print(files)
    files=files[1:]
    co2 = [grabnum.search(str(item)).group(1) for item in files]
    altitude = [grabnum.search(str(item)).group(2) for item in files]
    print(co2)
    out_dirs = [make_dir(item) for item in files]
    toc_dict = {}
    for i in altitude:
        toc_dict[i] = {}
        for j in co2:
            toc_dict[i][j]=''

    for the_file, the_dir in zip(files, out_dirs):
        co2 = grabnum.search(str(the_file)).group(1)
        altitude = grabnum.search(str(the_file)).group(2)
        toc_dict[altitude][co2] = str(the_dir)
        f"created {the_dir}"
        df_out, units_out = parse_file(the_file)
        #pdb.set_trace()
        the_dfs = [df_out.o3_prof,df_out.aero_prof,df_out.mol_prof, df_out.rad_spectrum]
        the_pqs = ['o3_prof.pq','aero_prof.pq','mol_prof.pq','rad_spectrum.pq']
        for pqfile, df in zip(the_pqs, the_dfs):
            parquet_file = the_dir / pqfile
            csv_file = parquet_file.with_suffix('.csv')
            df.to_parquet(parquet_file)
            df.to_csv(csv_file, index=False)
        units_dict=dict()
        for unitname in  ['aero_units', 'mol_units', 'o3_units']:
            the_dict = getattr(units_out,unitname)
            units_dict[unitname]=the_dict
        json_file = the_dir / 'units.json'
        with open(json_file,'w') as outfile:
            json.dump(units_dict,outfile,indent=4)
        #pdb.set_trace()
        make_trans_plot('total_trans', df_out.rad_spectrum, the_dir)
        make_planck('total_radiance_mum', df_out.rad_spectrum, the_dir)
    with open('toc_files.json', 'w') as outfile:
        json.dump(toc_dict, outfile, indent=4)

        # theFig = plt.figure(1)
        # theFig.clf()
        # theAx = theFig.add_subplot(111)
        # theAx.plot(out270['wavlen'], out270['total_radiance_mum'] * np.pi)
        # theAx.set_xlim([5, 40])
        # #convert from cm^2 to m^2
        # theIntens270 = np.sum(
        #     np.diff(out270['wavlen']) * out270['total_radiance_mum'][1:] *
        #     np.pi) * 1.e4
        # out540 = parse_file('mod_540.txt')
        # theAx.plot(out540['wavlen'], out540['total_radiance_mum'] * np.pi, 'r-')
        # theIntens540 = np.sum(
        #     np.diff(out540['wavlen']) * out540['total_radiance_mum'][1:] *
        #     np.pi) * 1.e4
        # theFig = plt.figure(2)
        # theFig.clf()
        # theAx = theFig.add_subplot(111)
        # theAx.semilogy(out0['freq'], out0['total_trans'])
        # theAx.semilogy(out270['freq'], out270['total_trans'])
        # theAx.semilogy(out540['freq'], out540['total_trans'], 'r-')
        # theAx.set_title("total trans 540")
        # theAx.set_xlim([100, 1600])

    ## theDict=csv.DictReader(theFile,colnames,delimiter=' ')
    ## for item in theDict:
    ##     print item

    #from Bio.Statistics import lowess

    ## co2index=np.where(np.logical_and(out270['wavlen'] > 11,out270['wavlen'] < 18))
    ## newout0=lowess.lowess(out0['wavlen'][co2index],out0['total_radiance_mum'][co2index]*np.pi,f=0.05)
    ## newout270=lowess.lowess(out270['wavlen'][co2index],out270['total_radiance_mum'][co2index]*np.pi,f=0.05)
    ## newout540=lowess.lowess(out540['wavlen'][co2index],out540['total_radiance_mum'][co2index]*np.pi,f=0.05)
    ## theFig=plt.figure(3)
    ## theFig.clf()
    ## theAx=theFig.add_subplot(111)
    ## #theAx.plot(out270['wavlen'],out270['total_radiance_mum']*np.pi)
    ## theAx.plot(out270['wavlen'][co2index],newout270,'b-')
    ## theAx.plot(out0['wavlen'][co2index],newout0,'g-')
    ## theAx.plot(out540['wavlen'][co2index],newout540,'k-')
    ## theAx.set_xlim([3,40])

    # theFig = plt.figure(4)
    # theFig.clf()
    # theAx = theFig.add_subplot(111)
    # #theAx.plot(out270['wavlen'],out270['total_radiance_mum']*np.pi)
    # theAx.plot(out270['freq'], out270['total_radiance_cm'] * np.pi * 1.e4,
    #            'b-')
    # theAx.plot(out0['freq'], out0['total_radiance_cm'] * np.pi * 1.e4, 'g-')
    # theAx.plot(out540['freq'], out540['total_radiance_cm'] * np.pi * 1.e4,
    #            'k-')
    # theAx.set_xlim([100, 1400])
    # plt.show()
