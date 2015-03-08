#!/usr/bin/python

# -*- coding: utf-8 -*-
# http://www.thisisthegreenroom.com/2011/installing-python-numpy-scipy-matplotlib-and-ipython-on-lion/
# -*--*--*--*--*--*--*--*-
# wikipediagame.py 
#    

import sys
import MySQLdb 

def wpgame(query):
    server='localhost'
    conn = None
        
    try:
        conn = MySQLdb.Connection(server, 'saguinag', 'dsg1!0xB', 'wikipediagame')
        cursor = conn.cursor()
            
        cursor.execute(query)
        conn.commit()

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
        return results

def clickedPagesForGameAndUser(game_uuid, userid):
    """ input:  wikipediagame: uuid, userid
                output: number of cliked pages for a given game and userid
                """
    server='localhost'
    conn = None

    try:
        conn = MySQLdb.Connection(server, 'saguinag', 'dsg1!0xB', 'wikipediagame')
        cursor = conn.cursor()

        #query ="SELECT /*uuid,end_page,*/ w.page_id from wikipediagame.game_game \
        query ="select count(clicked_page) \
                from game_click \
                WHERE game_uuid='%s' AND userid='%s';" % game_uuid

        cursor.execute(query)
        conn.commit()

        results = cursor.fetchall()

    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    finally:
        if conn:
            conn.close()
        return results
    """ Done """
 
def usersPlayedNFinishedGame( game_uuid ):
    """ input:  wikipediagame uuid
        output: users that played and finished the game & nbr of clicks
                it took them.
        """
    server='localhost'
    conn = None
        
    try:
        conn = MySQLdb.Connection(server, 'saguinag', 'dsg1!0xB', 'wikipediagame')
        cursor = conn.cursor()
        """
        query ="select wc.userid \
                from game_click AS wc \
                inner JOIN (SELECT userid, uuid, start_page, end_page, gc.clicked_page \
                      from game_game \
                      JOIN wikipediagame.game_click gc ON uuid=gc.game_uuid \
                      WHERE uuid='%s' AND gc.clicked_page=start_page\
                     ) as started \
                ON wc.game_uuid=started.uuid And wc.userid=started.userid \
                Where wc.clicked_page=started.end_page;" % game_uuid
        """
        ## can we split users that played the same game multiple times?
        """  query ="Select UID.userid, count(gc2.clicked_page) from \
                (select wc.game_uuid, wc.userid \
                from game_click AS wc \
                inner JOIN (SELECT userid, uuid, start_page, end_page, gc.clicked_page \
                      from game_game \
              JOIN wikipediagame.game_click gc ON uuid=gc.game_uuid \
                      WHERE uuid='%s' AND gc.clicked_page=start_page\
                     ) as started \
                ON wc.game_uuid=started.uuid And wc.userid=started.userid \
                Where wc.clicked_page=started.end_page \
                ) As UID Inner Join game_click gc2 ON gc2.game_uuid = UID.game_uuid \
                AND gc2.userid = UID.userid group by UID.userid;" % game_uuid
        """
        query ="SELECT gc.game_uuid, gc.userid, gg.start_page, gg.end_page, gc.clicked_page \
                from game_click as gc \
                JOIN game_game as gg ON gg.uuid=gc.game_uuid \
                WHERE gc.game_uuid='%s' AND gc.userid='Guest0C1CE13FC98742B58C90B35DC';" % game_uuid

        cursor.execute(query)
        conn.commit()

        results = cursor.fetchall() 
    
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    finally:
        if conn:
            conn.close()
        
    return results    
     
def ssspScoreToEndpageIn(game_uuid):
    server='localhost'
    conn = None
    
    try:
        conn = MySQLdb.Connection(server, 'saguinag', 'dsg1!0xB', 'wikipedia')
        cursor = conn.cursor()
        
        #query ="SELECT /*uuid,end_page,*/ w.page_id from wikipediagame.game_game \
        query ="SELECT w.page_id from wikipediagame.game_game \
                join wikipedia.page w ON w.page_title=end_page \
                WHERE uuid='%s' AND w.page_namespace=0;" % game_uuid

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


def humanPaths4GameStartingAt(srcPageId,limit):
    server='localhost'
    conn = None
    #print '-----------------------------------\n',limit
   
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


def gamesWithSourceNode(srcPageId,limit = -1):
    server='localhost'
    conn = None
    
    try:
        conn = MySQLdb.Connection(server, 'saguinag', 'dsg1!0xB', 'wikipedia')
        cursor = conn.cursor()
        if limit<0:
            print limit
            query = "SELECT W.page_id, uuid, W2.page_id \
                     FROM wikipediagame.game_game \
                     JOIN wikipedia.page W ON W.page_title=start_page \
                     JOIN wikipedia.page W2 ON W2.page_title=end_page \
                     WHERE W.page_id='%s' AND W2.page_namespace = 0;" % (srcPageId)
        else :
            query = "SELECT W.page_id, uuid, W2.page_id \
                 FROM wikipediagame.game_game \
                 JOIN wikipedia.page W ON W.page_title=start_page \
                 JOIN wikipedia.page W2 ON W2.page_title=end_page \
                 WHERE W.page_id='%s' AND W2.page_namespace=0 LIMIT %d ;" % (srcPageId,limit)


        cursor.execute(query)
        conn.commit()
        #print cursor.rowcount
        results = cursor.fetchall()
        print len(results) 
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
    tstInt = 3

    if tstInt == 0:
        for row in gamesWithSourceNode('1018340',10):
            print row
    elif tstInt == 1:
        for row in humanPaths4GameStartingAt('1018340',10):
            print row
    elif tstInt == 2: # find games played and finished by user 
        for row in usersPlayedNFinishedGame('2f8aa3635a8749f1b01af5d0e0af8d42'):
            print row
    elif tstInt == 3: # game completed by 
        for row in usersPlayedNFinishedGame('2a913d67cde840bc84306e5461b977b0'):
            print row
            
