#!/usr/bin/env python3
# -*- coding: utf-8 -*-

pool = dict()

class Player():
    def __init__(self, user_id, mines, death, wins, restricted_until, immunity_cards):
        self.user_id = user_id
        self.mines = mines
        self.death = death
        self.wins = wins
        self.restricted_until = restricted_until
        self.immunity_cards = immunity_cards
    @staticmethod
    def save():
        pass
    @staticmethod
    def db_close():
        pass

def get_player(user_id):
    player = pool.get(user_id, None)
    if player is None:
        player = Player(user_id=user_id, mines=0, death=0, wins=0,
                        restricted_until=0, immunity_cards=0)
        pool[user_id] = player
        return player
    else:
        return player
