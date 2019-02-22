# -*- coding: utf-8 -*-
import glob
import os
import sys
import json
import argparse
import pandas as pd

'''
{
  "measurement": "cpu_load_short",
  "tags": {
    "host": "server01",
    "region": "us-west"
  },
  "time": "2009-11-10T23:00:00Z",
  "fields": {
    "Float_value": 0.64,
    "Int_value": 3,
    "String_value": "Text",
    "Bool_value": 1
  }
}

json_body = [
    { "measurement": "necklace",
    "tags": {
      "necklaceId": "NL1",
      "pId": "203-2"
    },
    "time": "2019-01-11 15:39:08.030000-06:00Z",
    "fields": {
      "proximity": 0.64,
      "ambient": 3,
      "leanForward": "Text",
      "qW": 1,
      "qX": 1,
      "qY": 1,
      "qZ": 1,
      "aX": 1,
      "aY": 1,
      "aZ": 1,
      "power": 1,
      "cal": 3
    }
    }
]
Using itertuples (faster, see https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas)

for row in df.itertuples():
    print (getattr(row, "type"), getattr(row, "value"))
If you need to modify the rows you are iterating, use apply:

def my_fn(c):
    return c + 1

df['plus_one'] = df.apply(lambda row: my_fn(row['value']), axis=1)

'''

def frame_to_json_obj_fn(row,nfxl_dict):
    nfxl_dict.setdefault("influx_points", []).append({"measurement": "necklace",
                                     "tags": {
                                        "deviceId": "NL1",
                                        "pId": "203-2"
                                        },
                                    "time": row['date'],
                                    "fields": {
                                        "rtime":     row['Time'],
                                        "proximity": row['proximity'],
                                        "ambient":   row['ambient'],
                                        "leanForward":row['leanForward'],
                                        "qW":  row['qW'],
                                        "qX":  row['qX'],
                                        "qY":  row['qY'],
                                        "qZ":  row['qZ'],
                                        "aX":  row['aX'],
                                        "aY":  row['aY'],
                                        "aZ":  row['aZ'],
                                        "power": row['power'],
                                        "cal": 3,
                                        },
                                        })





def main(participantId):
    """ main function
    arguments:
    - participantId study participant
    """
    
    rootDir = "/Volumes/fsmresfiles/PrevMed/Alshurafa_Lab/Lab_Common/"

    files = glob.glob(rootDir+"SenseWhy/CLEAN/"+ participantId +"/NECKLACE/*.csv")
    df = pd.DataFrame()
    for f in files:
        df = pd.read_csv(f, header=0)
        nflx_point_dict = {}
        df.apply(lambda row: frame_to_json_obj_fn(row, nflx_point_dict), axis=1)

        print (type(nflx_point_dict['influx_points'][0]))
        print (nflx_point_dict['influx_points'][0])
        break


    # print(json.dumps(nflx_point_dict, indent=4, sort_keys=True))


def parse_args():
    """Parse the args from main."""
    parser = argparse.ArgumentParser(description='Create Points for InfluxDB')
    parser.add_argument('-p', '--participant', type=str, required=False,
                        default='TEST', help='Participant ID')
    return parser


if __name__ == '__main__':
    args = parse_args()

    if (len(sys.argv) < 2):
        print(args.print_help())
        exit()
    args = args.parse_args()
    main(participantId=args.participant)
