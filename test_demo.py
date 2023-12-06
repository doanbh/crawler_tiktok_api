from tiktokapipy.api import TikTokAPI

def do_something():
    with TikTokAPI() as api:
        user = api.user('vantoan___')
        print(user)
        for video in user.videos:
            num_comments = video.stats.comment_count
            num_likes = video.stats.digg_count
            num_views = video.stats.play_count
            num_shares = video.stats.share_count

if __name__ == '__main__':
    do_something()

