import api_handlers

import follow.api
import hashtag.api

"""
Register function on events created and published by clips api.
"""
api_handlers.register_on_clip_created(follow.api.on_clip_created)
api_handlers.register_on_clip_created(hashtag.api.update_hashtag)
api_handlers.register_on_clip_deleted(follow.api.on_clip_delete)