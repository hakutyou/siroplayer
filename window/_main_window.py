import pyglet

from ._configure_loader import ConfigureLoader
from ._main_player import MainPlayer


class MainWindow(pyglet.window.Window):
    def __init__(self, caption):
        self.cf = ConfigureLoader()
        self.index = 0
        self.max_index = 0
        super(MainWindow, self).__init__(caption=caption, resizable=True,
                                         width=self.cf.window_width, height=self.cf.window_height)
        self.set_minimum_size(width=self.cf.window_minimum_width, height=self.cf.window_minimum_height)
        self.player = MainPlayer()
        self.set_visible(True)

    def on_draw(self):
        if self.player.source and self.player.source.video_format:
            # 视频
            self.clear()
            # self.player.get_texture().blit(0, 0)
            self.player.get_texture().blit(
                self.player.x, self.player.y, width=self.player.width, height=self.player.height)

    def on_resize(self, width, height):
        super(MainWindow, self).on_resize(width, height)
        self.cf.window_width = self.width
        self.cf.window_height = self.height
        self._scale_player()

    def on_key_press(self, symbol, modifiers):
        a = self.player.source
        if pyglet.window.key.SPACE == symbol:
            if self.player.playing:
                self.player.pause()
            else:
                self.player.play()
            return
        if pyglet.window.key.T == symbol:
            print(f'{self.player.time:.2f}s/{self.player.source.duration:.2f}s')  # 打印当前播放时间
            return
        if pyglet.window.key.F == symbol:
            print(f'{self.player.source}')
            return
        if pyglet.window.key.RIGHT == symbol:
            print(self.player.seek(self.player.time + 5))
            return
        if pyglet.window.key.Q == symbol:
            self.close()

    def close(self):
        self.cf.write_data()
        if self.player.source:
            self.player.source.delete()
        self.player.delete()
        super(MainWindow, self).close()

    def add_path(self, path: str):
        self.max_index = self.player.analyse_path(path)

    def list_media(self):
        return self.player.play_list

    def load_media(self, debug_play=False):
        self.player.load_source(index=self.index, debug_play=debug_play)
        self._scale_player()
        return self.player

    def _scale_player(self):
        self.player.get_video_size(self.cf.window_width, self.cf.window_height)
