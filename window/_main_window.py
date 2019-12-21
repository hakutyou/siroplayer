import pyglet
from ._main_player import MainPlayer
from ._configure_loader import ConfigureLoader


class MainWindow(pyglet.window.Window):
    padding = 10

    def __init__(self, caption):
        self.cf = ConfigureLoader()
        self.index = 0
        self.max_index = 0
        super(MainWindow, self).__init__(caption=caption, resizable=True,
                                         width=self.cf.window_width, height=self.cf.window_height)
        self.player = MainPlayer()
        self.set_visible(True)

    def on_draw(self):
        if self.player.source and self.player.source.video_format:
            # 视频
            self.clear()
            # self.player.get_texture().blit(0, 0)
            self.player.get_texture().blit(
                0, 0, width=self.player.width, height=self.player.height)

    def close(self):
        self.cf.write_data()
        if self.player.source:
            self.player.source.delete()
        super(MainWindow, self).close()

    def add_path(self, path: str):
        self.max_index = self.player.analyse_path(path)

    def list_media(self):
        return self.player.play_list

    def load_media(self, debug_play=False):
        self.player.load_source(index=self.index, debug_play=debug_play)
        # 播放器
        # self.player.set_locate(0, 50)
        self.player.get_and_set_video_size()
        if self.player.width:
            self.set_size(width=int(self.player.width), height=int(self.player.height))
            self.player.push_handlers(self)

        return self.player
