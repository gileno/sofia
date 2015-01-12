from urllib import parse


def video_info(value):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    - http://vimeo.com/999999
    - http://www.vimeo.com/999999
    - http://player.vimeo.com/video/999999
    """
    result = parse.urlparse(value)
    if result.hostname == 'youtu.be':
        return result.path[1:], 'youtube'
    if result.hostname in ('www.youtube.com', 'youtube.com'):
        if result.path == '/watch':
            p = parse.parse_qs(result.query)
            return p['v'][0], 'youtube'
        if result.path[:7] == '/embed/':
            return result.path.split('/')[2], 'youtube'
        if result.path[:3] == '/v/':
            return result.path.split('/')[2], 'youtube'
    if result.hostname in ('vimeo.com', 'www.video.com'):
        return result.path.split('/')[1], 'vimeo'
    elif result.hostname == 'player.vimeo.com':
        return result.path.split('/')[2], 'vimeo'
    return None
