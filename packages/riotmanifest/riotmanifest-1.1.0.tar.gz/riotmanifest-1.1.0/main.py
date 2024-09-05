# -*- coding: utf-8 -*-
# @Author  : Virace
# @Email   : Virace@aliyun.com
# @Site    : x-item.com
# @Software: Pycharm
# @Create  : 2024/3/12 22:19
# @Update  : 2024/9/5 17:56
# @Detail  : 

import sys

from riotmanifest import WADExtractor
from riotmanifest.external_manifest import ResourceDL
from loguru import logger

logger.configure(handlers=[dict(sink=sys.stdout, level="DEBUG")])
logger.enable("riotmanifest")


def extra_test():
    we = WADExtractor(r"C:\Users\Virace\Downloads\DE515F568F4D9C73.manifest")
    data = we.extract_files(
        {
            "DATA/FINAL/Champions/Aatrox.wad.client": [
                "data/characters/aatrox/skins/skin0.bin",
                "data/characters/aatrox/skins/skin1.bin",
                "data/characters/aatrox/skins/skin2.bin",
                "data/characters/aatrox/skins/skin3.bin",
            ],
            "DATA/FINAL/Champions/Ahri.wad.client": [
                "data/characters/Ahri/skins/skin0.bin",
                "data/characters/Ahri/skins/skin1.bin",
                "data/characters/Ahri/skins/skin2.bin",
                "data/characters/Ahri/skins/skin3.bin",
            ]
        }
    )
    print(len(data))


def main():
    rdl = ResourceDL(r'C:\Users\Virace\Downloads\Programs\1')
    rdl.d_game = True
    rdl.download_resources('content-metadata.json')
    


if __name__ == "__main__":
    # asyncio.run(main())
    main()
    # manifest = PatcherManifest(r"https://lol.secure.dyn.riotcdn.net/channels/public/releases/AB8447A8C9D41A42.manifest")
    # manifest = PatcherManifest(r"C:\Users\Virace\Downloads\AB8447A8C9D41A42.manifest",
    #                            save_path=r"H:\Programming\Python\PyManifest\temp")
    # for file in manifest.files.values():

    # chunks = file.chunks
    # for chunk in chunks:
    #     print(chunk.size, chunk.target_size)
    # print(len(chunks))
    #
    # # 将chunks按bundle_id分组， 去重
    # chunk_group = {}
    # for chunk in chunks:
    #     if chunk.bundle.bundle_id not in chunk_group:
    #         chunk_group[chunk.bundle.bundle_id] = set()
    #     chunk_group[chunk.bundle.bundle_id].add(chunk)
    # print(len(chunk_group))
    # if file.name == 'Plugins/rcp-be-lol-game-data/default-assets.wad':
    #     logger.info(f"开始下载...{file.name}")
    #     manifest.download_file(file)
    #     logger.info(f"下载完毕...{file.name}")

