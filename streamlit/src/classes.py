import streamlit as st
import inspect
import re

roles = ['adc', 'jgl', 'mid', 'sup', 'top']


class Base:

    @staticmethod
    def convert_kda(kda):
        return kda.split("/")

    @staticmethod
    def convert_golds(golds):
        """Convert the gold. Example: from 21.3k to 21300"""
        return int(golds[:-1].replace('.', '')) * 100

    @staticmethod
    def convert_timer(timer):
        """Convert the timer in a float"""
        if re.match(r"^(\d+(:[0-6]\d)?)$", timer):
            timer = timer.split(':')
            timer[1] = round(float(timer[1]) / 60, 2)
            return float(timer[0]) + timer[1]
        return float(timer)

    @staticmethod
    def is_valid(attr: str, val: str):
        regex_dict = {
            "kda": r"^\d+\/\d+\/\d+$",
            "timer": r"^(\d+(:[0-5]\d)?)$",
            "golds": r"^\d+.\dk$",
            "score": r"^\d+$",
            "towers": r"^\d+$",
            "creeps": r"^\d+$"
        }
        cond = re.match(regex_dict[attr], val)
        if cond:
            if attr == 'tower':
                if not 1 <= int(val) <= 11:
                    return False
        return cond

    @staticmethod
    def get_attr(instance):
        """Return a list of the attributes of an instance of a class"""
        attr = []
        # getmembers() returns all the members of an object
        for i in inspect.getmembers(instance):
            # to remove private and protected functions
            if not i[0].startswith('_'):
                # To remove other methods that doesn't start with a underscore
                if not inspect.ismethod(i[1]):
                    attr.append(i[0])
        return attr

    @staticmethod
    def get_values(instance):
        """Return a list of values of the attributes of an instance of a class"""
        return [getattr(instance, val_attr) for val_attr in Base.get_attr(instance)]

    def list_attributes_values(self, dict_all={}, parent=''):
        for attribute, value in self.__dict__.items():
            if str(value).startswith('<__main__.'):
                dict_all.update(self.list_attributes_values(value, dict_all, parent=parent + '_' + attribute))
            else:
                dict_all.update({(parent + '_' + attribute)[1:]: value})
        return dict_all

    def set_attr(self, attr: str, val):
        """Check if there is a given value, if it is valid then add it to the given attribute
        of the given instance of a class. If it is not valid, it displays an error on streamlit"""
        if val:
            if self.is_valid(attr, val):
                if attr == 'kda':
                    kda = self.convert_kda(val)
                    setattr(self, 'kills', kda[0])
                    setattr(self, 'deaths', kda[1])
                    setattr(self, 'assists', kda[2])
                else:
                    if attr == 'golds':
                        val = self.convert_golds(val)
                    elif attr == 'timer':
                        val = self.convert_timer(val)
                    setattr(self, attr, val)
            else:
                st.error("Mauvais format !")


class Champion(Base):

    def __init__(self):
        self.kills = None
        self.deaths = None
        self.assists = None
        self.creeps = None

    def is_complete_champ(self):
        """Check if all the values of the attributes of the champion are completed"""
        list_val = self.get_values(self)
        return all(list_val)


class Team(Base):

    def __init__(self):
        self.golds = None
        self.towers = None
        for role in roles:
            setattr(self, role, Champion())

    def is_valid_team(self):
        """Check if the number of assist of every member is less
        than the sum of kills of the remaining members of the team"""
        for role in roles:
            other_roles = [other_rol for other_rol in roles if other_rol != role]
            sum_kills = 0
            for other_role in other_roles:
                sum_kills += int(getattr(self, other_role).kills)
            if int(getattr(self, role).assists) > sum_kills:
                return False
        return True

    def is_complete_team(self):
        """Check if all the values of the attributes of the team are completed"""
        list_val = self.get_values(self)
        cond_champ = []
        for role in roles:
            cond_champ.append(getattr(self, role).is_complete_champ())
        return all(list_val) and all(cond_champ)


class Match(Base):

    def __init__(self):
        self.blue_team = Team()
        self.red_team = Team()
        self.timer = None

    def is_valid_match(self):
        """Check if the match values are valid
        (sum of deaths of a team greater than sum of kills of the opposite team)"""
        blue_team_kills, blue_team_deaths, red_team_kills, red_team_deaths = 0, 0, 0, 0
        for role in roles:
            blue_team_kills += int(getattr(self.blue_team, role).kills)
            blue_team_deaths += int(getattr(self.blue_team, role).deaths)
            red_team_kills += int(getattr(self.red_team, role).kills)
            red_team_deaths += int(getattr(self.red_team, role).deaths)
        return blue_team_kills <= red_team_deaths \
            and red_team_kills <= blue_team_deaths \
            and self.blue_team.is_valid_team() \
            and self.red_team.is_valid_team()

    def is_complete_match(self):
        """Check if all the values of the attributes of the match are completed"""
        list_val = self.get_values(self)
        return self.blue_team.is_complete_team() and self.red_team.is_complete_team() and all(list_val)

