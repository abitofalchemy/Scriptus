# -*- coding: utf-8 -*-
import glob
import os
import sys
import json
import argparse
import pandas as pd
from influxdb import DataFrameClient


def write_habitslab_df_to_influx(pd_df, pId, studyName, dataType, userId):
    if pd_df is None: return
    # index of the dataframe
    pd_df['time'] = pd.to_datetime(pd_df['date'])
    pd_df = pd_df.set_index('time')
    pd_df['deviceId'] = "NL1"
    pd_df['pId'] = pId
    pd_df['studyName'] = studyName
    pd_df['type'] = dataType
    pd_df['userId'] = userId

    tags = {"deviceId": "NL1",
            "pId":      pId,
            "studyId":  studyName,
            "type":     dataType,
            "userId":   userId}
    dbConnDF = DataFrameClient(host='localhost', port=8086)
    dbConnDF.write_points(pd_df, 'habitsDB', tags=tags)



def frame_to_json_obj_fn(row,nfxl_dict, pId, studyName, dataType, userId):
    nfxl_dict.setdefault("influx_points", []).append({"measurement": "necklace",
                                     "tags": {
                                        "deviceId": "NL1",
                                        "pId": pId,
                                        "studyId": studyName,
                                        "type": dataType,
                                        "userId": userId
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

    return nfxl_dict



def main(participantId, studyName, dataType, userId):
    """ main function
    arguments:
    - participantId study participant
    """

    rootDir = "/Volumes/fsmresfiles/PrevMed/Alshurafa_Lab/Lab_Common/"
    rootDir = "/opt/fsmresfiles/" + studyName +"/"

    if userId is None:
        from pathlib import Path
        print("! detecting userId")
        userId = Path.home().parts[-1]

    # Hard coding the sensor=necklace
    files = glob.glob(rootDir+dataType +"/"+ participantId +"/NECKLACE/*.csv")
    df = pd.DataFrame()
    for f in files:
        df = pd.read_csv(f, header=0)
        write_habitslab_df_to_influx(df,
                participantId, studyName, dataType,
                userId)
        exit()#break
        nflx_point_dict = {}
        df.apply(lambda row: frame_to_json_obj_fn(row, nflx_point_dict,
            participantId,studyName, dataType, userId), axis=1)

        #print (type(nflx_point_dict['influx_points'][0]))
        #print (nflx_point_dict['influx_points'][0])
        #brea


    # print(json.dumps(nflx_point_dict, indent=4, sort_keys=True))
    # for k,v in nflx_point_dict.items():
    #    print ("k: {} -> v: {}".format(k, len(v)))

def parse_args():
    """Parse the args from main."""
    parser = argparse.ArgumentParser(description='tst_index_fsm_to_influx: Create Points for InfluxDB')
    parser.add_argument('-p', '--participant', type=str, required=False,
                        default='TEST', help='Participant ID')
    parser.add_argument("--datatype", type=str, required=False, default="CLEAN",
            help="Data Type [CLEAN|RAW|ANNOTATION]")
    parser.add_argument("-s","--study", type=str, required=True,
            help="HABits Lab Study Name")
    parser.add_argument("-u", "--userid", type=str, required=False,
            help="UserId")


    return parser


if __name__ == '__main__':
    args = parse_args()

    if (len(sys.argv) < 2):
        print(args.print_help())
        exit()
    args = args.parse_args()
    main(participantId=args.participant,
         studyName=args.study,
         dataType=args.datatype,
         userId=args.userid)
