# coding=utf-8
from core.baseclass import PluginBase
import re


class LeafeatorBot(PluginBase):
    def __init__(self, database, handler):
        super().__init__(database, handler, 'LeafeatorBot')
        self.APPROVE = ['dota2circlejerk', 'dota2', 'dotamasterrace', 'dota2moddingtesting']
        self.RESPONSE = self.config.get('LeafeatorBot', 'response')
        self.REGEX = re.compile(
            r'(ancient(?!.*(apparition)).*necro(?!s)|necro.*ancient(?!.*(apparition))|leafeator-bot)',
            re.IGNORECASE)

    def execute_comment(self, comment):
        return self.general_action(comment.body, comment, is_comment=True)

    def execute_titlepost(self, title_only):
        pass

    def execute_link(self, link_submission):
        pass

    def execute_submission(self, submission):
        return self.general_action(submission.selftext, submission)

    def update_procedure(self, thing_id, created, lifetime, last_updated, interval):
        pass

    def general_action(self, body, thing, is_comment=False):
        if thing.author and 'leafeator' in thing.author.name.lower():
            self.logger.info('Leafeator posted - ignoring')
            return False

        if thing.subreddit.display_name.lower() not in self.APPROVE:
            return False

        result = self.REGEX.findall(body)
        if result:
            self.logger.info('I should post soon if not already answered.')
            if not is_comment:
                thread_id = thing.name
            else:
                thread_id = thing.submission.name
            if self.database.retrieve_thing(thread_id, self.BOT_NAME):
                self.logger.info('Skipped - already commented in thread.')
                return False

            self.oa_refresh()
            self.session._add_comment(thing.name, self.RESPONSE)
            self.database.insert_into_storage(thread_id, self.BOT_NAME)
            return True
        return False

    def on_new_message(self, message):
        pass


def init(database, handler):
    """Init Call from module importer to return only the object itself, rather than the module."""
    return LeafeatorBot(database, handler)


if __name__ == '__main__':
    from praw import Reddit
    from core.DatabaseProvider import DatabaseProvider
    from core import LogProvider
    logger = LogProvider.setup_logging(log_level="DEBUG")
    db = DatabaseProvider()
    lb = LeafeatorBot(db)
    lb.test_single_comment('cuomou4')
    # lb.execute_submission(subm)
