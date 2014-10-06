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
where game_click.game_uuid = completedgames.gcuuid and game_click.userid = completedgames.cguserid group by game_uuid, userid LIMIT 20;"
    
    query6A="(  select clicks.uuid as gcuuid, clicks.userid as cguserid \
    from ( \
    select uuid, game_game.end_page \
    from game_game \
    where game_game.start_page = 'Columbia_university' group by uuid, end_page\
    ) AS endpage, \
    ( \
    select uuid, clicked_page, game_click.userid \
    from game_click, game_game \
    where game_game.uuid = game_click.game_uuid and game_game.start_page = 'Columbia_university' \
    ) AS clicks \
    where endpage.uuid = clicks.uuid and clicks.clicked_page = endpage.end_page \
    ) completedgames;"
    
    query7= "(  select clicks.uuid as gcuuid, clicks.userid as cguserid \
    from ( select uuid, end_page,W.page_id \
    from game_game \
    JOIN wikipedia.page W ON W.page_title=game_game.start_page \
    where W.page_id = '7555441' group by uuid, end_page\
    ) AS endpage, \
    ( \ "
    query8="select uuid, clicked_page, game_click.userid, WP.page_id \
    from game_click, game_game \
    JOIN wikipedia.page WP ON WP.page_title=game_game.start_page \
    where game_game.uuid = game_click.game_uuid and WP.page_id = '7555441' \
    LIMIT 20; "
    print 'user gid start_page end_page clicked_page count '