#!/usr/bin/env python3
import os
import shutil

from epub_extractor import EpubExtractor

def main():
    project_dir = os.path.dirname(os.path.dirname(__file__))
    # contents_id = 'BT000065827200100101'
    # チワワスタイル
    # contents_id = 'BT000091605700300301'
    # アロハ
    contents_id = 'BT000043193600800801'


    if os.path.exists(
        os.path.join(project_dir, 'test-epubs', contents_id)
    ):
        shutil.rmtree(
            os.path.join(project_dir, 'test-epubs', contents_id))

    epub_file = os.path.join(
        project_dir, 'test-epubs', f'{contents_id}.epub'
    )

    EpubExtractor(epub_file_path=epub_file).extract_images(delete_exists_dir=True)

if __name__ == '__main__':
    main()
