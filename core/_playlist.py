import pathlib

import ffmpeg


class PlayList:
    searched_path = []
    # 用 list 而不是 set()
    # set() 不保存数据顺序
    file_list = []

    def __init__(self):
        pass

    def append_path(self, path: str, operation='append'):
        """
        NOTE: 注意操作后刷新下一个播放
        根据路径（目录或文件）添加所有可播放的文件
        """

        def _iter_path(path_index: pathlib.Path) -> set:
            result = []
            if not path_index.exists():
                pass
            elif path_index.is_file():
                need_append = path_index.resolve()
                result.append(need_append)
            elif path_index.is_dir():
                for i in path_index.iterdir():
                    # 递归防止出现闭环
                    if i in self.searched_path:
                        continue
                    self.searched_path.append(path_index)
                    result += _iter_path(i)
            return set(filter(self._is_media_file, result))

        _path = pathlib.Path(path)
        if 'append' == operation:
            # 并集
            # self.file_list = set(self.file_list) | _iter_path(_path)
            self.file_list += [i for i in _iter_path(_path)
                               if i not in self.file_list]
        if 'remove' == operation:
            # 差集
            # self.file_list = set(self.file_list) - _iter_path(_path)
            self.file_list = [i for i in self.file_list
                              if i not in _iter_path(_path)]
        return len(self.file_list)

    def move_list(self, index, move_to_index):
        """
        NOTE: 注意操作后刷新下一个播放
        将 index 移动到 move_to_index
        例如原 [0,1,2,3,4,5] 将 1 移动到 3
        [0,2,1,3,4,5]
        """
        self.file_list.insert(move_to_index, self.file_list[index])
        if index > move_to_index:
            self.file_list.pop(index + 1)
        else:
            self.file_list.pop(index)

    def switch_list(self, index, switch_to_index):
        """
        NOTE: 注意操作后刷新下一个播放
        交换两个元素位置
        """
        self.file_list[index], self.file_list[switch_to_index] = \
            self.file_list[switch_to_index], self.file_list[index]

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
