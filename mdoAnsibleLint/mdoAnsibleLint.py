"""mdoAnsibleLint - check Ansible YAML files"""
#
# Author: Mark Olson, 2020-05-30 after spending all day looking for a missing ":"
#
# Reads one named Ansible YAML file and does crude check.
#
# import sys
# import os
import yaml
import argparse

def mdoAnsibleLint(yamlFile, verbose):
    myDict = {"a": 1}
    print("YAML file: %s" % yamlFile)
    f=open(yamlFile, 'r')
    y = yaml.load(f)
    f.close()
    #
    # y should either be
    #   1. None - there was nothing in the YAML file
    #   2. A dict {} - no structure - example just "---" then "ubuntu_apache_listen_port: 8080"
    #   3. Otherwise, all elements of y should be a dict {}
    #
    warns = 0
    errs = 0
    if (type(y) != type(myDict)) and (type(y) != type(None)):
        for elem in y:
            if type(elem) != type(myDict):
                warns += 1
                print("  WARNING: element %s is type %s not %s" % (elem, type(elem), type(myDict)))
    if verbose or (0 != (errs+warns)):
        print("   yaml.load(f) = %s" % y)
    print(" %d ERRORS and %d Warnings in YAML file %s" %(errs, warns, yamlFile))

if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(prog='mdoAnsibleLint',
        formatter_class=argparse.RawTextHelpFormatter,
        description="stdout receives warnings/errors found in *.yml file",
        epilog="""Example:
python mdoAnsibleLint.py test.yml
for v in `find ansible_mdo -name "*.yml"`; do python mdoAnsibleLint.py $v; done
""",
        usage='%(prog)s oneYamlFile.yml')
    my_parser.add_argument('yamlFile',type=str,help='path to a single YAML file')
    my_parser.add_argument('-v', '--verbose', action='store_true',
                           help='always display contents of parsed YAML')
    args = my_parser.parse_args()


    mdoAnsibleLint(args.yamlFile, args.verbose)
