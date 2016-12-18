from lxml import etree
import stats

class Server:
    pass

def escape_chars(string):
    rep_chr = {'&quot;': '"', '&#39;': "'", '&lt;': '<', '&gt;': '>',
            '&amp;': '&', '*': '\\*', '_': '\\_', '~': '\\~', '`': '\\`'}
    for i, j in rep_chr.items():
        string = string.replace(i, j)
    return string.strip()

def sv_list(track_players=False):
    tree = None
    try:
        url = 'http://dpmaster.deathmask.net/?game=openarena&xml=1&nocolors=1'
        tree = etree.parse(url)
        #  tree = etree.parse('test/dpmaster.xml') # DEBUG
    except:
        return

    servers = []
    human = 'player[ping/text()!=0]'
    # append also 0-players servers, useful in stats
    for server in tree.xpath('//server'):
        sv = Server()
        try:
            sv.name = escape_chars(server.xpath('./name/text()')[0])
            sv.hostname = escape_chars(server.xpath('./hostname/text()')[0])
            sv.map = escape_chars(server.xpath('./map/text()')[0])
            try:
                sv.players = [escape_chars(x) for x in
                        server.xpath('.//%s/name/text()' % human)[:]]
            except:
                sv.players = 0
        except:
            #print('Error in xml, missing information.')
            continue
        servers.append(sv)
    servers = sorted(servers, key=lambda sv: len(sv.players), reverse=True)

    # update stats
    if track_players:
        stats.Update(servers)

    player_count = 0
    for sv in servers:
        player_count += len(sv.players)
    message = '\n__ **OpenArena** server list (*{}*  online players) __\n\n'.format(player_count)
    hidden_sv = 0
    for sv in servers:
        # do not show 0-players server
        if len(sv.players) < 1:
            continue
        if len(sv.players) == 1:
            plinfo = 'player'
        else:
            plinfo = 'players'
        new_msg = '**{}** ({}) [{}] has `{}` {}:\n'.format(sv.name, sv.hostname, sv.map, len(sv.players), plinfo)
        new_msg += '|\t {} \t|\n\n'.format('\t|\t'.join(sv.players))
        #TODO: message too large: divide into multiple messages?
        if (len(message + new_msg) < 1970):
            message += new_msg
        else:
            hidden_sv += 1
    if hidden_sv:
        message += '+{} servers with players'.format(hidden_sv)
    return message
