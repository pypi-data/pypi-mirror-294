##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.19                                                            #
# Generated on 2024-09-04T23:07:02.519088                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.metaflow_current

current: metaflow.metaflow_current.Current

ASYNC_TIMEOUT: int

class CardProcessManager(object, metaclass=type):
    ...

class CardCreator(object, metaclass=type):
    def __init__(self, top_level_options):
        ...
    def create(self, card_uuid = None, user_set_card_id = None, runtime_card = False, decorator_attributes = None, card_options = None, logger = None, mode = "render", final = False, sync = False):
        ...
    ...

