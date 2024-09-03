# -*- coding: utf-8 -*-
# @Author  : Virace
# @Email   : Virace@aliyun.com
# @Site    : x-item.com
# @Software: Pycharm
# @Create  : 2024/9/2 11:54
# @Update  : 2024/9/2 12:24
# @Detail  : 

from typing import Dict, List

from league_tools.formats import WAD, WadHeaderAnalyzer
from loguru import logger

from riotmanifest import PatcherChunk, PatcherFile, PatcherManifest


class WADExtractor:
    def __init__(self, manifest_file: str, bundle_url: str, output_dir: str):
        """
        初始化WADExtractor实例。

        :param manifest_file: 清单文件路径或URL。
        :param bundle_url: 资源文件的基础URL。
        :param output_dir: 文件保存的目录。
        """
        self.manifest_file = manifest_file
        self.bundle_url = bundle_url
        self.output_dir = output_dir
        self.manifest = PatcherManifest(
            file=manifest_file, path=output_dir, bundle_url=bundle_url
        )
        logger.debug(f"WADExtractor实例已初始化 - 清单文件: {manifest_file}, 资源URL: {bundle_url}, 输出目录: {output_dir}")

    def extract_files(self, wad_file_paths: Dict[str, List[str]]) -> Dict[str, Dict[str, bytes]]:
        """
        从多个WAD文件中提取多个文件。

        :param wad_file_paths: 字典结构，键是WAD文件名，值是需要提取的内部文件路径列表。
        :return: 提取的文件字节内容字典，外层字典的键是WAD文件路径，内层字典的键是WAD内部文件路径，值是文件字节内容。
        """
        extracted_files = {}
        logger.info("开始提取WAD文件中的内容。")

        for wad_filename, target_paths in wad_file_paths.items():
            logger.debug(f"处理WAD文件: {wad_filename}，目标路径: {target_paths}")
            wad_file = self._get_wad_file(wad_filename)
            wad = self._load_wad(wad_file)

            extracted_files[wad_filename] = {}
            for internal_path in target_paths:
                logger.debug(f"从WAD文件 {wad_filename} 中提取文件: {internal_path}")
                extracted_data = self._extract_internal_file(wad, wad_file, internal_path)
                extracted_files[wad_filename][internal_path] = extracted_data

        logger.info("完成WAD文件内容提取。")
        return extracted_files

    def _get_wad_file(self, wad_filename: str) -> PatcherFile:
        """
        根据WAD文件名查找并返回对应的PatcherFile对象。

        :param wad_filename: WAD文件名（支持正则匹配）。
        :return: PatcherFile对象。
        """
        logger.debug(f"正在查找WAD文件: {wad_filename}")
        wad_files = list(self.manifest.filter_files(pattern=wad_filename))
        if not wad_files:
            logger.error(f"未找到匹配的WAD文件: {wad_filename}")
            raise FileNotFoundError(f"未找到匹配的WAD文件: {wad_filename}")
        logger.debug(f"找到WAD文件: {wad_filename}")
        return wad_files[0]

    @classmethod
    def _load_wad(cls, wad_file: PatcherFile) -> WAD:
        """
        下载并加载WAD文件的头部数据。

        :param wad_file: 目标WAD文件。
        :return: 加载后的WAD对象。
        """
        logger.debug(f"加载WAD文件: {wad_file.name}")
        first_chunk = wad_file.chunks[0]
        header_data = wad_file.download_chunk(first_chunk)
        header_analyzer = WadHeaderAnalyzer(header_data)

        required_chunks = []
        accumulated_size = 0
        for chunk in wad_file.chunks:
            if accumulated_size >= header_analyzer.header_size:
                break
            accumulated_size += chunk.size
            required_chunks.append(chunk)

        wad_header_data = wad_file.download_chunks(required_chunks)
        logger.debug(f"WAD文件加载完成: {wad_file.name}")
        return WAD(wad_header_data)

    @classmethod
    def _extract_internal_file(
        cls, wad: WAD, wad_file: PatcherFile, internal_path: str
    ) -> bytes:
        """
        从WAD文件中提取指定内部路径的文件数据。

        :param wad: WAD对象实例。
        :param wad_file: 目标WAD文件。
        :param internal_path: 需要提取的内部文件路径。
        :return: 提取的文件字节内容。
        """
        logger.debug(f"从WAD文件 {wad_file.name} 中提取内部文件: {internal_path}")
        path_hash = WAD.get_hash(internal_path)
        for file_entry in wad.files:
            if file_entry.path_hash == path_hash:
                required_chunks = cls._get_required_chunks(wad_file, file_entry)
                wad_data = wad_file.download_chunks(required_chunks)[
                    : file_entry.compressed_size + file_entry.offset
                ]
                logger.debug(f"成功从WAD文件 {wad_file.name} 中提取文件: {internal_path}")
                return wad.extract_by_section(file_entry, None, True, wad_data)

        logger.error(f"未能在WAD文件 {wad_file.name} 中找到内部文件: {internal_path}")
        raise FileNotFoundError(f"在WAD文件中未找到路径 {internal_path} 对应的文件。")

    @classmethod
    def _get_required_chunks(
        cls, wad_file: PatcherFile, file_entry
    ) -> List[PatcherChunk]:
        """
        获取提取指定文件数据所需的chunks列表。

        :param wad_file: 目标WAD文件。
        :param file_entry: WAD中的文件条目。
        :return: 所需的chunks列表。
        """
        logger.debug(f"计算文件 {file_entry} 在WAD文件 {wad_file.name} 中所需的chunks")
        required_chunks = []
        accumulated_size = 0

        for chunk in wad_file.chunks:
            accumulated_size += chunk.target_size
            if accumulated_size >= file_entry.offset:
                required_chunks.append(chunk)
            if (
                accumulated_size
                >= file_entry.first_subchunk_index
                + file_entry.offset
                + file_entry.compressed_size
            ):
                break

        logger.debug(f"完成计算文件 {file_entry} 在WAD文件 {wad_file.name} 中所需的chunks")
        return required_chunks
