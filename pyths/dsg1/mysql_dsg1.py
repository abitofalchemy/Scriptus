#!/usr/bin/python

# -*- coding: utf-8 -*-
# http://www.thisisthegreenroom.com/2011/installing-python-numpy-scipy-matplotlib-and-ipython-on-lion/
# -*--*--*--*--*--*--*--*-
# mysql_dsg1.py 
#	

import sys
import MySQLdb 

#server='129.74.155.16'
server='localhost'
conn = None

try:

    #conn = MySQLdb.Connection('snoopy.cse.nd.edu', 'root', 'ixaedu1', 'neurosenz')
    #                         host    user       password    db
    conn = MySQLdb.Connection(server, 'saguinag', 'dsg1!0xB', 'wikipedia')
    cursor = conn.cursor()
    query = "SELECT page_id,page_namespace,page_title from page \
            where page_title='Emily_Dickinson' \
            ORDER BY COUNT(*) DESC \
            LIMIT 10;" 
    query0 = "SELECT C.userid, A.uuid, COUNT(C.userid)  \
              FROM wikipediagame.game_game       A \
              JOIN wikipediagame.game_click      B ON A.uuid=B.game_uuid \
              JOIN wikipediagame.game_gameplayed C ON B.userid=C.userid \
              WHERE B.userid ='alex' GROUP BY B.game_uuid DESC ";
    query0A = "SELECT C.userid, B.game_uuid, B.clicked_page   \
             FROM wikipediagame.game_game       A \
             JOIN wikipediagame.game_click      B ON A.uuid=B.game_uuid \
             JOIN wikipediagame.game_gameplayed C ON B.userid=C.userid \
             WHERE C.userid ='alex' AND B.game_uuid='fffe6cd3a41a4022861c4a37874b22ad'";

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
    
    query3 = "SELECT GP.userid,GC.game_uuid,GC.clicked_page,W.page_id/*, COUNT(*)*/ \
            FROM wikipediagame.game_gameplayed GP \
            LEFT JOIN wikipediagame.game_click GC ON GC.userid = GP.userid \
            JOIN wikipedia.page W ON W.page_title=GC.clicked_page \
            WHERE W.page_id='7555441' \
            /*GROUP BY GC.game_uuid DESC*/ LIMIT 10;"

    print '>> games, users, completed games'
    query4="SELECT WC.game_uuid, WC.userid, WG.start_page, WG.end_page, COUNT(WC.game_uuid)  from wikipediagame.game_click WC \
            join wikipediagame.game_game WG ON WC.game_uuid=WG.uuid \
            WHERE WC.clicked_page=WG.start_page AND WC.clicked_page=WG.end_page \
            GROUP BY WC.game_uuid DESC LIMIT 10;"

    print '>> example user that finished a game'
    query5="SELECT WC.userid, WC.game_uuid, WG.start_page, WG.end_page, WC.clicked_page  \
            FROM wikipediagame.game_game  WG  \
            JOIN wikipediagame.game_click WC ON WC.game_uuid=WG.uuid \
            WHERE WC.userid='dudet';"


    cursor.execute(query5)
    conn.commit()
    #print cursor.rowcount
    results = cursor.fetchall()
    #print results 
    for row in results:
	print row;
		 
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

finally:
    
    if conn:
        conn.close()


def buildConnectionString(params):
    """Build a connection string from a dictionary of parameters.
    Returns string."""
    return ";".join(["%s=%s" % (k, v) for k, v in params.items()])

if __name__ == "__main__":

    excQuery("SELECT wc.userid, wc.game_uuid, 
