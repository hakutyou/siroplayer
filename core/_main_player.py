import pyglet
import pyglet_ffmpeg2

from ._playlist import PlayList


class MainPlayer(pyglet.media.Player):
    x = y = width = height = 0
    source = None
    have_next = False

    def __init__(self):
        super(MainPlayer, self).__init__()
        pyglet_ffmpeg2.load_ffmpeg()
        self._play_list = PlayList()

    @property
    def play_list(self):
        """
        返回整个列表
        """
        return self._play_list.file_list

    def append_path(self, path: str):
        """
        刷新或添加一个路径
        """
        self._play_list.append_path(path)
        # TODO: 如果在播放中需要刷新位置

    def remove_path(self, path: str):
        """
        删除一个路径
        """
        self._play_list.append_path(path, operation='remove')
        # TODO: 如果在播放中需要刷新位置

    def load_source(self, index=0, debug_play=False):
        do_play = self.play_list[index]
        if debug_play:
            print(do_play)
        self.source = pyglet.media.load(str(do_play))
        return

    def get_video_size(self, window_width, window_height):
        if not self.source:  # 未加载文件
            return
        if self.source.video_format is None:  # 音频
            return

        # 真实尺寸
        self.width = self.source.video_format.width
        self.height = self.source.video_format.height
        if self.source.video_format.sample_aspect > 1:
            self.width *= self.source.video_format.sample_aspect
        else:
            self.height /= self.source.video_format.sample_aspect
        # 缩放
        width_scale = window_width / self.width  # (800 / 1024) * 1024
        height_scale = window_height / self.height  # 768 / 600
        scale = min(width_scale, height_scale)
        self.width = int(self.width * scale)
        self.height = int(self.height * scale)
        self.x = (window_width - self.width) // 2
        self.y = (window_height - self.height) // 2
