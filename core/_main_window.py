import time

import pyglet

from ._configure_loader import ConfigureLoader
from ._main_player import MainPlayer


class Text:
    font_name = 'Sarasa Mono SC'
    font_size = 26
    x = y = None
    expired = 0
    text = None

    def __init__(self, x, y):
        self.set_position(x, y)

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_tips(self, content, timeout=5, anchor_x='center', anchor_y='center'):
        if self.x is None or self.y is None:
            return
        self.expired = time.time() + timeout
        self.text = pyglet.text.Label(content, font_name=self.font_name, font_size=self.font_size,
                                      x=self.x, y=self.y, anchor_x=anchor_x, anchor_y=anchor_y)


class MainWindow(pyglet.window.Window):
    trim = False
    tips = {}

    def __init__(self, caption):
        self.cf = ConfigureLoader()
        self.index = 0
        self.max_index = 0
        super(MainWindow, self).__init__(caption=caption, resizable=True,
                                         width=self.cf.window_width, height=self.cf.window_height)
        self.set_minimum_size(width=self.cf.window_minimum_width, height=self.cf.window_minimum_height)
        self.player = MainPlayer()
        self.set_visible(True)

        # 居中字幕
        self.tips['center'] = Text(x=self.width / 2, y=self.height / 2)

    def play(self):
        self.player.play()
        # TODO: media_info 或许有用
        media_info = self.player.media_info
        do_play = self.player.do_play
        self.tips['center'].set_tips(do_play.name, timeout=5)

    def on_draw(self):
        self.clear()
        # 视频
        if self.player.source and self.player.source.video_format:
            # self.player.get_texture().blit(0, 0)
            self.player.get_texture().blit(
                self.player.x, self.player.y, width=self.player.width, height=self.player.height)
        # 文字
        for tip_label in self.tips:
            tip = self.tips[tip_label]
            left_time = tip.expired - time.time()
            # 渐渐消失
            if left_time > 0:
                tip.text.color = (255, 255, 255, int(255 * min(1, left_time)))
                tip.text.draw()

    def on_resize(self, width, height):
        super(MainWindow, self).on_resize(width, height)
        self.cf.window_width = self.width
        self.cf.window_height = self.height
        self._scale_player()

    def on_key_press(self, symbol, modifiers):
        # 播放/暂停
        if pyglet.window.key.SPACE == symbol:
            if self.player.playing:
                self.player.pause()
            else:
                self.player.play()
            return
        # 退出
        if pyglet.window.key.Q == symbol:
            self.close()
        # 微调
        if symbol in [pyglet.window.key.LCTRL, pyglet.window.key.RCTRL]:
            self.trim = True
            return
        # 查看信息
        if pyglet.window.key.T == symbol:
            frame_rate = self.player.source.video_format.frame_rate
            progress = self.player.time / self.player.source.duration
            # 打印当前播放时间
            print(f'Time: {self.player.time:.2f}s/{self.player.source.duration:.2f}s ({progress:.2f}%)')
            # 打印当前播放帧
            print(f'Frame: {self.player.time * frame_rate:.1f}/{self.player.source.duration * frame_rate:.1f}')
            return
        # 音量
        if pyglet.window.key.UP == symbol:
            self.player.volume += 0.02 if self.trim else 0.2
            return
        if pyglet.window.key.DOWN == symbol:
            self.player.volume -= 0.02 if self.trim else 0.2
            if self.player.volume < 0:
                self.player.volume = 0
            return
        # 快进
        if pyglet.window.key.RIGHT == symbol:
            self.player.seek(self.player.time + 0.1 if self.trim else 1)
            return
        if pyglet.window.key.LEFT == symbol:
            self.player.seek(self.player.time - 0.1 if self.trim else 1)
            return

    def on_key_release(self, symbol, modifiers):
        # 微调
        if symbol in [pyglet.window.key.LCTRL, pyglet.window.key.RCTRL]:
            self.trim = False
            return

    def close(self):
        self.cf.write_data()
        if self.player.source:
            self.player.source.delete()
        self.player.delete()
        super(MainWindow, self).close()

    def add_path(self, path: str):
        self.max_index = self.player.append_path(path)

    def list_media(self):
        return self.player.play_list

    def load_media(self, debug_play=False):
        self.player.load_source(index=self.index, debug_play=debug_play)
        self._scale_player()
        return self.player

    def _scale_player(self):
        self.player.get_video_size(self.cf.window_width, self.cf.window_height)
