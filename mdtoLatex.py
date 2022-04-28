import re
class md2latex():
    # 出力形式
    is_include_file = False
    # タイトル表示
    makeTitle = True
    # プリアンブル
    preamble = [
        "\\documentclass{jsarticle}",
        "\\usepackage{amsmath,amssymb}",
        "\\usepackage[usenames]{color}",
        "\\usepackage[option]{colortbl}",
        "\\usepackage[dvipdfmx]{graphicx}",
        "\\usepackage{verbatim}"
    ]
    # 数式のフィールド名
    math_field = "gather"
    # メタデータ
    metaData = {"title":"","author":"","date":""}
    # 読み込んだmdデータ
    __md_data = []
    # 変換したlatexデータ
    __latex_txtData=[]
    # 見出し
    __section = re.compile('^(#+) ?(.+)')
    # コメント 開始
    __comment_start = re.compile('^\s*<!--(.*| *)')
    # コメント 終了
    __end_comment = re.compile('(.*| *)-->\n?$')
    # コードブロック 開始
    __codeBlock_start = re.compile('^\s*```(.*)')
    # コードブロック 終了
    __codeBlock_end = re.compile('(.*)```\s*\n?$')
    # リスト
    __list_1st = re.compile('^(\s*)(-|\*) +(.+)')
    # table
    __table_set = re.compile('^\s*\|([^\|]+)(.+)')
    # 改行
    __par_check = re.compile('^(\s*)\n')
    # bold
    __bold__as_start = re.compile('^(.*)\*{2}(.*)\*{2}(.*)')
    # イタリック
    __italic_block = re.compile('^([^*]*)\*([^*]*)\*(.*)')
    #インラインコードブロック
    __inlineCode_block2 = re.compile('(.*?)`{2}(.*)`{2}(.*)')
    __inlineCode_block1 = re.compile('([^`]*?)`([^`]+)`(.*)')
    # インライン数式ブロック
    __inline_math_code = re.compile('([^\$]*?)\$([^\$]*)\$(.*)')
    # 参照
    __ref_item = re.compile('^(.*?)\(@(\w+)\)(.*)')
    # 画像
    __image_block_nonTitle = re.compile('^[\ \t]*?!\[([^\]]*)\]\(([^\(\"]*)\"?([^\(\"]*)\"?\)')
    # キャプションの定義
    __caption_txt_block = re.compile('^\s*: (.*)\n')
    #メタデータ終了、開始宣言
    __start_end_yaml = re.compile('^\s*---(.|\n)*')
    def __init__(self, fName):
        with open(fName) as f:
            self.__md_data = f.readlines();
        return self
    def __init__(self):
        pass

    # ./,spaceを取り除く
    def __remove_dot_sl(self, text):
        getFname = re.compile("^(./)*(\S+)")
        res = getFname.match(text)
        return res.group(2)
    # 特殊文字のエスケープ
    def escape_chars(self, text):
        str = text.replace("\n",'')
        str = str.replace("\\","\\textbackslash ")
        str = str.replace(" ","\\ ")
        str = str.replace("#","\\#")
        str = str.replace("&","\\&")
        str = str.replace("<","\\textless ")
        str = str.replace(">","\\textgreater ")
        str = str.replace("$","\\$")
        str = str.replace("%","\\%")
        str = str.replace("_","\\_")
        str = str.replace("{","\\{")
        str = str.replace("}","\\}")
        str = str.replace("^","\\textasciicircum ")
        str = str.replace("|","\\textbar ")
        str = str.replace("~","\\textasciitilde ")
        return str
        # str = str.replace("","\\")
    # メタデータの読み取り
    def __get_Meta_data(self, text):
        _item_ = re.compile('\s*([a-zA-Z]+)\s*:\s*(.+)\n')
        res = _item_.match(text)
        if res:
            key_ = res.group(1)
            value_ = res.group(2)
            if key_ in ["title", "author", "date"]:
                # キーワードの変換
                if value_ in ["today"]:
                    value_ = "\\today"
                self.metaData[key_] = value_
    # 表の列データの取得
    def __check_table_col(self, colData, txt):
        res = self.__table_set.match(txt)
        if res:
            colData.append(res.group(1))
            return self.__check_table_col(colData,res.group(2))
        else :
            return colData
    # 配置指定子？をl,c,rへ変換
    def __check_table_data_pos(self, colData):
        right_ = re.compile('^\s*-{3,}')
        center_ = re.compile('^\s*:-{3,}:')
        ret_data = ""
        for data in colData:
            res = right_.match(data)
            if res:
                ret_data+="|r"
                continue
            res = center_.match(data)
            if res:
                ret_data+="|c"
                continue
            ret_data+="|l"
        ret_data+="|"
        return ret_data
    # 平文の解析
    def __txt_parase(self,text):
        retStr = ''
        # 太字(**txt**)
        res = self.__bold__as_start.match(text)
        if res:
            retStr = "%s\\textbf{%s}%s" % (
                self.__txt_parase(res.group(1)), self.__txt_parase(res.group(2)),
                self.__txt_parase(res.group(3))
            )
            return retStr
        # 斜体
        res = self.__italic_block.match(text)
        if res:
            retStr = "%s\\textit{%s}%s" % (
                self.__txt_parase(res.group(1)), self.__txt_parase(res.group(2)),
                self.__txt_parase(res.group(3))
            )
            return retStr
        # インラインコードブロック
        res = self.__inlineCode_block2.match(text)
        if res:
            resStr = "%s\\texttt{%s}%s" % (
                self.__txt_parase(res.group(1)), res.group(2), self.__txt_parase(res.group(3))
            )
            return resStr
        res = self.__inlineCode_block1.match(text)
        if res:
            resStr = "%s\\texttt{%s}%s" % (
                self.__txt_parase(res.group(1)), res.group(2), self.__txt_parase(res.group(3))
            )
            return resStr
        # インライン数式ブロック
        res = self.__inline_math_code.match(text)
        if res:
            resStr = "%s$%s$%s" % (
                self.__txt_parase(res.group(1)), res.group(2), self.__txt_parase(res.group(3))
            )
            return resStr
        # 参照を設定
        res = self.__ref_item.match(text)
        if res:
            print(res.group(1))
            print(res.group(2))
            print(res.group(3))
            resStr = "%s\\ref{%s} %s" % (
                self.__txt_parase(res.group(1)), res.group(2), self.__txt_parase(res.group(3))
            )
            return resStr
        retStr = text.replace("\\", "\\textbackslash ")
        retStr = retStr.replace("_", "\\_")
        retStr = retStr.replace("<","\\textless ")
        retStr = retStr.replace(">","\\textgreater ")
        retStr = retStr.replace("$","\\$")
        return retStr
    # コメントブロックの終了を判定
    def __check_end_comment_block(self, text):
        res = self.__end_comment.match(text);
        if res:
            temp = res.group(1);
            if len(temp) > 1:
                self.__latex_txtData.append('%' + temp)
            return False
        else:
            self.__latex_txtData.append('%' + text)
            return True
    # コードブロックの終了を判定
    def __check_end_code_block(self, text,line,isMath):
        res = self.__codeBlock_end.match(text);
        retParam = True
        str = ""
        if res:
            temp = res.group(1);
            if len(temp) > 2:
                str = temp
            retParam = False
        else:
            str = text
        if isMath:
            self.__latex_txtData.append((str.replace("\n","")))
        else:
            if retParam:
                self.__latex_txtData.append("\\item[%d] \\texttt{%s} "%(line,self.escape_chars(str)))
        return retParam

    # 見出しの場合分け
    def check_hedding_num(self, hashs, txt):
        num_h = len(hashs)
        cmd_ = "{%s}"
        if num_h == 1:
            cmd_ ="\\section{%s}"
        elif num_h == 2:
            cmd_="\\subsection{%s}"
        elif num_h == 3:
            cmd_="\\subsubsection{%s}"
        elif num_h == 4:
            cmd_="\\paragraph{%s}"
        elif num_h == 5:
            cmd_="\\subparagraph{%s}"

        self.__latex_txtData.append(cmd_ % (self.__txt_parase(txt)))
    def __end_table(self, text):
        self.__latex_txtData.append(text)
        self.__latex_txtData.append("\\end{tabular}\n\\end{table}")
    def __end_list(self, text):
        self.__latex_txtData.append("\\end{itemize}")
    # Markdownを分解してlatexに変換
    def __parse(self):
        commentBlock = False
        codeBlock = False
        line = 1
        latex_ = False
        list_ = False
        list_indents = []
        isTable = False
        tableRow = 0;
        tableCol = []
        tableTxt = '';
        # 0:Caption [1:label] 3:position
        table_data_pos="\\begin{table}[h]\n \\caption{%s} \n %s\\centering \n  \\begin{tabular}{%s}\n\\hline\n"
        caption_ = ''
        label_ = ''
        yamlBlock = False
        for mdString in self.__md_data:
            # コメントブロック内
            if commentBlock:
                commentBlock = self.__check_end_comment_block(mdString);
                continue
            # コードブロック内
            if codeBlock:
                codeBlock = self.__check_end_code_block(mdString,line,latex_)
                line+=1
                # コードブロックの終了
                if not codeBlock:
                    line = 1
                    if latex_:
                        # 数式入力
                        self.__latex_txtData.append("\\end{%s}"%(self.math_field))
                        latex_ = False
                    else :
                        # コード
                        self.__latex_txtData.append("\\end{description}\n \\hrulefill \n \\normalsize \n \\par")
                continue

            # コメント
            res = self.__comment_start.match(mdString)
            if res:
                commentBlock = self.__check_end_comment_block(res.group(1))
                continue
            # リスト
            res = self.__list_1st.match(mdString)
            if res:
                # 表の終了処理
                if isTable:
                    self.__end_table.append(tableTxt)
                    isTable = False
                    tableRow = 0
                    tableTxt = ""
                    tableCol.clear()
                # リストの開始
                list_ = True
                if len(list_indents) == 0:
                    list_indents.append(len(res.group(1)))
                    self.__latex_txtData.append("\\begin{itemize}\n \\item %s" % (self.__txt_parase(res.group(3))))
                elif list_indents[-1] < len(res.group(1)):
                    # リストをネスト
                    self.__latex_txtData.append("\\begin{itemize}\n \\item %s" % (self.__txt_parase(res.group(3))))
                    list_indents.append(len(res.group(1)))
                elif list_indents[-1] == len(res.group(1)):
                    # 同階層にデータを追加
                    self.__latex_txtData.append("\\item %s" % (self.__txt_parase(res.group(3))))
                else:
                    while len(list_indents) > 1 and list_indents[-1] > len(res.group(1)):
                        self.__latex_txtData.append("\\end{itemize}")
                        list_indents.pop()
                    self.__latex_txtData.append("\\item %s" % (self.__txt_parase(res.group(3))))
                continue
            if list_:
                list_ = False
                if len(list_indents)>1:
                    while list_indents.pop():
                        self.__latex_txtData.append("\\end{itemize}")
                else:
                    list_indents.pop()
                self.__latex_txtData.append("\\end{itemize}")
            # 表
            res = self.__table_set.match(mdString)
            if res:
                isTable = True
                tableRow += 1
                tableCol.append(res.group(1))
                tableCol = self.__check_table_col(tableCol, res.group(2))
                if tableRow == 2:
                    # データの配置を設定
                    if len(label_)>0:
                        label_ = "\\label{%s}\n"%(label_)
                    table_pos_temp = table_data_pos % (caption_, label_,self.__check_table_data_pos(tableCol))
                    tableTxt = table_pos_temp + tableTxt
                    if len(caption_) > 0:
                        caption_=''
                        label_ = ''
                else:
                    amp_ = ''
                    for data_ in tableCol:
                        if tableRow == 1:
                            data_ = '**%s**' % (data_)
                        tableTxt += amp_ + self.__txt_parase(data_)
                        amp_ = '&'
                    tableTxt += "\\\\ \\hline \n"
                tableCol.clear()
                continue
            if isTable:
                self.__end_table(tableTxt)
                tableTxt = ""
                isTable = False
                tableRow = 0
            # 表、コードのキャプション
            res = self.__caption_txt_block.match(mdString)
            if res:
                caption_ = res.group(1)
                # ラベルの取得
                temp_res = re.match("(.*)\[(.*)\]", caption_)
                if temp_res:
                    caption_=temp_res.group(1)
                    label_ = ''
                    label_= temp_res.group(2)
                # キャプションを変換
                caption_ = self.__txt_parase(caption_)
                continue
            # YAMLブロックの開始、終了を判断
            res = self.__start_end_yaml.match(mdString)
            if res:
                yamlBlock = not yamlBlock
                continue
            # YAMLデータ
            if yamlBlock:
                self.__get_Meta_data(mdString)
                continue
            # コードブロック
            res = self.__codeBlock_start.match(mdString)
            if res:
                # キャプションを挿入
                if len(caption_)>0:
                    if len(label_)>0:
                        self.__latex_txtData.append("\\listCaptionhaslabel{\label{%s}}{%s}"%(label_,caption_))
                        label_ = ''
                    else:
                        self.__latex_txtData.append("\\listCaption{%s}"%(caption_))
                    caption_ = ''
                code_temp = self.__codeBlock_end.match(res.group(1));
                if code_temp:
                    # インライン
                    self.__latex_txtData.append(code_temp.group(1))
                else:
                    # コードブロック
                    codeBlock = True
                    # 数式入力への対応
                    if res.group(1) == 'math':
                        latex_ = True
                        self.__latex_txtData.append("\\begin{%s}" % (self.math_field))
                    else :
                        self.__latex_txtData.append("\\par \n \\scriptsize \\hrulefill \n \\begin{description}\n ")
                continue
            # ヘディング(見出し)
            res = self.__section.match(mdString)
            if res:
                self.check_hedding_num(res.group(1),res.group(2))
                continue
            # 画像
            res = self.__image_block_nonTitle.match(mdString)
            if res:
                # 図の挿入
                self.__latex_txtData.append("\\begin{figure}[h]")
                self.__latex_txtData.append("\\centering")
                self.__latex_txtData.append(
                    "  \\includegraphics[keepaspectratio,width=0.8\\linewidth]{%s}"%(self.__remove_dot_sl(res.group(2)))
                )
                # キャプションの挿入
                if len(res.group(3)):
                    self.__latex_txtData.append("  \\caption{%s}"%(self.__txt_parase(res.group(3))))
                # ラベルの挿入
                if len(res.group(1)):
                    self.__latex_txtData.append("  \\label{%s}"%(res.group(1)))
                self.__latex_txtData.append("\\end{figure}")
                continue
            # 段落変更
            res = self.__par_check.match(mdString)
            if res:
                self.__latex_txtData.append("\\par")
                continue
            # 平文
            self.__latex_txtData.append(self.__txt_parase(mdString))
        # 表、リストを閉じる
        if isTable:
            self.__end_table(tableTxt)
        elif list_:
            self.__end_list()
        # 改行のみのデータを削除
        self.__latex_txtData = [
            ltxt_ for ltxt_ in self.__latex_txtData if ltxt_ != '\n' and len(ltxt_) > 0
        ]

    def loadMD(self, fName):
        with open(fName) as f:
            self.__md_data = f.readlines()
        return self

    def cvtMD2Latex(self):
        if len(self.__md_data) > 0:
            self.__parse();
            return True
        else:
            print("Markdown file is not loaded.")
            return False
    def exportLatex(self, FileName):

        has_bs_n = re.compile("(.+)\n$")
        with open(FileName,'w') as f:
            # プリアンブルの書き込み
            if not self.is_include_file:
                for pre in self.preamble:
                    f.write(pre + '\n')
                # タイトルの設定
                for k,v in self.metaData.items():
                    f.write("\\%s{%s}\n"%(k,v))

                f.write('\\begin{document}\n')
                # タイトルの挿入
                if self.makeTitle:
                    f.write('\\maketitle\n')
            # 変換データ用のコマンドを書き込み(リスト用キャプション)
            f.write(
                "\\newcounter{md_cvter_gen_listNumber}\n"
                "\\newcommand{\\listCaption}[1]{\n"
                "\\stepcounter{md_cvter_gen_listNumber} \\par\n"
                "\\centerline{リスト\\arabic{md_cvter_gen_listNumber}: #1}\n"
                "}\n"
                "\\newcommand{\\listCaptionhaslabel}[2]{\n"
                "\\refstepcounter{md_cvter_gen_listNumber}{#1} \\par\n"
                "\\centerline{リスト\\arabic{md_cvter_gen_listNumber}: #2}\n"
                "}\n"
            )
            # 変換したデータを書き込み
            for line_ in self.__latex_txtData:
                res = has_bs_n.match(line_)
                if res:
                    f.write(line_)
                else :
                    f.write(line_ + '\n')
            if not self.is_include_file:
                f.write('\\end{document}\n')
