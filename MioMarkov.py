# coding=utf-8
from misc.brain import Brain
from core.baseclass import PluginBase
from random import random, choice
from pkg_resources import resource_filename


class MioMarkov(PluginBase):

    def __init__(self, database, handler):
        super().__init__(database, handler, 'MioMarkov')
        self.brain = Brain(resource_filename('misc', 'dota2_cobe.sql'))

    def execute_titlepost(self, title_only):
        pass

    def on_new_message(self, message):
        pass

    def update_procedure(self, thing, created, lifetime, last_updated, interval):
        pass

    def execute_link(self, link_submission):
        pass

    def execute_submission(self, submission):
        if submission.subreddit.display_name.lower() == 'dota2' and random() <= 0.001:
            reply = self.produce_dank_maymays(submission.selftext)
            if reply:
                self.add_comment(submission.name, reply)
                return True

    def execute_comment(self, comment):
        if comment.subreddit.display_name.lower() == 'dota2' or random() <= 0.001:
            reply = self.produce_dank_maymays(comment.body)
            if reply:
                self.add_comment(comment.name, reply)
                return True

    def produce_dank_maymays(self, message):
        msg = ''
        i = 0
        while(not (10 < len(msg) < 210)):
            if i > 4:
                msg = ''
                break
            msg = self.brain.reply(message)
            i += 1
        return msg


def init(database, handler):
    return MioMarkov(database, handler)

if __name__ == '__main__':
    from core.logprovider import setup_logging
    from core.handlers import RoverHandler
    from core.database import Database
    logger = setup_logging('DEBUG')
    mm = MioMarkov(Database(), RoverHandler())
    mm.test_single_comment('cvfmf9e')
