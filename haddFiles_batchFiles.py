#!/usr/bin/env python3
from pathlib import Path
import subprocess
import argparse


parser = argparse.ArgumentParser(description='A script hadding hadding different background and signal samples')
parser.add_argument('--basePath',help="Enter base path of Location of Root Files",required=True)
parser.add_argument('--haddDir',help="Folder in which the files are present",required=True)
parser.add_argument('--savePath',help="Place where to store the hadded files",required=True)
parser.add_argument('--Search',help="Anything before this will be the file name",required=True)
parser.add_argument('--temp',help="Temporary location on nfs scratch to store the file",required=True)
parser.add_argument('--data', help='If it is data - only use the nanoHadd', action='store_true')
parser.add_argument('--OnlySpecific', help='If you use this then fill out the names in the files to hadd array', action='store_true')
args = parser.parse_args()

hadd_dir_name = args.haddDir
base_path = Path(args.basePath)
hadd_dir = base_path / hadd_dir_name
save_path = Path(args.savePath)

filestohadd = [
"GluGluToRadionToHHTo2B2VTo2L2Nu_M-2000_02January25_0737_skim__skim_Jan_2_25",
"GluGluToBulkGravitonToHHTo2B2WToLNu2J_M-2000_02January25_0737_skim__skim_Jan_2_25",
"GluGluToBulkGravitonToHHTo2B2Tau_M-1250_02January25_0739_skim__skim_Jan_2_25",
"GluGluToBulkGravitonToHHTo2B2WToLNu2J_M-1750_02January25_0740_skim__skim_Jan_2_25",
"GluGluToRadionToHHTo2B2VTo2L2Nu_M-1200_02January25_0739_skim__skim_Jan_2_25",
"GluGluToBulkGravitonToHHTo2B2WToLNu2J_M-1500_02January25_0739_skim__skim_Jan_2_25",
"GluGluToBulkGravitonToHHTo2B2Tau_M-4000_02January25_0740_skim__skim_Jan_2_25",
"GluGluToRadionToHHTo2B2WToLNu2J_M-1600_02January25_0739_skim__skim_Jan_2_25",
"GluGluToBulkGravitonToHHTo2B2Tau_M-1500_02January25_0741_skim__skim_Jan_2_25",
"GluGluToBulkGravitonToHHTo2B2WToLNu2J_M-3500_02January25_0740_skim__skim_Jan_2_25",
"GluGluToBulkGravitonToHHTo2B2Tau_M-3000_02January25_0742_skim__skim_Jan_2_25",
"GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-1250_02January25_0740_skim__skim_Jan_2_25",
"GluGluToRadionToHHTo2B2VTo2L2Nu_M-1800_02January25_0741_skim__skim_Jan_2_25",
"ZZTo4Q_5f_02January25_0741_skim__skim_Jan_2_25",
"GluGluToRadionToHHTo2B2VTo2L2Nu_M-3000_02January25_0741_skim__skim_Jan_2_25",
"GluGluToRadionToHHTo2B2VTo2L2Nu_M-4000_02January25_0742_skim__skim_Jan_2_25",
"GluGluToRadionToHHTo2B2WToLNu2J_M-1200_02January25_0743_skim__skim_Jan_2_25",
"GluGluToRadionToHHTo2B2VTo2L2Nu_M-1600_02January25_0742_skim__skim_Jan_2_25",
"GluGluToRadionToHHTo2B2WToLNu2J_M-2000_02January25_0743_skim__skim_Jan_2_25",
"GluGluToBulkGravitonToHHTo2B2WToLNu2J_M-4500_02January25_0743_skim__skim_Jan_2_25",
"GluGluToBulkGravitonToHHTo2B2WToLNu2J_M-1250_02January25_0745_skim__skim_Jan_2_25",
"GluGluToRadionToHHTo2B2VTo2L2Nu_M-2500_02January25_0743_skim__skim_Jan_2_25",
"GluGluToBulkGravitonToHHTo2B2Tau_M-2500_02January25_0745_skim__skim_Jan_2_25",
"GluGluToBulkGravitonToHHTo2B2WToLNu2J_M-3000_02January25_0745_skim__skim_Jan_2_25",
"GluGluToBulkGravitonToHHTo2B2Tau_M-1000_02January25_0746_skim__skim_Jan_2_25",
"GluGluToRadionToHHTo2B2VTo2L2Nu_M-1000_02January25_0745_skim__skim_Jan_2_25",
"GluGluToRadionToHHTo2B2WToLNu2J_M-1400_02January25_0746_skim__skim_Jan_2_25",
"GluGluToBulkGravitonToHHTo2B2Tau_M-2000_02January25_0747_skim__skim_Jan_2_25",
"GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-3500_02January25_0746_skim__skim_Jan_2_25",
"GluGluToRadionToHHTo2B2WToLNu2J_M-1800_02January25_0747_skim__skim_Jan_2_25",
"GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-2500_02January25_0747_skim__skim_Jan_2_25",
"GluGluToRadionToHHTo2B2WToLNu2J_M-2500_02January25_0747_skim__skim_Jan_2_25",
"GluGluToBulkGravitonToHHTo2B2Tau_M-1750_02January25_0751_skim__skim_Jan_2_25",
"GluGluToRadionToHHTo2B2WToLNu2J_M-3000_02January25_0750_skim__skim_Jan_2_25",
"GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-1500_02January25_0753_skim__skim_Jan_2_25",
"GluGluToBulkGravitonToHHTo2B2WToLNu2J_M-4000_02January25_0753_skim__skim_Jan_2_25",
"GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-4000_02January25_0752_skim__skim_Jan_2_25",
"GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-1750_02January25_0751_skim__skim_Jan_2_25",
"WWTo2L2Nu_02January25_0744_skim__skim_Jan_2_25",
"GluGluToBulkGravitonToHHTo2B2WToLNu2J_M-1000_02January25_0752_skim__skim_Jan_2_25",
"GluGluToBulkGravitonToHHTo2B2Tau_M-4500_02January25_0751_skim__skim_Jan_2_25",
"GluGluToRadionToHHTo2B2WToLNu2J_M-4500_02January25_0752_skim__skim_Jan_2_25",
"GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-1000_02January25_0750_skim__skim_Jan_2_25",
"GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-2000_02January25_0753_skim__skim_Jan_2_25",
"ZZTo2L2Nu_02January25_0737_skim__skim_Jan_2_25",
"GluGluToRadionToHHTo2B2VTo2L2Nu_M-3500_02January25_0755_skim__skim_Jan_2_25",
"GluGluToRadionToHHTo2B2WToLNu2J_M-3500_02January25_0755_skim__skim_Jan_2_25",
"GluGluToRadionToHHTo2B2VTo2L2Nu_M-1400_02January25_0756_skim__skim_Jan_2_25",
"GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-3000_02January25_0756_skim__skim_Jan_2_25",
"GluGluToBulkGravitonToHHTo2B2WToLNu2J_M-2500_02January25_0755_skim__skim_Jan_2_25",
"GluGluToRadionToHHTo2B2WToLNu2J_M-4000_02January25_0756_skim__skim_Jan_2_25",
"GluGluToRadionToHHTo2B2WToLNu2J_M-1000_02January25_0757_skim__skim_Jan_2_25",
"GluGluToBulkGravitonToHHTo2B2VTo2L2Nu_M-4500_02January25_0758_skim__skim_Jan_2_25",
"GluGluToBulkGravitonToHHTo2B2Tau_M-3500_02January25_0758_skim__skim_Jan_2_25",
"GluGluToRadionToHHTo2B2VTo2L2Nu_M-4500_02January25_0757_skim__skim_Jan_2_25",
"ST_s-channel_4f_hadronicDecays_02January25_0754_skim__skim_Jan_2_25",
"WWTo4Q_4f_02January25_0748_skim__skim_Jan_2_25"]
               
alreadyHaddFileNames = []
#filestoSkip = ["DYJetsToLL_M-4to50_HT-100to200.root",
#"DYJetsToLL_M-4to50_HT-400to600.root",
#"DYJetsToLL_M-4to50_HT-600toInf.root",
#"DYJetsToLL_M-4to50_HT-70to100.root",
#"DYJetsToLL_M-50_HT-100to200.root",
#"DYJetsToLL_M-50_HT-1200to2500.root",
#"DYJetsToLL_M-50_HT-400to600.root",
#"DYJetsToLL_M-50_HT-600to800.root",
#"DYJetsToLL_M-50_HT-70to100.root",
#"DYJetsToLL_M-50_HT-800to1200.root",
#"QCD_HT1000to1500.root",
#"QCD_HT100to200.root",
#"QCD_HT1500to2000.root",
#"QCD_HT200to300.root",
#"QCD_HT500to700.root",
#"QCD_HT700to1000.root",
#"RadionTohhTohtatahbb_narrow_M-1000.root",
#"RadionTohhTohtatahbb_narrow_M-1200.root",
#"RadionTohhTohtatahbb_narrow_M-1400.root",
#"RadionTohhTohtatahbb_narrow_M-1600.root",
#"RadionTohhTohtatahbb_narrow_M-1800.root",
#"RadionTohhTohtatahbb_narrow_M-2000.root",
#"RadionTohhTohtatahbb_narrow_M-2500.root",
#"ST_s-channel_4f_leptonDecays.root",
#"ST_t-channel_antitop_4f_InclusiveDecays.root",
#"ST_t-channel_top_4f_InclusiveDecays.root",
#"ST_tW_antitop_5f_inclusiveDecays.root",
#"ST_tW_top_5f_inclusiveDecays.root",
#"QCD_HT50to100.root",
#"TTTo2L2Nu.root",
#"TTTo2L2Nu_2.root",
#"TTToHadronic.root",
#"TTToSemiLeptonic.root",
#"TTToSemiLeptonic_2.root",
#"MET_Run2018A.root",
#"MET_Run2018B.root",
#"MET_Run2018C.root"]

numberOfFilesToHadd = 500

#searchPhrase = "_01March22_0950_skim_2016_Data_29February-singleFileSkimForSubmission"
#searchPhrase = "_TuneCP5"
searchPhrase = args.Search

for obj in hadd_dir.iterdir():
    if not obj.is_dir():
        continue
    
    if(args.OnlySpecific):
        if(obj.name not in filestohadd):
            continue

    if searchPhrase not in obj.name:
    #if searchPhrase in obj.name:
        #print(f"{obj.name} doesn't have "+searchPhrase+" in it")
        continue
    if searchPhrase in obj.name:
        print (f"{obj.name} has  "+searchPhrase+" in it")

    filename = f'{obj.name[:obj.name.index(searchPhrase)]}.root'
    if filename not in alreadyHaddFileNames:
        filename = f'{obj.name[:obj.name.index(searchPhrase)]}.root'
    else:
        filename = f'{obj.name[:obj.name.index(searchPhrase)]}_other.root'
    #For debugging:
    #if ((filename == "Run2016G.root") or (filename == "TTT")):
    #    continue

    #if filename in filestoSkip:
        #print("To skip: ", filename)
        #continue

    print (filename)
    alreadyHaddFileNames.append(filename)
    root_list = [str(rootfile) for rootfile in obj.glob("**/*.root")]
    print ("Total number of files to hadd = ", len(root_list))
    if ((len(root_list)>numberOfFilesToHadd) and (len(root_list) != 0) and (args.data)):
        print("###############################################################################")
        print ("The number of Data files exceeds maximum limit of = ", numberOfFilesToHadd, "We add using nanohadd in batches")
        print ("We will create ",int((len(root_list)-1)/numberOfFilesToHadd)+1," temp files")
        #print (hadd_dir/obj.name/"*.root")
        #I need set up the fall back mechanism to add 900 files at a time
        end_str=""
        for n, i in enumerate(range(int((len(root_list)-1)/numberOfFilesToHadd)+1)):
            #end_str += f" {filename}_{n}_tmp.root"
            end_str += f" {args.temp}/tmp_{n}_{filename}"
            success1 = subprocess.call(f'PhysicsTools/NanoAODTools/scripts/haddnano.py {args.temp}/tmp_{n}_{filename} {" ".join([str(j) for j in root_list[numberOfFilesToHadd*(i):numberOfFilesToHadd*(i+1)]])}', shell=True)
    
        success2 = subprocess.call(f'PhysicsTools/NanoAODTools/scripts/haddnano.py {args.temp}/{filename} {end_str}', shell=True)
        success3 = subprocess.call(f'mv {args.temp}/{filename} {save_path}', shell=True)
        success4 = subprocess.call(f'rm {args.temp}/tmp_*_{filename}', shell=True)
        print("###############################################################################")

    elif ((len(root_list) != 0) and (not args.data)):
        print ("These are MC files = ", len(root_list), "We will use cmssw hadd")
        success1=subprocess.call(f'hadd {args.temp}/{filename} {hadd_dir/obj.name/"*.root"}', shell=True)
        success2=subprocess.call(f'mv {args.temp}/{filename} {save_path}', shell=True)        
    
    elif ((len(root_list)<=numberOfFilesToHadd) and (len(root_list) != 0) and (args.data)):
        print("These are the Data files to add = ",len(root_list),"We will use nanohadd")
        success1=subprocess.call(f'PhysicsTools/NanoAODTools/scripts/haddnano.py {args.temp}/{filename} {hadd_dir/obj.name/"*.root"}', shell=True)
        success2=subprocess.call(f'mv {args.temp}/{filename} {save_path}', shell=True)







#######    success1=subprocess.call(f'PhysicsTools/NanoAODTools/scripts/haddnano.py {args.temp}/{filename} {hadd_dir/obj.name/"*.root"}', shell=True)
#######
#######
#######    if (success1 !=0 and (not args.data)):
#######        print ("NanoAOD tools hadd didnt work, switching to hadd cmssw. This is only done on MC samples")
#######        #success = subprocess.call(f'hadd -f /nfs_scratch/parida/HaddFilesTempStore2/{filename} {hadd_dir/obj.name/"*.root"}', shell=True)
#######        success = subprocess.call(f'hadd -f {args.temp}/{filename} {hadd_dir/obj.name/"*.root"}', shell=True)
#######
#######    #success2=subprocess.call(f'mv /nfs_scratch/parida/HaddFilesTempStore2/{filename} {save_path}', shell=True)
#######    success2=subprocess.call(f'mv {args.temp}/{filename} {save_path}', shell=True)
