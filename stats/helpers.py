import itertools


def get_sliced_list(generator, number=50):
    while True:
        id_list = [video.id for video in itertools.islice(generator, number)]

        if not id_list:
            break

        yield id_list


def get_video_id(video_detail):
    return video_detail['id']['videoId'] if type(video_detail['id']) == dict else video_detail['id']


