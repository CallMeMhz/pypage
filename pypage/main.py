import argparse

from pypage.generator import ArticleGenerator


def parse_arguments():
    parser = argparse.ArgumentParser(description="""Convert markdown file to static html file""")
    parser.add_argument(dest='path', nargs='?', default='content')
    parser.add_argument('-o', '--output', dest='output_path', default='output', help='where to out put')
    return parser.parse_args()


def main():
    args = parse_arguments()
    ag = ArticleGenerator(
        INPUT_PATH=args.path,
        OUTPUT_PATH=args.output_path
    )
    ag.generate()

    print('Finish!')
