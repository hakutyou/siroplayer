import pyglet
import pathlib
import pyglet_ffmpeg2
import ffmpeg


class MainPlayer(pyglet.media.Player):
    width = height = 0
    source = None

    def __init__(self):
        super(MainPlayer, self).__init__()
        pyglet_ffmpeg2.load_ffmpeg()
        self._play_list = []

    @property
    def play_list(self):
        return self._play_list

    def load_source(self, index=0, debug_play=False):
        do_play = self.play_list[index]
        if debug_play:
            print(do_play)
        self.source = pyglet.media.load(str(do_play))
        return

    def analyse_path(self, path_index: str):
        """
        根据路径（目录或文件）返回所有可播放的文件
        """

        def _iter_analyse_path(_path_index: pathlib.Path, searched_path=()):
            result = []
            if not _path_index.exists():
                pass
            elif _path_index.is_file():
                result.append(_path_index.resolve())
            elif _path_index.is_dir():
                for i in _path_index.iterdir():
                    # 递归防止出现闭环
                    if i not in searched_path:
                        result += _iter_analyse_path(i, (searched_path + (_path_index,)))
            return set(filter(self._is_media_file, result))

        _path = pathlib.Path(path_index)
        self._play_list += _iter_analyse_path(_path)
        return len(self._play_list)

    @staticmethod
    def _is_media_file(file) -> bool:
        """
        音频视频文件返回 True
        无法识别文件返回 False
        """
        try:
            ffmpeg.probe(str(file))
            return True
        except ffmpeg.Error:
            return False

    def get_and_set_video_size(self):
        if not self.source:  # 未加载文件
            return
        if self.source.video_format is None:  # 音频
            return

        self.width = self.source.video_format.width
        self.height = self.source.video_format.height
        if self.source.video_format.sample_aspect > 1:
            self.width *= self.source.video_format.sample_aspect
        else:
            self.height /= self.source.video_format.sample_aspect
