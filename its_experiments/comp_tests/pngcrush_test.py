#!/usr/bin/env python3
from pathlib import Path
from PIL import Image
from statistics import mode, mean
import subprocess
import copy
import csv
import time
import os

"""
Test various compression tools on a directory of images.
"""

def main():
    jpegs = Path(__file__).parent / "images/test_jpgs"
    pngs = Path(__file__).parent / "images/test_pngs"
    results = dict()

    out_folder = mk_folder("pngcrush_results/")

    results['pngcrush'] = run_pngcrush(pngs)
    results['pngcrush_mode'] = run_pngcrush(pngs,results['pngcrush']['other']['mode_method'])

    write_results(results)


def calc_percent_difference(original, compressed):
    original_size = os.stat(original).st_size
    compressed_size = os.stat(compressed).st_size
    percent_comp = ((original_size  - compressed_size) / original_size) * 100
    return percent_comp

def mk_folder(dir_name):
    folder = Path(__file__).parent / dir_name
    if not folder.exists():
        Path.mkdir(folder)
    return folder

def write_results(results_dict):
    with open('pngcrush_results.csv', 'w') as csvfile:
        fieldnames = ['utility', 'mean_run_time', 'best_compression_id', 'worst_compression_id','mean_compression_percentage','other_descript', 'other']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for key in results_dict:
            writer.writerow({'utility':key, 'mean_run_time':results_dict[key]['mean_run_time'], 'best_compression_id':results_dict[key]['best_compression_id'],\
                'worst_compression_id':results_dict[key]['worst_compression_id'],'mean_compression_percentage':results_dict[key]['mean_compression']})

            if results_dict[key]['other'] is not None:
                for other_key in results_dict[key]['other']:
                    if results_dict[key]['other'][other_key] is not None:
                        writer.writerow({'other_descript':other_key, 'other':results_dict[key]['other'][other_key]})

def run_pngcrush(pngs, method=None):

    print("Running PNGCrush ...\n")
    
    print(method)
    if method is None:
        base = ["./pngcrush"]
        out_folder = mk_folder("pngcrush_results/heuristic_method/")
    else:
        base = ["./pngcrush", "-m " + str(method)]
        out_folder = mk_folder("pngcrush_results/method_" + str(method) + "/")
    saved_output = [] # list of output that needs to be parsed to gather more data
    num_methods = 148
    best_methods = list()
    compression_percent = list()
    increase_percent = list() # list of filesize increase percentages
    mean_time = list()
    
    num_pngs = 0

    for img in pngs.iterdir():
        if img.name.lower().find("png") != -1:
            print(img.name)
            start = time.time()
            command = copy.deepcopy(base)
            command.append(img)
            command.append(out_folder / img.name)
            try:
                Path.touch(out_folder / img.name)

                output = subprocess.check_output(command, stderr=subprocess.STDOUT)
                # output is a bytes-like object, so decode into a string
                decoded_output = output.decode('ascii')
                # find index of relevant data i.e. best method, compression percentage, etc.
                relevant_index = decoded_output.find("Best")
                # store relevant data for later processing
                if relevant_index != -1:
                    saved_output.append(decoded_output[relevant_index:])
                mean_time.append(time.time() - start)
            except Exception as e:
                print("An error occurred with PNGCrush:" + str(e))

    for line in saved_output:
        # best method number is after the first '=' and before the first '('
        best_method = int(line[line.find('=') + 1: line.find('(')])
        best_methods.append(best_method)

        if line.find('filesize reduction') != -1:
            percent_reduction = float(line[line.find('filesize reduction') - 7:line.find('filesize reduction')].strip('% ('))
            compression_percent.append(percent_reduction)
        else:
            # Sometimes filesizes increase for reasons unknown
            percent_increase = float(line[line.find('filesize increase') - 7:line.find('filesize increase')].strip('% ('))
            increase_percent.append(percent_increase)

    mean_time = mean(mean_time)

    if len(increase_percent) == 0:
        increase_percent.append(-1)

    if len(compression_percent) == 0:
        compression_percent.append(-1)

    res = {'mean_run_time':mean_time, 'mean_compression': mean(compression_percent),'best_compression_id':compression_percent.index(max(compression_percent)),\
        'worst_compression_id':compression_percent.index(min(compression_percent)),'other':{'mode_method':mode(best_methods), 'mean_size_increase':mean(increase_percent)}}
    return res


if __name__ == '__main__':
    main()
