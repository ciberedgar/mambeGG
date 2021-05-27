#Es el encargado de renderizar las views o el endpoint
#del api en este caso.
##Un enpoint es un \algo osea, una direccion a la que quieres ir en tu web server
from django.shortcuts import render
from django.http import HttpResponse
from riotwatcher import LolWatcher, ApiError
import time

# Create your views here.
def r404(request):
    return render(request, '404.html')

def homep(request):
    return render(request, 'untitled.html')

def index(request):
    if request.method=='POST':
        # golbal variables
        api_key = 'RGAPI-97e244c3-86b1-460b-bf9e-333d33757ff1'
        watcher = LolWatcher(api_key)
        my_region = 'LA1'
        try:
            summoner = request.POST.get('nombre')

            me = watcher.summoner.by_name(my_region, summoner)
            liga = watcher.league.by_summoner(my_region, me['id'])
            
            ligaimg1 = "unranked" + ".png"
            ligaimg2 = "unranked" + ".png"
            porcentajef = 100
            porcentajes = 100
            if liga != []:
                ligaimg1 = str.capitalize(liga[0]['tier']) + ".png"
                porcentajef = int(liga[0]['wins']/int(liga[0]['wins'] + liga[0]['losses']) * 100)
                if len(liga) > 1:
                    ligaimg2 = str.capitalize(liga[1]['tier']) + ".png"
                    porcentajes = int(liga[1]['wins']/int(liga[1]['wins'] + liga[1]['losses']) * 100)
                else:
                    ligaimg2 = "unranked" + ".png"
                    porcentajes = 100
            icon = 'http://ddragon.leagueoflegends.com/cdn/11.8.1/img/profileicon/' +str(me['profileIconId']) + '.png'
            ##########################################################################################################################
            ##DATA DRAGON(INFORMACION ESTATICA)
            latest = watcher.data_dragon.versions_for_region('na1')['n']['champion']
            static_spell_list = watcher.data_dragon.summoner_spells(latest, 'en_US')
            static_champ_list = watcher.data_dragon.champions(latest, True, 'en_US')
            champ_dict = {}
            imgchamp_dict = {}
            spell_dict = {}
            for key in static_champ_list['data']:
                row = static_champ_list['data'][key]
                champ_dict[row['key']] = row['id']
                imgchamp_dict[row['key']] = row['image']['full']
            
            for key in static_spell_list['data']:
                row = static_spell_list['data'][key]
                spell_dict[row['key']] = row['id']
            ################################################################################################
            ##DATOS DE PARTIDAS
            my_matches = watcher.match.matchlist_by_account(my_region, me['accountId'], begin_index = 0, end_index = 10)
            n = 0
            for row in my_matches['matches']:
                #print(str(row['champion']) + ' ' + champ_dict[str(row['champion'])] + ' ' + 'http://ddragon.leagueoflegends.com/cdn/11.8.1/img/champion/' + imgchamp_dict[str(row['champion'])])
                row['championName'] = champ_dict[str(row['champion'])]
                row['ident'] = n
                n = n + 1

            #print(my_matches['matches'])
            #pd.DataFrame(my_matches['matches'])                
            ############################################################################################################
            d={}
            k = 0
            for i in my_matches['matches']:
                n = 0
                participants = []
                #print(my_matches['matches'][n])
                last_match = my_matches['matches'][k]
                match_detail = watcher.match.by_id(my_region, last_match['gameId'])
                #print(last_match['gameId'])
                for row in match_detail['participants']:
                    participants_row = {}
                    participants_row['win'] = row['stats']['win']
                    participants_row['duration'] = round(match_detail['gameDuration']/60,2)
                    participants_row['champion'] = row['championId']
                    participants_row['spell1'] = row['spell1Id']
                    participants_row['spell2'] = row['spell2Id']
                    participants_row['win'] = row['stats']['win']
                    participants_row['kills'] = row['stats']['kills']
                    participants_row['deaths'] = row['stats']['deaths']
                    participants_row['assists'] = row['stats']['assists']
                    participants_row['totalDamageDealt'] = row['stats']['totalDamageDealt']
                    participants_row['goldEarned'] = row['stats']['goldEarned']
                    participants_row['champLevel'] = row['stats']['champLevel']
                    participants_row['minions'] = row['stats']['totalMinionsKilled']
                    participants_row['item0'] = row['stats']['item0']
                    participants_row['item1'] = row['stats']['item1']
                    participants_row['item2'] = row['stats']['item2']
                    participants_row['item3'] = row['stats']['item3']
                    participants_row['item4'] = row['stats']['item4']
                    participants_row['item5'] = row['stats']['item5']
                    participants_row['item6'] = row['stats']['item6']
                    s = match_detail['participantIdentities'][n]['player']['summonerName']
                    
                    participants_row['summoner'] = s
                    participants_row['summonerId'] = match_detail['participantIdentities'][n]['player']['summonerId']
                    participants_row['summonerIcon'] = match_detail['participantIdentities'][n]['player']['profileIcon']
                    participants.append(participants_row)
                    #print('http://ddragon.leagueoflegends.com/cdn/11.8.1/img/profileicon/' + str(participants_row['SummonerIcon']) + '.png')
                    n = n + 1
                d[k] = participants
                #pd.DataFrame(d[k])
                k = k + 1

            #print(d['t0'][1]['Summoner'])

            historialUsuario = {}
            h = 0
            for x in d:
                p = 0
                while p < 10:
                    if me['id'] == d[x][p]['summonerId']:
                        #print("PARTIDA" + x)
                        #print(d["%s" %x][p])
                        f = d[x][p]
                        historialUsuario[h] = f;
                        break;
                    p = p + 1
                h = h + 1
            #pd.DataFrame(d[0])        
            #pd.DataFrame(historialUsuario).T
    ################################################################################################################
            n = 0
            for row in my_matches['matches']:
                row['championName'] = champ_dict[str(row['champion'])]
                row['kills'] = historialUsuario[n]['kills']
                row['deaths'] = historialUsuario[n]['deaths']
                row['assists'] = historialUsuario[n]['assists']
                row['spell1'] = historialUsuario[n]['spell1']
                row['spell2'] = historialUsuario[n]['spell2']
                row['item1'] = historialUsuario[n]['item1']
                row['item2'] = historialUsuario[n]['item2']
                row['item3'] = historialUsuario[n]['item3']
                row['item4'] = historialUsuario[n]['item4']
                row['item5'] = historialUsuario[n]['item5']
                row['item6'] = historialUsuario[n]['item6']
                row['dmg'] = historialUsuario[n]['totalDamageDealt']
                row['win'] = historialUsuario[n]['win']
                row['minions'] = historialUsuario[n]['minions']
                row['oro'] = historialUsuario[n]['goldEarned']
                row['p1'] = d[n][0]['summoner']
                row['p2'] = d[n][1]['summoner']
                row['p3'] = d[n][2]['summoner']
                row['p4'] = d[n][3]['summoner']
                row['p5'] = d[n][4]['summoner']
                row['p6'] = d[n][5]['summoner']
                row['p7'] = d[n][6]['summoner']
                row['p8'] = d[n][7]['summoner']
                row['p9'] = d[n][8]['summoner']
                row['p10'] = d[n][9]['summoner']
                row['i1'] = d[n][0]['summonerIcon']
                row['i2'] = d[n][1]['summonerIcon']
                row['i3'] = d[n][2]['summonerIcon']
                row['i4'] = d[n][3]['summonerIcon']
                row['i5'] = d[n][4]['summonerIcon']
                row['i6'] = d[n][5]['summonerIcon']
                row['i7'] = d[n][6]['summonerIcon']
                row['i8'] = d[n][7]['summonerIcon']
                row['i9'] = d[n][8]['summonerIcon']
                row['i10'] = d[n][9]['summonerIcon']
                row['duration'] = historialUsuario[n]['duration']
                n = n + 1
            #pd.DataFrame(my_matches['matches'])
            
            #########################################CALCULOS
            n = 0
            kda = []
            for o in my_matches['matches']:
                kda_row = {}
                if o['deaths'] != 0:
                    kda_row = round((o['kills'] + o['assists']) / o['deaths'],2)
                else:
                    kda_row = 'Perfecto'
                n+1
                kda.append(kda_row)

            n = 0
            kda = []
            cs = []
            cs10 = []
            for o in my_matches['matches']:
                kda_row = {}
                cs_row = {}
                cs10_row = {}
                if o['deaths'] != 0:
                    kda_row = round((o['kills'] + o['assists']) / o['deaths'],2)
                else:
                    kda_row = 'Perfecto'
                cs_row = round(o['minions']/o['duration'],2)
                cs10_row = round(o['minions']/10,2)
                n+1
                kda.append(kda_row)
                cs.append(cs_row)
                cs10.append(cs10_row)

            n = 0
            for row in my_matches['matches']:
                row['kda'] = kda[n]
                row['cs'] = cs[n]
                row['cs10'] = cs10[n]
                n = n+1

            timest = []
            n = 0
            g1 = 0
            g2 = 0
            g3 = 0
            prom = 0
            prokda = 0
            prodmg = 0
            proro = 0
            w = 0
            l = 0
            for x in my_matches['matches']:
                timest_row = {}
                timest_row = time.strftime("%D", time.localtime((x['timestamp']/1000)))
                timest.append(timest_row)

            for row in my_matches['matches']:
                row['date'] = timest[n]
                n = n+1
                f = ('http://ddragon.leagueoflegends.com/cdn/11.11.1/img/spell/' + spell_dict[str(row['spell1'])] + '.png')
                g = ('http://ddragon.leagueoflegends.com/cdn/11.11.1/img/spell/' + spell_dict[str(row['spell2'])] + '.png')
                row['spell1'] = f
                row['spell2'] = g
                if row['lane'] == 'NONE':
                    row['lane'] = 'ARAM'
                g1 = g1 + row['kills']
                g2 = g1 + row['deaths']
                g3 = g1 + row['assists']
                prom = prom + row['minions']
                if row['kda'] != 'Perfecto':
                    prokda = prokda + row['kda']
                prodmg = prodmg + row['dmg']
                proro = proro + row['oro']
                if row['win'] == True:
                    w = w + 1
                else:
                    l = l + 1
            prom = prom/10
            prokda = prokda/10
            prodmg = prodmg/10
            proro = proro/10

            if g1 > g2 and g1 > g3:
                ph = 'Matar y carrear al equipo'
            if g2 > g1 and g2 > g3:
                ph = 'Morir mucho'
            if g3 > g1 and g3 > g2:
                ph = 'Asistir a sus compañeros'
            else:
                ph = 'null'
            return render(request, 'index.html', {"results":me, "icon":icon, "liga":liga, "soloimg":ligaimg1, "fleximg":ligaimg2,
            "porcentajes":porcentajes, "porcentajef":porcentajef, "pusuario":historialUsuario, "datospartidas":d, "matches":my_matches, "gk":g1
            , "gd":g2, "ga":g3, "prom":prom, "prokda":prokda, "prodmg":prodmg, "proro":proro, "proh":ph, "win":w, "lose":l})
        except ApiError as e:
            if e.response.status_code == 404:
                return render(request, '404i.html')
    else:
        #print(me)
       # print('id:' + ' ' + me['id'])
       # print('name:' + ' ' + me['name'])
       # print('level:' + ' ' + str(me['summonerLevel']))
       # print(icon)
        return render(request, 'untitled.html')


def handler404(request, *args, **argv):
    return render(request, '404.html')