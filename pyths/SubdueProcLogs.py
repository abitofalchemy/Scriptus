#!/usr/bin/python 
# encoding: utf-8

"""
Process the Subdue logs

"""
__author__ = """Sal Aguinaga (saguinag@nd.edu)"""
#    Copyright (C) 2015
#    Sal Aguinaga <saguinag@nd.edu>
#    All rights reserved.
#    BSD license.

from SubdueLogFiles import SubdueLogFiles
import os, sys
import argparse


if __name__ == '__main__':

	print'-'*80
	parser = argparse.ArgumentParser(description='Parse Subdue Ouput files')
	parser.add_argument('log_files', help='Input file: subdue log', action='store')
	args = parser.parse_args()

	os.chdir(args.log_files)
	print args.log_files
