import pyglet

from window import MainWindow


def play_method(order_method='nr'):
    def _closure_play_method():
        # 先播放
        s_media = s_window.load_media(debug_play=True)
        s_player = s_media.play()
        # 考虑下一首
        have_next = False
        if 'n' in order_method:  # 顺序播放
            have_next = True
            s_window.index += 1
        elif 's' in order_method:  # 单曲循环
            have_next = True
        elif s_window.index >= s_window.max_index:
            if 'r' in order_method:  # 循环播放
                s_window.index = 0
            else:  # 放完了停止
                have_next = False
        if have_next:
            s_player.on_player_eos = play_method(order_method)

    # 返回一个可调用的对象
    return _closure_play_method


if __name__ == '__main__':
    s_window = MainWindow('Player')
    s_window.add_path(r'C:\Users\hakutyou\Videos')

    _len = len(s_window.list_media())
    do_play = play_method(order_method='')
    do_play()
    pyglet.app.run()
