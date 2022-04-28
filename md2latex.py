import mdtoLatex
import sys
def main(arg):
    if len(arg)>=2:
        ldMd = mdtoLatex.md2latex()

        if ldMd.loadMD(arg[0]).cvtMD2Latex():
            ldMd.exportLatex(arg[1])
        else:
            print("ファイルを読み込めませんでした")
    else:
        print("引数が不足しています。入力ファイルパス、出力ファイルパスの2つを指定してください")
if __name__ == '__main__':
    main(sys.argv[1:])
