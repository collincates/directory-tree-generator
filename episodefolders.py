#!/usr/bin/env python
import os

def epfolders():

    while True:
        try:
            season = int(input("Which season is this? "))
        except ValueError:
            print("Try a number instead.")
            continue
        else:
            break

    while True:
        try:
            ep_qty = int(input("How many episodes are in this season? "))
        except ValueError:
            print("Try a number instead.")
            continue
        else:
            break

    for ep in range(1, int(ep_qty) + 1):
        if not os.path.exists(os.path.join(os.path.curdir, "Episode " + f"{season}{ep:02d}")):
            os.mkdir(os.path.join(os.path.curdir, "Episode " + f"{season}{ep:02d}"))
            #print(os.path.join(os.path.curdir, "Episode " + f"{season}0{ep}"))
        else:
            print("Episode " + f"{season}{ep:02d} already exist within this directory.")


epfolders()
