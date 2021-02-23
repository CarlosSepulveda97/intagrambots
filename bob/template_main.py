# Official documentation
# https://instapy.org/settings/


# Additional imports random amount for interactions
import random
from instapy import InstaPy
from instapy import Settings
from instapy import set_workspace
from instapy.util import smart_run
import os

#####################
# InstaPy Settings  #
#####################

set_workspace(path="/InstaPy/Data/")
#base_dir = '/InstaPy/'
#Settings.log_location = os.path.join(base_dir, 'logs')
#Settings.database_location = os.path.join(base_dir, 'db', 'instapy.db')
#Settings.chromedriver_location = os.path.join(base_dir, 'assets', 'chromedriver')
#Settings.browser_location = '/path/to/chromedriver'

#####################
# Automate Settings #
#####################

# Login credentials
insta_username = '<YourLogin>'
insta_password = '<YourPassword>'

# Login data
#
# Proxy settings (add to session = InstaPy)
# proxy_address=proxy_host,
# proxy_port=proxy_port,
# proxy_username=proxy_username,
# proxy_password=proxy_password,

# bypass_suspicious_attempt=False,

session = InstaPy(username=insta_username,
                  password=insta_password,
                  headless_browser=True,
                  split_db=True,
                  nogui=False,
                  selenium_local_session=True,
                  disable_image_load=False,
                  want_check_browser=False)
                  
# Restrictions
dont_likes = ['sex', 'nude', 'naked', 'hunt', 'gun', 'war' 'shoot', 'slaughter', 'pussy', 'dick', 'squirt', 'gay', 'homo', 'nazi', 'promoter', 'jew', 'judaism', 'muslim', 'islam', 'bangladesh', 'hijab', 'niqab', 'farright', 'rightwing', 'death', 'racist', '#fit', '#fitfam', '#fittips', '#abs', '#kids', '#children', '#child', '#conservative']

ignore_users = ['user1', 'user2', 'user3']

# Prevent commenting on and unfollowing your good friends (the images will still be liked)
friends = ['friend1', 'friend2', 'friend3']

# Tags
like_tags=(['natgeo', 'world', 'pizza'])

# Prevent posts that contain
ignore_list = ['vegan', 'veggie']

# Skip all business accounts, except from list given
# https://www.google.com/search?q=instagram all business categories list
target_business_categories = ['category1', 'category2', 'category3']

# Comment Settings
comments = ['Cool photo!', 'Nice pic️', 'Good!']

# Following list
#following_list = session.grab_following(username="lazy.smurf", amount="full", live_match=True, store_locally=True)

# Target Settings
# set similar accounts and influencers from your niche to target
targets = ['natgeo', 'instagram']

#####################
# Session Settings  #
#####################

# If you want use session.end
# uncomment "while True:" and "session.end()"
# while True:

with smart_run(session):
    
    # Simulation
    session.set_simulation(enabled=True)
    # Target
    # LATIN, GREEK, CYRILLIC, ARABIC, HEBREW, CJK, HANGUL, HIRAGANA, KATAKANA , THAI
    session.set_mandatory_language(enabled=True, character_set=['LATIN', 'CYRILLIC'])
    # Set limits
    session.set_quota_supervisor(enabled=True, sleep_after=["likes", "comments", "follows", "server_calls"], sleepyhead=True, stochastic_flow=True, notify_me=True,
        peak_likes_hourly=random.randint(10, 30),
        peak_likes_daily=random.randint(100, 250),
        peak_comments_hourly=random.randint(1, 5),
        peak_comments_daily=random.randint(1, 10),
        peak_follows_hourly=random.randint(10, 30),
        peak_follows_daily=random.randint(10, 150),
        peak_unfollows_hourly=random.randint(10, 50),
        peak_unfollows_daily=random.randint(100, 300),
        peak_server_calls_hourly=random.randint(200, 2000),
        peak_server_calls_daily=random.randint(3000, 5000))
    # Min-Max likes or comments on the post
    session.set_delimit_liking(enabled=True, max_likes=100, min_likes=5)
    session.set_delimit_commenting(enabled=True, max_comments=10, min_comments=2)
    # Delays
    # Sleep in seconds after action
    session.set_action_delays(enabled=True,
        like=10,
        comment=200,
        story=5,
        follow=10,
        unfollow=60,
        randomize=True, random_range_from=70, random_range_to=160)
    # Relationship bounds
    session.set_relationship_bounds(enabled=True,
        potency_ratio=None,
        delimit_by_numbers=True,
        max_followers=1500,
        max_following=300,
        min_followers=50,
        min_following=25,
        min_posts=30)
    # Activity
    session.set_dont_include(friends)
    session.set_dont_like(dont_likes)
    session.set_ignore_if_contains(ignore_list)
    session.set_ignore_users(ignore_users)
    session.set_skip_users(skip_private=True,
        skip_no_profile_pic=True,
        skip_business=True,
        dont_skip_business_categories=[target_business_categories])
    session.set_user_interact(amount=random.randint(3, 5), randomize=True, percentage=80, media='Photo')
    session.set_do_like(enabled=True, percentage=90)
    # Stories
    session.set_do_story(enabled = True, percentage = 95, simulate = True)
#   session.story_by_users(following_list)
    session.story_by_tags(like_tags)
    # Comments
    session.set_do_comment(enabled=True, percentage=5)
    session.set_comments([comments], media='Photo')
    # Follow
    session.set_do_follow(enabled=True, percentage=40, times=1)
    # Likes
    # Like by Feeds
    session.like_by_feed(amount=random.randint(10, 25), randomize=True, unfollow=False, interact=True)
    # Like by Tags
    session.set_smart_hashtags(['nature', 'trip'], limit=3, sort='top', log_tags=True)
    session.like_by_tags(amount=random.randint(10, 25), use_smart_hashtags=True)

#####################
#     Targeting     #
#####################   

    # select users form a list of a predefined targets
    number = random.randint(3, 5)
    random_targets = targets
    if len(targets) <= number:
        random_targets = targets
    else:
        random_targets = random.sample(targets, number)

    # Interact with the chosen targets
    session.follow_user_followers(random_targets, amount=random.randint(30, 60), randomize=True, sleep_delay=600, interact=True)

#####################
#     Unfollow      #
#####################

    # After 2 days (All nonfollowers)
    session.unfollow_users(amount=random.randint(75,100), InstapyFollowed=(False, "nonfollowers"), style="FIFO", unfollow_after=48*60*60, sleep_delay=600)
    
    # After one week (All users followed by instapy)
    session.unfollow_users(amount=random.randint(75,100), InstapyFollowed=(True, "all"), style="FIFO", unfollow_after=168*60*60, sleep_delay=600)

    # Joining Engagement Pods
    #session.join_pods(topic='travel', engagement_mode='no_comments')
    
    
# If you want use session.end
# uncomment "while True:" and "session.end()"
# session.end()