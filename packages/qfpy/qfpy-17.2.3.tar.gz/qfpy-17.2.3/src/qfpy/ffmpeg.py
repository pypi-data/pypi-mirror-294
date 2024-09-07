"""
def is_hevc(file: Path) -> bool

def is_not_hevc(file: Path) -> bool

class ffprobe
    def duration() -> str
    def codec_name() -> str
    def size() -> str

class ffmpeg
    ffmpeg_path
    def i(输入文件: str | Path)
    def c_v(视频编码: Literal["copy", "hevc_nvenc"])
    def c_a(音频编码: Literal["copy"])
    def c_s(字幕编码: Literal["mov_text"])
    def hwaccel(硬件加速: Literal["auto", "cuda"])
    def 输出(输出文件: str | Path)
    def 运行(capture_output: bool = True) -> None
"""

import json
import subprocess as sp
from pathlib import Path
from typing import Literal, Self

from qfpy.log import logger


class ffprobe:
    """
    方法

    duration：获取视频时长

    codec：获取视频编码

    size：获取视频大小
    """

    def __init__(self, file: str | Path):
        self.metadata = self.__ffprobe(file)
        if not self.metadata:
            raise Exception("metadata 解析错误：" + str(file))

    def __repr__(self):
        return str(self.metadata)

    def __ffprobe(self, file: str | Path) -> dict:
        """
        私有方法：获取视频的元数据信息。

        参数:
        - file: 字符串，指定要分析的视频文件的路径。

        返回值:
        - 返回一个字典，包含视频的元数据信息，如格式、流信息等。
        """
        # 构造ffprobe命令行字符串，并执行命令获取视频元数据
        cmd = f'd:/ffmpeg/bin/ffprobe -print_format json -show_format -show_streams -v quiet "{file}"'
        process = sp.run(cmd, shell=True, stdout=sp.PIPE)
        output = process.stdout.decode()
        return json.loads(output)  # 将命令输出的JSON字符串解析为字典并返回

    def duration(self) -> str:
        return self.metadata["format"]["duration"]

    def codec_name(self) -> str:
        return self.metadata["streams"][0]["codec_name"]

    def size(self) -> str:
        return self.metadata["format"]["size"]


def is_hevc(file: Path) -> bool:
    """
    编码为 hevc 返回 True
    """
    return True if ffprobe(file).codec_name() == "hevc" else False


def is_not_hevc(file: Path) -> bool:
    """
    编码不是 hevc 返回 True
    """
    return not is_hevc(file)


class ffmpeg:
    ffmpeg_path = "d:/ffmpeg/bin/ffmpeg.exe"

    def __init__(self):
        self.args = [self.ffmpeg_path, "-hide_banner"]

    def i(self, 输入文件: str | Path) -> Self:
        if isinstance(输入文件, Path):
            输入文件 = 输入文件.as_posix()
        self.args.extend(["-i", 输入文件])
        return self

    def c_v(self, 视频编码: Literal["copy", "hevc_nvenc"]):
        self.args.extend(["-c:v", 视频编码])
        return self

    def c_a(self, 音频编码: Literal["copy"]):
        self.args.extend(["-c:a", 音频编码])
        return self

    def c_s(self, 字幕编码: Literal["mov_text"]):
        self.args.extend(["-c:s", 字幕编码])
        return self

    def hwaccel(self, 硬件加速: Literal["auto", "cuda"]):
        self.args.extend(["-hwaccel", 硬件加速])
        return self

    def c(self, 编码: Literal["copy"]):
        self.args.extend(["-c", 编码])
        return self
    
    def ss(self, 开始时间: str):
        self.args.extend(["-ss", 开始时间])
        return self
    
    def to(self, 结束时间: str):
        self.args.extend(["-to", 结束时间])
        return self
    
    def y(self):
        """覆盖已存在文件"""
        self.args.append("-y")
        return self

    def 输出(self, 输出文件: str | Path):
        if isinstance(输出文件, Path):
            输出文件 = 输出文件.as_posix()
        self.args.append(输出文件)
        return self

    def 运行(self, capture_output: bool = True) -> None:
        logger.info(f"执行命令：{' '.join(self.args)}")
        sp.run(self.args, capture_output=capture_output)
    
    def f(self, 过滤器: Literal["concat"]):
        self.args.extend(["-f", 过滤器])
        return self
    
    def safe(self, 安全模式: Literal["0"]):
        self.args.extend(["-safe", 安全模式])
        return self


if __name__ == "__main__":
    print(ffprobe())
