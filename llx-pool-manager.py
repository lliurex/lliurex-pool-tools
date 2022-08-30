#!/bin/python3
import sys
import glob
import os
import datetime

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

import colorama
BLACK=colorama.Fore.BLACK
BLUE=colorama.Fore.BLUE
CYAN=colorama.Fore.CYAN
GREEN=colorama.Fore.GREEN
YELLOW=colorama.Fore.YELLOW
WHITE=colorama.Fore.WHITE
RED=colorama.Fore.RED
MAGENTA=colorama.Fore.MAGENTA

class LlxPoolManager:

    ACTIONS_DIR="/home/lliurex/llx-pool-manager/"
    EXIT=-255
    BACK_TO_POOL_SELECTION=-200

    DEBUG=True
    USE_COLORS=True

    def __init__(self,argv=None):

        if LlxPoolManager.USE_COLORS:
            colorama.init(autoreset=True)

        self.actions={}
        self.executed_actions={}

        self.parse_actions_dir()
        self.print_welcome()

    #def __init__

    def dprint(self,data):

        if LlxPoolManager.DEBUG:
            print("[LPM] %s"%str(data))

    #def dprint

    def pprint_actions(self):

        for pool in self.actions.keys():
            self.dprint(pool)
            for action in self.actions[pool]:
                self.dprint("\t%s"%action)

    def parse_actions_dir(self,directory=None):

        if directory==None:
            directory=LlxPoolManager.ACTIONS_DIR

        for pool in glob.glob(directory+"/*"):
            short_pool=pool.split("/")[-1]
            self.actions[short_pool]={}
            self.actions[short_pool]=sorted(glob.glob(pool+"/*"))

        #self.pprint_actions()

    #def parse_actions_dir

    def print(self,data,color=None):

        if not LlxPoolManager.USE_COLORS or color==None:
            print(data)
        else:
            print(color + data)

    #def print

    def print_welcome(self):

        self.print("")
        self.print("Lliurex Pool Manager",BLUE)
        self.print("====================",BLUE)
        self.print("")
        self.select_pool_step()

    #def print_welcome

    def select_pool_step(self):

        ok=False

        while not ok:
            self.print("> Select pool to manage:\n",CYAN)
            options={}
            count=1
            for pool in self.actions.keys():
                print("\t%s) %s"%(count,pool))
                options[str(count)]=pool
                count+=1

            print("")
            print("\tq) %s"%("Exit"))
            options["q"]=LlxPoolManager.EXIT

            print("")
            option=input("> ")
            print("")
            if option not in options:
                self.print("[!] Unknown option '%s'"%option,YELLOW)
            else:
                ok=True

        if options[option]==LlxPoolManager.EXIT:
            sys.exit(0)
        else:
            self.current_pool=options[option]
            self.select_action_step()

    #def select_pool_step

    def select_action_step(self):

        ok=False

        while not ok:
            self.print("> Select action to execute:\n",CYAN)
            count=1
            options={}
            for action in self.actions[self.current_pool]:
                last_executed=""
                if action in self.executed_actions:
                    last_executed="%s(Last executed at %s)"%(GREEN if LlxPoolManager.USE_COLORS else "",self.executed_actions[action])
                print("\t%s) %s %s"%(count,action.split("/")[-1],last_executed))
                options[str(count)]=action
                count+=1

            print("")
            print("\tb) Go back to pool selection")
            options["b"]=LlxPoolManager.BACK_TO_POOL_SELECTION
            count+=1
            print("\tq) %s"%("Exit"))
            options["q"]=LlxPoolManager.EXIT
            print("")

            option=input("> ")
            print("")
            if option not in options:
                self.print("[!] Unknown option '%s'"%option,YELLOW)
            else:
                ok=True

        if options[option]==LlxPoolManager.EXIT:
            sys.exit(0)
        elif options[option]==LlxPoolManager.BACK_TO_POOL_SELECTION:
            self.select_pool_step()
        else:
            self.current_action=options[option]
            self.execute_action()

    def execute_action(self):

        count=0
        next_execution=False
        offer_next=False

        for action in self.actions[self.current_pool]:
            if action==self.current_action:
                self.print("> Executing %s ..."%action.split("/")[-1])
                os.system('%s'%action)
                date=datetime.datetime.now()
                formated_time="%s:%s:%s"%(date.hour,date.minute,date.second)
                self.executed_actions[action]=formated_time
                print("> Finished executing %s"%action.split("/")[-1])
                print("")

                if offer_next:
                    if len(self.actions[self.current_pool])>count+1:
                        ok=False
                        while not ok:
                            print("> Do you want to execute '%s' ? [y|n]"%self.actions[self.current_pool][count+1].split("/")[-1])
                            option=input("> ")
                            if option not in ["y","n"]:
                                print("[!] Unknown option")
                            else:
                                ok=True
                        if option=="y":
                            self.current_action=self.actions[self.current_pool][count+1]
                            next_execution=True

                break

            else:
                count+=1

        if next_execution:
            self.execute_action()
        else:
            self.select_action_step()

    #def execute_action

#class LlxPoolManager

if __name__=="__main__":

    lpm=LlxPoolManager(sys.argv[1:])



