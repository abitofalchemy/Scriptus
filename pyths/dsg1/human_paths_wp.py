#!/usr/bin/python

# -*- coding: utf-8 -*-
# http://www.thisisthegreenroom.com/2011/installing-python-numpy-scipy-matplotlib-and-ipython-on-lion/
# -*--*--*--*--*--*--*--*-
# human_paths_wp.py 
#	

import sys
import MySQLdb 
import datetime
from itertools import groupby
import csv

def execQuery(query,out2file):
    """ Query mysql on dsg1

    Returns mysql output"""
    
    server='localhost'
    conn = None
    results=()
    try:
        #                         host    user       password    db
        conn = MySQLdb.Connection(server, 'saguinag', 'dsg1!0xB', 'wikipediagame')
        cursor = conn.cursor()

        cursor.execute(query)
        conn.commit()
        #print cursor.rowcount
        #print results
        results = cursor.fetchall()
        if (out2file):
            fn_datetime='outputFiles/'+datetime.date.today().strftime("%d%b%y")+datetime.datetime.now().strftime("_%I%M%p")
            f = open(fn_datetime,'w')
            for row in results:
                csv.writer(f).writerow(row) #f.write(row)
            f.close()
        else:
            for row in results:
                print row;

    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    finally:

        if conn:
            conn.close()

    return
################################################################
##  main
###############################################################
if __name__ == "__main__":

    query = "SELECT page_id,page_namespace,page_title from page \
            where page_title='Emily_Dickinson' \
            ORDER BY COUNT(*) DESC \
            LIMIT 10;" 
    
    query0 = "SELECT A.game_uuid, A.userid, B.start_page, B.end_page, A.clicked_page  \
              FROM wikipediagame.game_click     A \
              JOIN wikipediagame.game_game      B ON A.game_uuid=B.uuid \
              WHERE A.userid ='alex' ORDER BY A.game_uuid /*GROUP BY B.game_uuid DESC*/ ";

    query0A = "SELECT A.game_uuid, A.userid, B.start_page, B.end_page, A.clicked_page, COUNT(*) \
               FROM wikipediagame.game_click     A \
               JOIN wikipediagame.game_game      B ON A.game_uuid=B.uuid \
               WHERE A.userid ='alex' AND A.game_uuid='fc8f6efd76764568a9a88b9a3fecf70a' \
               /*ORDER BY A.game_uuid */ \
               GROUP BY B.uuid,A.userid  DESC "

    query0B = "SELECT A.game_uuid, A.userid, B.end_page, A.clicked_page, COUNT(A.clicked_page) \
               FROM wikipediagame.game_click     A \
               JOIN wikipediagame.game_game      B ON A.game_uuid=B.uuid AND A.clicked_page=B.end_page \
               WHERE A.userid ='alex'  \
               GROUP BY A.game_uuid, A.userid DESC "

    query1 = "  SELECT wp.page_id, wp.page_title, gc.game_uuid, gc.userid, gc.clicked_page \
		FROM wikipedia.page wp \
		JOIN wikipediagame.game_game wpg ON wp.page_title=wpg.start_page \
		LEFT JOIN wikipediagame.game_click gc ON gc.game_uuid=wpg.uuid \
		WHERE wp.page_id='7555441' AND gc.userid='bexinc' \
                ;"
    query1 = "  SELECT wp.page_id, wp.page_title, gc.game_uuid, gc.userid, COUNT(*) \
                FROM wikipedia.page wp \
                JOIN wikipediagame.game_game wpg ON wp.page_title=wpg.start_page \
                JOIN wikipediagame.game_click gc ON gc.game_uuid=wpg.uuid \
                WHERE wp.page_id='7555441' \
                GROUP BY gc.game_uuid DESC;"
    query2 = "  SELECT /*W.page_id, GG.end_page, */ GG.uuid, GC.userid, COUNT(*) \
                FROM wikipedia.page W \
                JOIN wikipediagame.game_game GG  ON W.page_title=GG.start_page \
                JOIN wikipediagame.game_click GC ON GG.uuid=GC.game_uuid  \
                WHERE W.page_id = '7555441' AND GG.uuid='facf2dc47b8346d08b48ff895f82686d' GROUP BY GC.userid DESC limit 10;"
    query2 = "  SELECT GP.userid, GG.uuid, COUNT(GG.uuid) \
            FROM wikipediagame.game_gameplayed  GP \
            RIGHT JOIN wikipediagame.game_click GC ON GC.userid=GP.userid \
            RIGHT JOIN wikipediagame.game_game  GG ON GG.uuid=GC.game_uuid \
            GROUP BY GG.uuid DESC LIMIT 10;"
    
    #print 'show clicked_page for a given user to show that he/she finished ...'
    query3 = "SELECT WC.userid,WC.game_uuid, WC.clicked_page /*, COUNT(WC.game_uuid) */\
             FROM wikipediagame.game_click     WC \
             /*JOIN wikipediagame.game_game WG ON WG.uuid=WC.game_uuid \
             WHERE WC.clicked_page = WG.start_page OR WC.clicked_page=WG.end_page*/ \
             WHERE WC.game_uuid='1b9d24e490714adaa23313d2bdc39ee9' \
             /*GROUP BY WG.uuid DESC*/ ;"
    # user that completed the game:
    query4= "select wc.userid,gg.uuid, gg.start_page, gg.end_page, wc.clicked_page from game_click wc JOIN game_game gg ON gg.uuid=wc.game_uuid  where wc.userid='KanyeTS' AND gg.uuid='0eab61821b0a404a82a466afbd27b9b6' LIMIT 10;"

    query4= "select wc.userid,gg.uuid, gg.start_page, gg.end_page, wc.clicked_page \
            from game_click wc JOIN game_game gg ON gg.uuid=wc.game_uuid \
            where (gg.end_page=wc.clicked_page OR gg.start_page = wc.clicked_page) AND (wc.userid IS NOT NULL) \
            GROUP BY wc.userid,gg.uuid DESC limit 10;"

    query4="SELECT wc.userid, wc.game_uuid, \
            wg.start_page, wg.end_page, wc.clicked_page, count(wc.game_uuid) \
            from wikipediagame.game_click wc JOIN wikipediagame.game_game wg ON wg.uuid=wc.game_uuid \
            WHERE wc.userid = 'themikeman' AND (wg.start_page=wc.clicked_page OR wg.end_page=wc.clicked_page)  \
            group by wg.uuid, wc.userid DESC ;"


    query5 = "SELECT wc.userid, wc.game_uuid, \
              wg.start_page, wg.end_page, wc.clicked_page, count(wc.game_uuid) \
              from wikipediagame.game_click wc JOIN wikipediagame.game_game wg ON wg.uuid=wc.game_uuid \
              WHERE wc.userid = 'themikeman' AND (wg.start_page=wc.clicked_page OR wg.end_page=wc.clicked_page)  \
              group by wg.uuid, wc.userid DESC ;"
    
#--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
    query6= "select game_uuid, userid, count(clicked_page) \
            from game_click, \
                 (   select clicks.uuid as gcuuid, clicks.userid as cguserid \
                    from ( \
                        select uuid, game_game.end_page \
                        from game_game \
                        where game_game.start_page = 'Columbia_university' group by uuid, end_page\
                        ) endpage, \
                        ( \
                        select uuid, clicked_page, game_click.userid \
                        from game_click, game_game where game_game.uuid = game_click.game_uuid and game_game.start_page = 'Columbia_university' \
                        ) clicks \
                        where endpage.uuid = clicks.uuid and clicks.clicked_page = endpage.end_page\
                ) completedgames \
                where game_click.game_uuid = completedgames.gcuuid \
                AND game_click.userid = completedgames.cguserid group by game_uuid, userid LIMIT 20;"
#--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
    query6A0= "SELECT game_uuid, userid, count(clicked_page) \
               FROM   game_click, \
                    ( select clicks.uuid as gcuuid, clicks.userid as cguserid \
                      from (select WG.uuid, WG.end_page, W.page_id \
                          from wikipediagame.game_game WG\
                          JOIN wikipedia.page W ON W.page_title=WG.start_page \
                          where W.page_id='7555441' group by WG.uuid, WG.end_page\
                      ) endpage, \
                      (select uuid, clicked_page, game_click.userid \
                      from wikipediagame.game_click, wikipediagame.game_game \
                      JOIN wikipedia.page W ON W.page_title=wikipediagame.game_game.start_page \
                      where game_game.uuid = game_click.game_uuid and W.page_id='7555441' \
                      ) clicks \
                      where endpage.uuid = clicks.uuid and clicks.clicked_page = endpage.end_page\
                    ) completedgames \
               where game_click.game_uuid = completedgames.gcuuid and \
               game_click.userid = completedgames.cguserid group by game_uuid, userid ;"
#--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
    query7="SELECT game_uuid, userid, W0.page_id, W0.page_namespace, W0.page_title, count(clicked_page) \
            FROM   game_click, \
              ( select clicks.uuid as gcuuid, clicks.userid as cguserid \
                from (select WG.uuid, WG.end_page \
                      from wikipediagame.game_game WG \
                      JOIN wikipedia.page W ON W.page_title=WG.start_page \
                      where W.page_id='7555441' group by WG.uuid, WG.end_page \
                ) endpage, \
                ( select uuid, clicked_page, game_click.userid \
                from wikipediagame.game_click, wikipediagame.game_game \
                JOIN wikipedia.page W ON W.page_title=wikipediagame.game_game.start_page \
                where game_game.uuid = game_click.game_uuid and W.page_id='7555441' \
                ) clicks \
                where endpage.uuid = clicks.uuid and clicks.clicked_page = endpage.end_page \
              ) completedgames \
              JOIN wikipedia.page as W0 ON W0.page_id='7555441' \
              where game_click.game_uuid = completedgames.gcuuid and \
                game_click.userid = completedgames.cguserid group by game_uuid, userid LIMIT 10;"

    #print 'user gid start_page end_page clicked_page count '
    #execQuery(query0) 
    #print '1 user gid start_page end_page clicked_page that completed the game '
    #execQuery(query0)
    #print '1 user 1 game completed'
    #execQuery(query0A) 
    #print '1 user that finished the game'
    #execQuery(query0B)
    
    #print 'TimQuery modified for Page_id'
    #execQuery(query6A0,1)  ## query where we use the page_id rather the page_title 
    execQuery(query7,0)

    ## read
