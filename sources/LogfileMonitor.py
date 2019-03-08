#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
###################################################################
# changes :                                                       #
# 20190301-XJS : Initial                                          #
###################################################################
# Search the pattern from the monitored log file/s, and generate the output with defined format

"""
import copy
import logging
import os
import re
import sys

import yaml

SCRIPT_NAME = os.path.basename(__file__)

d = os.path.dirname(__file__)

# set default values
CONFIG_FILE, PARAM_FILE, OUT_FILE, RC_FILE = \
    os.path.join(d, "LogfileMonitorConfig.yml"), os.path.join(d, "LogfileMonitorParam.yml"), \
    os.path.join(d, "LogfileMonitorOut.yml"), os.path.join(d, "ReturnedCode.yml")

# define the output format
OUT_SAMPLE = "LogfileMonitorOut.sample"

###
# Get the setting of loglevel for DEBUG instead from CONFIG_FILE
pass
DEBUG = "1"

if DEBUG == "1":
    logging.basicConfig(filename='/tmp/%s' % SCRIPT_NAME.replace(".py", ".log"),
                        level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')
else:
    logging.basicConfig(filename='/tmp/%s' % SCRIPT_NAME.replace(".py", ".log"),
                        level=logging.WARNING,
                        format='%(asctime)s - %(levelname)s - %(message)s')


def usage():
    print("Usage is:")
    print("%s [-c <Configure file>] [-p <Parameter file>] [-o <Output file>]" % SCRIPT_NAME)
    print("-c <Configure file>  Default is ./LogfileMonitorConfig.yml")
    print("-p <Parameter file>  Default is ./LogfileMonitorPara.yml")
    print("-o <Output file>  Default is ./LogfileMonitorOut.yml")
    sys.exit(1)


def get_argv_dict(argv):
    """
    Save all the parameters into variable

    :return: otpd
    """
    optd = {"script": argv[0]}
    argv = argv[1:]

    while argv:
        if len(argv) >= 2:
            optd[argv[0]] = argv[1]
            argv = argv[2:]
        else:
            usage()
    return optd


def get_from_yaml(file):
    """
    Capture the data from YAML file to a variable
    :global: OUT_ITEM_SAMPLE
    :param file: file
    :return: filed
    """

    filed = {}
    # Will capture the data from file to a variable
    logging.info("Capture the data from file(%s) to a variable" % file)
    try:
        with open(file) as f:
            filed = yaml.load(f)
    except IOError:
        logging.error("RC=1, File access error: %s" % file)

        OUT_ITEM_SAMPLE["rc"] = "1"
        write_data_outfile(OUT_ITEM_SAMPLE)  # Append the data into output file
        OUT_ITEM_SAMPLE["rc"] = ""

    except:
        logging.error("RC=99, File might not exactly apply YAML format: %s" % file)
        logging.error(str(Exception))

        OUT_ITEM_SAMPLE["rc"] = "99"
        write_data_outfile(OUT_ITEM_SAMPLE)  # Append the data into output file
        OUT_ITEM_SAMPLE["rc"] = ""

    return filed


def valid_param_data(data, mylist_out):
    """
    Validate the parameters defined in Parameters file
    :param mylist_out:
    :param data:
    :return: update the contents of variable of mylist_out
    """

    for i in range(len(data)):
        item = copy.deepcopy(data[i])

        # Check the required parameters
        required_list = ["logicalname", "logfilename"]
        logging.info("TBD: will verify the list of required parameters:\n %s" % required_list)
        for k in required_list:
            if not item.get(k) or not item[k]:
                # Not configured or NULL
                print("Parameter is missing for: %s" % k)

                # return error
                print("Return error")

        logging.info("TBD: will validate the parameters of:\n %s" % data)
        pass
        # e.g to fill the returned code to 3 with "invalid parameters" into mylist_out
        mylist_out[0]["rc"] = "3"

    return mylist_out


def trans_pattern_logfile(mylist_1):
    """
    Translate the search pattern to the exact logfilename/s from the regexp if have
    :param mylist_1:
    :return: mylist_2
    """
    logging.debug("To be translated search pattern with regexp logfilenames:")
    for i in range(len(mylist_1)):
        logging.debug(mylist_1[i])
    mylist_2 = []

    for i in range(len(mylist_1)):
        match_yn = False
        # Save the item of pattern search for logfilename regexp
        item_logfilename = mylist_1[i]

        # Get the filename and dir name
        logging.debug("logfilename regexp is: %s" % mylist_1[i]["logfilename"])

        file_exp = os.path.basename(mylist_1[i]["logfilename"])
        dir_exp = os.path.dirname(mylist_1[i]["logfilename"])

        for f in os.listdir(dir_exp):
            file = os.path.join(dir_exp, f)
            if os.path.isfile(file):
                # check with expr
                res = re.match(file_exp, f)
                if res:
                    match_yn = True
                    matched_file = os.path.join(dir_exp, res.group(0))
                    logging.debug("File matches: %s" % matched_file)
                    # Update and/or Add logfilename
                    item_logfilename["logfilename"] = matched_file
                    # Append it
                    mylist_2.append(item_logfilename)
        if not match_yn:
            logging.error("No match for logfilename: %s" % item_logfilename["logfilename"])

    return mylist_2


def trans_param_pattern(mylist_1, mylist_2):
    """
    Translate the parameters to every pattern
    :param mylist_1:
    :param mylist_2:
    :return: mylist_2
    """
    logging.debug("To be translated data:")
    for i in range(len(mylist_1)):
        logging.debug(mylist_1[i])

    for i in range(len(mylist_1)):
        item = copy.deepcopy(mylist_1[i])
        mydict = {}
        for k in item.keys():
            if k != "patternmatch":
                mydict[k] = item[k]

        for j in range(len(item["patternmatch"])):
            mydict2 = copy.deepcopy(mydict)

            pattern = item["patternmatch"][j]
            for k in pattern.keys():
                mydict2[k] = pattern[k]

            # Append the data into mylist_2
            mylist_2.append(mydict2)

    logging.debug("translated data:")
    for i in range(len(mylist_2)):
        logging.debug(mylist_2[i])

    return mylist_2


def write_data_outfile(out_item):
    """
    Append the data to OUT_FILE
    :param out_item: new data
    : Global: OUT_FILE, RC_FILE
    :return: Update OUT_FILE
    """

    # Get rcdesc relies on rc from RC_FILE file
    mylist_rc = get_from_yaml(RC_FILE)

    out_item["rcdesc"] = "RC is not defined"

    #    print(out_item)
    #    print(mylist_rc)
    #    print(RC_FILE)

    for i in range(len(mylist_rc)):
        if out_item["rc"] == mylist_rc[i]["rc"]:
            out_item["rcdesc"] = mylist_rc[i]["desc"]
            break

    # Append the new item into OUT_FILE

    try:
        if os.path.exists(OUT_FILE):
            with open(OUT_FILE, 'r') as f:
                out_data = yaml.load(f)
            if out_data is None:
                out_data = []
        else:
            out_data = []

        out_data.append(out_item)  # Append new item

        with open(OUT_FILE, 'w') as f:  # Write data to file
            yaml.dump(out_data, f)
    except:
        logging.error("Failed to append data to output file")

    return OUT_FILE


def main():
    global CONFIG_FILE, PARAM_FILE, OUT_FILE, OUT_SAMPLE
    global OUT_ITEM_SAMPLE

    # Get args
    argv = sys.argv
    logging.info(argv)
    mydict = get_argv_dict(argv)

    # Validate the imput parameters
    para = ["script", "-c", "-p", "-o", "-h"]
    for key in mydict:
        if key not in para:
            print("%s is not supported!!!" % key)
            usage()

    logging.info("file is:%s" % PARAM_FILE)

    if mydict.get("-c"):
        CONFIG_FILE = mydict["-c"]
    if mydict.get("-p"):
        PARAM_FILE = mydict["-p"]
    if mydict.get("-o"):
        OUT_FILE = mydict["-o"]

    ###
    # Will change the script from here
    # to run it with a interval

    logging.info(PARAM_FILE)
    # Get the fullname for PARAM_FILE
    logging.info("TBD: Will get the fullname for config file(%s)" % PARAM_FILE)
    pass

    out_data = get_from_yaml(OUT_SAMPLE)  # Get data from sample file
    OUT_ITEM_SAMPLE = out_data[0]  # Get one item from the output sample

    # Clear the data, and only keep the keys and default values
    for k in OUT_ITEM_SAMPLE.keys():
        if k not in ["actualnumberofhits", "maxnumberofhits", "ttl"]:
            OUT_ITEM_SAMPLE[k] = ""
        else:
            # Set 0 for Interger type data
            OUT_ITEM_SAMPLE[k] = 0

    # Get parameters from file
    mylist_param = get_from_yaml(PARAM_FILE)
    logging.debug("data for parameter file:\n %s" % mylist_param)

    #  Translate the parameters to every patternsearch
    mylist_pattern = []
    mylist_pattern = trans_param_pattern(mylist_param, mylist_pattern)
    logging.debug("data for patterns:\n%s" % mylist_pattern)

    # debugging: list out all the search patterns
    logging.debug("All the search patterns:")
    for i in range(len(mylist_pattern)):
        logging.debug(mylist_pattern[i])

    # Translate the regexp in logfilename to the exact logfilename/s
    mylist_logfile = trans_pattern_logfile(mylist_pattern)

    if len(mylist_logfile) == 0:
        print("There is not any exactly match logfilename.")
    else:
        print("All the search patterns with exact logfilename")
        for i in range(len(mylist_logfile)):
            print(mylist_logfile[i])

    ###
    # Search pattern in the specific logfile
    # Every item should like as following:
    # {'alarmonmatch': 'Y', 'responsible': 'Support Application 001', 'occurence': '1', \
    # 'eventtype': 'InitializationError', 'logicalname': 'http-server-log', 'readtype': 'Incremental', \
    # 'logfilename': '/tmp/http8.log', 'deduplicate': 'N', 'clearmatch': 'ABCRunning', 'instance': 'http', \
    # 'pattern': 'ErrorABC', 'rotation': 'N', 'logfield2': 'fieldx2', \
    # 'matchtype': 'substring', 'logfield1': 'fieldx1', 'sevrity': 'sev1'}
    #
    # Useful keys for searching are:
    #     logfilename, pattern, matchtype ???
    # also depends on:
    #     readtype: Full/Increment
    #
    # will search as well for:
    #      clearmatch
    # The match pattern will add into global variable:out_data (a list which contains dictionary type data)

    pass

    ###
    # Process logfile ( delete or not) depends on:
    #     rotation: Y/N
    #     and when readtype is Full
    pass

    ###
    # Process (deduplicate) and generate event from global variable: out_data

    pass

    ###
    # Maintain the logs
    pass

    # ##
    # run in next turn
    pass

    # End of Main


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
