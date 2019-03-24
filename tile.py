
from random import shuffle
import numpy as np
import random as rnd

class tile():
    def __init__(self, tid):
        self.tid = tid
        self.color_key = [
            "black",
            "white",
            "blue",
            "red",
            "green",
            "yellow"]
    def get_id(self):
        return self.tid
    def return_color(self):
        return self.color_key[self.tid]

class bag():
    def __init__(self, tiletypes):
        self.bag_status = [[],[],[]]
        self.tiletypes = tiletypes

        # 0: tiles in bag
        # 1: tiles out of bag
        # 2: tiles in hand // temporarely out of bag
    def add_tile(self,ioo, tid):
        temptile = tile(tid)
        self.bag_status[ioo].append(temptile)
    def add_tile_series(self,ioo, tserie):
        for tile in tserie:
            self.add_tile(ioo, tile)
    def add_tile_amount(self,tid,ioo,amount):
        series = []
        for x in range(amount):
            series.append(tid)
        self.add_tile_series(ioo,series)
    def print_bag(self, ioo,idoc):
        for tile in self.bag_status[ioo]:
            if idoc == 0:
                print tile.get_id()
            else:
                print tile.return_color()
    def search_tile_id(self, ioo, tid):
        counter = 0
        for tile in self.bag_status[ioo]:
            if tile.get_id() == tid:
                return counter
            counter+=1
        return -1
    def has_tile_id(self, ioo, tid):
        for tile in self.bag_status[ioo]:
            if tile.get_id() == tid:
                return True
        return False
    def move_tile(self, ioo1, ioo2,tid):
        if self.has_tile_id(ioo1,tid):
            ttid = self.search_tile_id(ioo1,tid)
            # print ttid
            temptile = self.bag_status[ioo1][ttid]
            del self.bag_status[ioo1][ttid]
            self.bag_status[ioo2].append(temptile)
            # print "bag doesn't contain tid: %s" %(tid,)
    def move_tile_series(self, ioo1,ioo2,tidseries):
        for tid in tidseries:
            self.move_tile(ioo1,ioo2,tid)
    def remove_tile(self,ioo,tid):
        if self.has_tile_id(ioo,tid):
            ttid = self.search_tile_id(ioo,tid)
            # print ttid
            temptile = self.bag_status[ioo][ttid]
            del self.bag_status[ioo][ttid]
        # else: 
        #     print "bag doesn't contain tid: %s" %(tid,)
    def remove_tile_series(self,ioo,tidseries):
        for tid in tidseries:
            self.remove_tile(ioo,tid)
    def shuffle_bag(self):
        for list in self.bag_status:
            shuffle(list)
    def draw_tiles(self, ioo1,ioo2, amount):
        for x in range(amount):
            self.bag_status[ioo2].append(self.bag_status[ioo1].pop(0))
        return self.bag_status[ioo2]
    def end_action(self):
        for x in range(len(self.bag_status[2])):
            self.bag_status[0].append(self.bag_status[2].pop(0))
        self.shuffle_bag()
    def count_id(self,ioo,tid):
        counter = 0
        for x in self.bag_status[ioo]:
            if x.get_id() == tid:
                counter += 1
        return counter
    def bag_composition(self,ioo):
        composition = []
        for x in range(self.tiletypes):
            composition.append(self.count_id(ioo,x))
        return composition
    def tile_amount(self):
        return len(self.bag_status[0])+len(self.bag_status[1])
    def invert_order(self, ioo):
        inverted_list = []
        for i in self.bag_status[ioo]:
            inverted_list.insert(0,i)
        self.bag_status[ioo]=inverted_list
    def composition_order(self,composition):
        order = [0]*self.tiletypes
        for x in range(len(composition)):
            comp = 0
            for y in composition:
                if composition[x] >=y:
                    comp = comp + 1
            order[x] = self.tiletypes-comp
            composition[x]+= 1
        return order
 
class continious_play_2():
    def __init__(self,tiletypes):
        self.tiletypes = tiletypes
        self.turn = 0
        self.bb = bag(tiletypes)
        self.bb.add_tile_amount(0,0,5)
        self.bb.add_tile_amount(1,0,5)
        self.bb.add_tile_amount(2,0,5)
        self.bb.add_tile_amount(3,0,5)
        self.bb.shuffle_bag()
        self.sb = bag(tiletypes)
        self.sb.add_tile_amount(0,0,3)
        self.sb.add_tile_amount(1,0,3)
        self.sb.add_tile_amount(2,0,3)
        self.sb.add_tile_amount(3,0,3)
        self.sb.shuffle_bag()
    def moveTile(self,frombag,tobag,tile):
        if frombag.has_tile_id(0,tile):
            frombag.remove_tile(0,tile)
            tobag.add_tile(0,tile)
    def playTurn(self,sbag,bbag,bbag_series_length,):
        #mogelijke acties & selecteur vermoedelijk beste - Score heureustiek X007
        # > bepaal aantal sbag blokken
        #       - amount_predictor(self,bbag,bbag_series_length,sbag)
        amount = self.amount_predictor(bbag,bbag_series_length,sbag)
        # > pak startblokken
        biglist = bbag.draw_tiles(0,2,bbag_series_length)
        smalllist =  sbag.draw_tiles(0,2,amount[1])

        # >> bepaal mogelijke match posities voor sbag - sequentie
        #       - running_match(self,sbag,smalllist,bbag,biglist)
        topscore = self.running_match(sbag,smalllist,bbag,biglist)
        # >>> bepaal score voor deze match positie - Score heureustiek X007
        #       -scoreHeureustiek(self,bag_composition)
        #       -simulate_bag_status(self,bag,hit_miss_pattern)
        # >>>> bepaal hoe je match eruit zien = per bloktype #+, #-
        #       -match(self,smalllist,biglist,position)
        #       -compare1(self,tile1,tile2)
        #voer vermoedelijk beste actie uit 
        # if topscore[2]==0:
        #     hit_miss_pattern = self.match(smalllist,biglist,topscore[1])
        # else:
        #     sbag.invert_order(2)
        
        # self.permutations(smalllist,len(smalllist))[topscore[2]]
        hit_miss_pattern = self.match(self.permutations(smalllist,len(smalllist))[topscore[2]],biglist,topscore[1])

        #MAAAK COMPARISSON ZICHTBAAR
        # self.print_compare(topscore,self.permutations(smalllist,len(smalllist))[topscore[2]],biglist)
        #MAAAK COMPARISSON ZICHTBAAR

        self.manipulate_bag_status(sbag,bbag,hit_miss_pattern)
        #bepaal score - score heureustiek X001
        #genereer output

        return self.print_turn(sbag,bbag,hit_miss_pattern,amount[1]) 

        
        #zet klaar voor nieuwe beurt
    def print_turn(self,sbag,bbag,hit_miss_pattern,amount):
        TS = []
        #sbag compostiion
        TS.extend(sbag.bag_composition(0))
        #score
        TS.append(self.scoreHeureustiek(sbag,sbag.bag_composition(0)))
        #aantal blokskes
        TS.append(amount)
        #totaal aantal hits
        TS.append(np.sum(hit_miss_pattern[0]))
        #totaal aantal misses
        TS.append(np.sum(hit_miss_pattern[1]))
        #welke hits
        TS.extend(hit_miss_pattern[0])
        #welke misses
        TS.extend(hit_miss_pattern[1])
        #bbag composition
        TS.extend(bbag.bag_composition(0))
        #totaal aantal bbag tiles
        TS.append(bbag.tile_amount())
        #totaal aantal sbag tiles
        TS.append(sbag.tile_amount())
        #totaal aantal tiles
        TS.append(bbag.tile_amount()+sbag.tile_amount())
        return TS
    def amount_predictor(self,bbag,bbag_series_length,sbag):
        averages = []
        for i in range(1,bbag_series_length):
            average = []
            if i <= sbag.tile_amount():
                k=0
                if i <= 4:
                    k = 50
                elif i <= 6:
                    k = 3
                else:
                    k=1
                for x in range(k):
                    biglist = bbag.draw_tiles(0,2,bbag_series_length)
                    smalllist = sbag.draw_tiles(0,2,i)
                    average.append(self.running_match(sbag,smalllist,bbag,biglist)[0])
                    bbag.end_action()
                    sbag.end_action()
                averages.append(average)



        averages_calc = []
        for i in averages:
            averages_calc.append(np.mean(i))

        # print averages_calc

        max_mean_loc = [0,0]
        for i in range(1,len(averages_calc)):
            if averages_calc[i] >= max_mean_loc[0]:
                max_mean_loc[0] = averages_calc[i]
                max_mean_loc[1] = i
        return max_mean_loc
    def permutations(self, smalllist,amount):
        goalarray = []
        temparray = []
        temparray.append(smalllist[0])
        goalarray.append(temparray)
        biggoalarray = []
        if amount == 1:
            biggoalarray = goalarray

        for n in range(1,amount):
            for x in range((2**(n-1))-1,(2**n)-1):
                original = goalarray[x]
                modifier = [smalllist[n]]
                prestr=original+modifier
                poststr=modifier+original
                goalarray.append(prestr)
                goalarray.append(poststr)
                if n == amount-1:
                    biggoalarray.append(prestr)
                    biggoalarray.append(poststr)

        return biggoalarray
    def running_match(self,sbag,smalllist,bbag,biglist):
        psmalllist = self.permutations(smalllist,len(smalllist))
        topscore = [0,0,0]
        for permutation in range(len(psmalllist)):
            for position in range(len(biglist)-len(smalllist)+1):
                hit_miss_pattern = self.match(psmalllist[permutation],biglist, position)
                bag_composition = self.simulate_bag_status(sbag,hit_miss_pattern)
                points = self.scoreHeureustiek(sbag,bag_composition)
                if points > topscore[0]:
                    topscore = [points, position,permutation]
        # smalllist.reverse()
        # for position in range(len(biglist)-len(smalllist)+1):
        #     hit_miss_pattern = self.match(smalllist,biglist, position)
        #     bag_composition = self.simulate_bag_status(sbag,hit_miss_pattern)
        #     points = self.scoreHeureustiek(sbag,bag_composition)            
        #     if points > topscore[0]:
        #         topscore = [points, position,1]
        return topscore
    def scoreHeureustiek(self,bag,bag_composition):
        # final_composition = np.add(bag.bag_composition(0),bag.bag_composition(2))
        order = bag.composition_order(bag_composition)
        score = 0
        for x in order:
            if x <= 1:
                score += bag_composition[x]
            else:
                score -= bag_composition[x]
        return score
    def simulate_bag_status(self,bag,hit_miss_pattern):
        #-------------------------------------------------------------------------
        #- dit past dus aan afhankelijk van de spelregels die je wilt gebruiken. -
        #-------------------------------------------------------------------------
        #X007: +-1 bij succes / -1 random bij failure / dynamische zak
        final_composition = np.add(bag.bag_composition(0),bag.bag_composition(2))
        #+-1 bij succes
        order = bag.composition_order(final_composition.tolist())
        for x in range(len(order)):
            if order[x] <= 1:
                final_composition[x] += hit_miss_pattern[0][x]
            else:
                final_composition[x] -= hit_miss_pattern[0][x]

        #-1 random bij failure
        failamount = np.sum(hit_miss_pattern[1])
        for x in range(failamount): 
            order = bag.composition_order(final_composition)
            if bag.tile_amount() >= 12:
                final_composition[order.index(0)] -= 1
            elif bag.tile_amount() <12:
                final_composition[order.index(self.tiletypes-1)] +=1

        return final_composition.tolist()
    def manipulate_bag_status(self,sbag,bbag,hit_miss_pattern):
        #-------------------------------------------------------------------------
        #- dit past dus aan afhankelijk van de spelregels die je wilt gebruiken. -
        #-------------------------------------------------------------------------
        bbag.end_action()
        sbag.end_action()
        #X007: +-1 bij succes / -1 random bij failure / dynamische zak
        #+-1 bij succes
        final_composition = sbag.bag_composition(0)
        order = sbag.composition_order(final_composition)
        for x in range(len(order)):
            if order[x] <= 1:
                sbag.add_tile_amount(x,0,hit_miss_pattern[0][x])
                bbag.remove_tile_series(0,[x]*hit_miss_pattern[0][x])
            else:
                bbag.add_tile_amount(x,0,hit_miss_pattern[0][x])
                sbag.remove_tile_series(0,[x]*hit_miss_pattern[0][x])

        #-1 random bij failure
        failamount = np.sum(hit_miss_pattern[1])
        for x in range(failamount): 
            final_composition = sbag.bag_composition(0)
            order = sbag.composition_order(final_composition)
            if sbag.tile_amount() >= 12:
                sbag.remove_tile(0,order.index(0))
                bbag.add_tile(0,order.index(0))
            elif sbag.tile_amount() <12:
                sbag.add_tile(0,order.index(self.tiletypes-1))
                bbag.remove_tile(0,order.index(self.tiletypes-1))
    def match(self,smalllist,biglist,position):
        hitMiss = [[0]*self.tiletypes,[0]*self.tiletypes]
        for a in range(len(smalllist)):
            if self.compare1(smalllist[a],biglist[a+position]):
                hitMiss[0][smalllist[a].get_id()]+= 1
            else: #en nu kunde dus ook punten verliezen
                hitMiss[1][smalllist[a].get_id()]+= 1
        return hitMiss
    def compare1(self,tile1,tile2):
        if tile1.get_id() == tile2.get_id():
            return True
        else:
            return False
    def print_compare(self,topscore,smalllist,biglist):
        for i in range(len(biglist)):
            if i >= topscore[1] and i < topscore[1]+len(smalllist):
                print "%s - %s" % (biglist[i].get_id(),smalllist[i-topscore[1]].get_id())
            else:
                print biglist[i].get_id()

for xxy in range(50):

    ng = continious_play_2(4)
    info = []
    info.append(0)
    info.extend(ng.print_turn(ng.sb,ng.bb,[[0]*ng.tiletypes,[0]*ng.tiletypes],0))
    print info

    for n in range(50):
        info = []
        info.append(n)
        info.extend(ng.playTurn(ng.sb,ng.bb,10))
        print info

    print ""
    print ""

# for n in range(5):
#     temp = [rnd.randrange(100),rnd.randrange(100),rnd.randrange(100),rnd.randrange(100)]
#     print " new test"
#     print temp
#     print ng.sb.composition_order(temp)
#     print ""