#!/usr/bin/env python3

import os
from epub_dump_toc import procedure, EpubExtractor


def test():
    project_dir = os.path.dirname(os.path.dirname(__file__))
    # epub_file = os.path.join(
    #     project_dir, 'test-epubs', 'BT000027007500100101900206_001.epub')
    epub_file = os.path.join(
        project_dir, 'test-epubs', 'BT000012354200100101900206_001.epub'
    )
    data = procedure(epub_file)
    EpubExtractor.print_json(data)


if __name__ == '__main__':
    test()
