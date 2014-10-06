#!/usr/bin/python

# -*- coding: utf-8 -*-
# http://www.thisisthegreenroom.com/2011/installing-python-numpy-scipy-matplotlib-and-ipython-on-lion/
# -*--*--*--*--*--*--*--*-
# wikipediagame.py 
#	

import sys
import MySQLdb 

def humanPaths4GameStartingAt(srcPageId,limit):
    server='localhost'
    conn = None
    print '-----------------------------------\n',limit
    try:
        conn = MySQLdb.Connection(server, 'saguinag', 'dsg1!0xB', 'wikipedia')
        cursor = conn.cursor()
        if limit<0:
            query ="SELECT gc.game_uuid, gc.userid, W0.page_id, W0.page_namespace, W0.page_title, count(gc.clicked_page) \
                    FROM   wikipediagame.game_click AS gc, \
                    ( select clicks.uuid as gcuuid, clicks.userid as cguserid \
                    from (select WG.uuid, WG.end_page \
                    from wikipediagame.game_game WG \
                    JOIN wikipedia.page W ON W.page_title=WG.start_page \
                    where W.page_id='%s' group by WG.uuid, WG.end_page \
                    ) endpage, \
                    ( select uuid, clicked_page, game_click.userid \
                    from wikipediagame.game_click, wikipediagame.game_game \
                    JOIN wikipedia.page W ON W.page_title=wikipediagame.game_game.start_page \
                    where game_game.uuid = game_click.game_uuid and W.page_id='%s' \
                    ) clicks \
                    where endpage.uuid = clicks.uuid and clicks.clicked_page = endpage.end_page \
                    ) completedgames \
                    JOIN  wikipedia.page as W0 ON W0.page_id='%s' \
                    where gc.game_uuid=completedgames.gcuuid and \
                    gc.userid = completedgames.cguserid group by gc.game_uuid, userid ;" % (srcPageId,srcPageId,srcPageId)

        else :
            query ="SELECT gc.game_uuid, gc.userid, W0.page_id, W0.page_namespace, W0.page_title, count(gc.clicked_page) \
                    FROM   wikipediagame.game_click AS gc, \
                    ( select clicks.uuid as gcuuid, clicks.userid as cguserid \
                    from (select WG.uuid, WG.end_page \
                    from wikipediagame.game_game WG \
                    JOIN wikipedia.page W ON W.page_title=WG.start_page \
                    where W.page_id='%s' group by WG.uuid, WG.end_page \
                    ) endpage, \
                    ( select uuid, clicked_page, game_click.userid \
                    from wikipediagame.game_click, wikipediagame.game_game \
                    JOIN wikipedia.page W ON W.page_title=wikipediagame.game_game.start_page \
                    where game_game.uuid = game_click.game_uuid and W.page_id='%s' \
                    ) clicks \
                    where endpage.uuid = clicks.uuid and clicks.clicked_page = endpage.end_page \
                    ) completedgames \
                    JOIN  wikipedia.page as W0 ON W0.page_id='%s' \
                    WHERE gc.game_uuid=completedgames.gcuuid and \
                    gc.userid = completedgames.cguserid \
                    GROUP BY gc.game_uuid, userid LIMIT %d;" % (srcPageId,srcPageId,srcPageId,limit)

        cursor.execute(query)
        conn.commit()
        
        results = cursor.fetchall()
        #print results
        #for row in results:
        #    print row;

    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    finally:
        if conn:
            conn.close()
        return results


def gamesWithSourceNode(srcPageId,limit):
    server='localhost'
    conn = None
    
    try:
        conn = MySQLdb.Connection(server, 'saguinag', 'dsg1!0xB', 'wikipedia')
        cursor = conn.cursor()
        if limit<0:
            query = "SELECT W.page_id, uuid, W2.page_id \
                     FROM wikipediagame.game_game \
                     JOIN wikipedia.page W ON W.page_title=start_page \
                     JOIN wikipedia.page W2 ON W2.page_title=end_page \
                     WHERE W.page_id='%s';" % (srcPageId)
        else :
            query = "SELECT W.page_id, uuid, W2.page_id \
                 FROM wikipediagame.game_game \
                 JOIN wikipedia.page W ON W.page_title=start_page \
                 JOIN wikipedia.page W2 ON W2.page_title=end_page \
                 WHERE W.page_id='%s' LIMIT %d ;" % (srcPageId,limit)


        cursor.execute(query)
        conn.commit()
        #print cursor.rowcount
        results = cursor.fetchall()
        #print results 
        #for row in results:
        #    print row;
             
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    finally:
        if conn:
            conn.close()
        return results 

def buildConnectionString(params):
    """Build a connection string from a dictionary of parameters.
    Returns string."""
    return ";".join(["%s=%s" % (k, v) for k, v in params.items()])
if __name__ == "__main__":
	#import sys
	#fib(int(sys.argv[1]))
	print gamesWithSourceNode('1018340',10)
	print humanPaths4GameStartingAt('1018340',-1)
