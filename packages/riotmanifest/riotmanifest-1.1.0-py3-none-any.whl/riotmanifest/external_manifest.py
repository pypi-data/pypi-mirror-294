# -*- coding: utf-8 -*-
# @Author  : Virace
# @Email   : Virace@aliyun.com
# @Site    : x-item.com
# @Software: Pycharm
# @Create  : 2024/9/3 13:39
# @Update  : 2024/9/5 17:56
# @Detail  : 

import os
import platform
import subprocess
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, List, Optional, Union

import requests
from loguru import logger

from riotmanifest.game import RiotGameData


@contextmanager
def execute_command(
    args: Union[str, List[str]], executable: Optional[str] = None, cwd: Optional[str] = None
) -> Iterator[subprocess.Popen]:
    """
    执行第三方命令并提供一个上下文管理器来处理其输出。

    :param args: 要执行的命令，可以是字符串或字符串列表。
    :param executable: 可执行文件的路径。如果为 None，则使用 args 中的第一个元素。
    :param cwd: 执行命令的工作目录。如果为 None，则使用当前目录。
    :yield: 提供一个子进程对象以供上下文管理。
    """
    if isinstance(args, str):
        # 如果 args 是字符串，则按空格分割为列表
        args = args.split()

    process = None  # 初始化 process 变量

    try:
        logger.debug(f"准备执行命令: {' '.join(args)}")

        # 启动子进程，并将 stderr 重定向到 stdout
        process = subprocess.Popen(
            args=args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            executable=executable,
            cwd=cwd,
            text=True,
            bufsize=1,  # 行缓冲
        )

        yield process

    except subprocess.CalledProcessError as e:
        logger.error(f"命令执行失败: {e}")
    except Exception as e:
        logger.error(f"执行命令时发生未知错误: {e}")
    finally:
        if process and process.stdout:
            process.stdout.close()
        if process:
            process.wait()


class GeneralError(Exception):
    pass


class ManifestDL:
    def __init__(self, md_path: Optional[str] = None, use_cn_mirror: bool = False):
        """
        初始化 ManifestDL 实例。

        :param md_path: ManifestDownloader 的本地路径。如果未提供，将自动下载。
        :param use_cn_mirror: 是否使用中国镜像下载。
        """
        self.base_url = "https://github.com/Morilli/ManifestDownloader/releases/latest/download/"
        self.cache_dir = Path("/tmp") if platform.system() != "Windows" else Path(os.getenv("TEMP", "/tmp"))
        if use_cn_mirror:
            self.base_url = f"https://mirror.ghproxy.com/{self.base_url}"

        self.md_path = md_path or self._download_md()
        if not self.md_path:
            raise GeneralError("ManifestDownloader 未提供或下载失败")

    def _download_md(self) -> Optional[str]:
        """
        下载 ManifestDownloader 程序。

        :return: 下载文件的完整路径，如果下载失败则返回 None。
        """
        filename = "ManifestDownloader.exe" if platform.system() == "Windows" else "ManifestDownloader"
        url = self.base_url + filename

        cache_path = self.cache_dir / "manifest_dl"
        cache_path.mkdir(parents=True, exist_ok=True)

        file_path = cache_path / filename

        try:
            logger.debug(f"下载 {filename} 到 {file_path}")
            response = requests.get(url, stream=True)
            response.raise_for_status()

            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            logger.debug(f"下载完成：{file_path}")

            # 设置可执行权限（仅限非Windows系统）
            if platform.system() != "Windows":
                os.chmod(file_path, 0o755)
                logger.debug(f"设置 {file_path} 为可执行")

            return str(file_path)

        except requests.RequestException as e:
            logger.error(f"下载失败：{e}")
            return None

    def run(
        self, manifest: str, output: str, threads: int = 8, pattern: str = "", exclude: str = "", retries: int = 3
    ) -> bool:
        """
        运行 ManifestDownloader 命令，支持重试。

        :param manifest: 清单文件路径。
        :param output: 输出目录。
        :param threads: 使用的线程数。
        :param pattern: 匹配的正则表达式模式。
        :param exclude: 排除的正则表达式模式。
        :param retries: 重试次数。
        :return: 如果执行成功返回 True，否则返回 False。
        """

        command = ["ManifestDownloader", manifest, "-o", output, "-t", str(threads)]

        if pattern:
            command.append("-f")
            command.append(pattern)

        if exclude:
            command.append("-u")
            command.append(exclude)

        for attempt in range(retries):
            try:
                with execute_command(
                    args=command,
                    executable=self.md_path,
                    cwd=str(self.cache_dir),
                ) as process:
                    for line in process.stdout:
                        line = line.strip()

                        # 报错，但是排除程序默认重试机制
                        if (
                            any(word in line.lower() for word in ["error", "aborted", "failed", "closed", "not"])
                            and "Trying again" not in line
                        ):
                            logger.error(f"ManifestDownloader执行失败：{line}")
                            raise GeneralError(f"ManifestDownloader执行失败: {line}")
                logger.debug("ManifestDownloader执行完毕")
                return True
            except Exception as e:
                logger.warning(f"尝试 {attempt + 1}/{retries} 失败: {e}")
                if attempt + 1 == retries:
                    logger.error("所有重试均失败")
                    return False
        return False


class ResourceDL:
    def __init__(self, out_dir: str, md_path: Optional[str] = None, max_retries: int = 5):
        """
        初始化 ResourceDL 类。

        可以通过修改 game_d，lcu_d来控制是否下载某一项，防止误操作默认均不下载

        :param out_dir: 输出目录
        :param md_path: ManifestDownloader 的路径
        :param max_retries: 最大重试次数
        """
        self.out_dir = out_dir
        self.max_retries = max_retries
        self.mdl = ManifestDL(md_path)
        self.game = RiotGameData()
        self.game.load_game_data()
        self.game.load_lcu_data()

        self.d_game = False
        self.d_lcu = False

    def download_resources(self, game_filter: str = "", lcu_filter: str = ""):
        """
        下载游戏和 LCU 资源。

        :param game_filter:  game正则
        :param lcu_filter: lcu正则
        """
        game_data = self.game.latest_game()
        lcu_data = self.game.lcu.EUW

        logger.debug(f"LCU: {game_data.version}")
        logger.debug(f"GAME: {lcu_data.version}")

        try:
            if self.d_game:
                self.mdl.run(
                    game_data.url,
                    os.path.join(self.out_dir, "Game"),
                    pattern=f"{game_filter}",
                    retries=self.max_retries,
                )
        except Exception as e:
            logger.error(f"下载游戏资源失败: {e}")

        try:
            if self.d_lcu:
                self.mdl.run(
                    lcu_data.patch_url,
                    os.path.join(self.out_dir, "LeagueClient"),
                    pattern=lcu_filter,
                    retries=self.max_retries,
                )
        except Exception as e:
            logger.error(f"下载 LCU 资源失败: {e}")
