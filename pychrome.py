#google-chrome --remote-debugging-port=9222

import pychrome
import json
from collections import OrderedDict
from operator import getitem

guilds = {}
guilds_gvg = {}

toFile = True

class EventHandler:
    def __init__(self, tab, world):
        self.tab = tab
        self.world = world
        self.lastMapOpened = False

    def handleRequest(self, requestId, **kwargs):
        try:
            request = kwargs.get('request')
            url = request.get('url')

            if self.world in url:
                headers = request.get('headers')
                postdata = request.get('postData', '')

            if len(postdata) > 10:
                postdatalist = json.loads(postdata)

        except Exception as e:
            pass

    def handleResponse(self, requestId, **kwargs):
        try:
            response = kwargs.get('response')
            url = response.get('url')

            if self.dest in url:
                mt = response.get('mimeType')

            if 'json' in mt:
                pass

        except Exception as e:
            pass

    def handleLoading(self, requestId, **kwargs):
        makeMMRTable()

        try:
            body = self.tab.Network.getResponseBody(requestId=requestId)
            responses = json.loads(body.get('body'))

        except Exception as e:
            responses = []

        for r in responses:
            rc = r.get('requestClass')
            rm = r.get('requestMethod')
            rd = r.get('responseData')

            # get info about what map was last open to check for errors later
            if rc == "ClanBattleService" and rm == "getProvinceDetailed":
                province_detailed = rd.get('province_detailed')
                self.lastMapOpened = province_detailed.get('era')

            # handle guild ranking
            if rc == "RankingService":
                cat = rd.get('category')

                if cat == "clan_battle_clan_global":
                    rankings = rd.get('rankings')
                    processClanRankings(rankings)

                if cat == "clan_battle_clan_province":
                    rankings = rd.get('rankings')
                    processClanProvinceRankings(self.lastMapOpened, rankings)



def processClanRankings(data):
    for guild in data:
        _id = guild["clan"]["id"]
        prestige = guild["prestige"]
        name = guild["clan"]["name"]
        prestige_lvl = guild["level"] * 25
        guilds[_id] = {"_id" : _id, "prestige" : prestige, "prestige_lvl" : prestige_lvl, "name" : name}

def processClanProvinceRankings(lastMapOpened, data):
    guilds_gvg[lastMapOpened] = {}

    for guild in data:
        _id = guild["clan"]["id"]
        powerSum = guild["powerSum"]

        guilds_gvg[lastMapOpened][_id] = {"_id" : _id, "powerSum": powerSum}

def makeMMRTable():
    totalGvGPRestige = {}

    for key, age in guilds_gvg.items():
        for key, guild in age.items():
            _id = guild["_id"]

            totalGvGPRestige[_id] = totalGvGPRestige.get(_id, 0) + guild["powerSum"]

    for key, guild in guilds.items():
        guilds[key]["MMR"] = (guild["prestige"] - guild["prestige_lvl"] - totalGvGPRestige.get(guild["_id"], 0))/18

    print(chr(27) + "[2J")
    if len(guilds_gvg) >= 13:
    #if len(guilds_gvg) >= 1:
        res = OrderedDict(sorted(guilds.items(), key = lambda x: getitem(x[1], 'MMR'), reverse = True))
        
        if toFile == False:
            print "=== BEGINNING OF THE MMR TABLE ==="
            for key, item in res.items():
                print item["MMR"], item["name"]
            print "=== END of the table ==="

        else:
            r = json.dumps(res, sort_keys=True)
            #loaded_json = json.loads(r)

            #with open('mmr_data.json', 'w') as json_file:
            #    json.dump(loaded_json, json_file)

            file = "mmr_data.json"
            f = open(file, "w")
            f.write(r)
            f.close()

            print file

    print "-------"
    print "GvG MAPS:", len(guilds_gvg),"/ 13"
    print "Guilds:", len(guilds)
    print "-------"

def main():
    browser = pychrome.Browser(url='http://127.0.0.1:9222')
    tabs = browser.list_tab()
   
    for tab in tabs:
        tab.start()
        node = tab.DOM.getDocument()
        url = node['root']['documentURL']
        
        world, domain = url[8:].split('.', 1)

        if 'forgeofempires.com/game' in url:
            eh = EventHandler(tab, world)
            tab.Network.responseReceived = eh.handleResponse
            tab.Network.loadingFinished = eh.handleLoading
            tab.Network.requestWillBeSent = eh.handleRequest

            tab.Network.enable()
        
if __name__ == '__main__':
    main()
    raw_input()