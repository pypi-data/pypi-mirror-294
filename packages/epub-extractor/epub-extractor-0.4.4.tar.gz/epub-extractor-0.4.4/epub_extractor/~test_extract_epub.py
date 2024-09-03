#!/usr/bin/env python3
import os
import shutil

from epub_extractor import EpubExtractor

def main():
    project_dir = os.path.dirname(os.path.dirname(__file__))
    if os.path.exists(
        os.path.join(project_dir, 'test-epubs', 'BT000065827200100101')
    ):
        shutil.rmtree(
            os.path.join(project_dir, 'test-epubs', 'BT000065827200100101'))

    epub_file = os.path.join(
        project_dir, 'test-epubs', 'BT000065827200100101.epub'
    )

    EpubExtractor(epub_file_path=epub_file).extract_images()

if __name__ == '__main__':
    main()
