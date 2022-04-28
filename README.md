# Markdown-Latex Convertor
Markdownをlatexに変換するプログラム
## 使用法
### モジュールとして使用
`import mdtoLatex`でモジュールをロード。
```python
  # インスタンスの生成
  [変数名] = mdtoLatex.md2latex()
  # マークダウンファイルのロード
  [変数名].loadMD(String:File Path)
  # マークダウンを変換
  [変数名].cvtMD2Latex()
  # latexファイルを出力
  [変数名].exportLatex(String:File Path)
  # 変換に関する設定
  # 生成形式を指定
  [変数名].is_include_file = [True or False] # Trueで埋め込み用のファイルとして出力。(プリアンブルをつけない)
  # math指定時の空間を指定(デフォルトはgather)
  [変数名].math_field = [String]
  # プリアンブルの設定
  # 追加
    [変数名].preamble.append(String) # \\usepackage{amsmath,amssymb}のように記述
  # 削除は頑張ってpopする
```
### 直接変換を行う
  以下のコマンドを実行
  ```
    python3 md2latex.py inputFilePath outputFilePath
  ```
## 変換可能な文法

以下のMarkdownの文法を認識する
* ヘディング

* コメントブロック

* コードブロック

  - mathを指定することでlatexによる数式を記述可能

* インラインコードブロック

* インライン数式

* 表

  - 2行目をデータの位置指定として解釈する

  - :---, :---:, ---:以外の入力は左寄せと解釈する

* リスト

  - *, -の後ろに空白がない場合エラーが発生する。エラー内容`IndexError: pop from empty list`

* 斜体、太字

* 画像

  - 代替テキストをラベル、タイトルをキャプションとして設定を行う

### 独自の拡張

* `: caption`で表、ソースコードにキャプションを設定

  - `: caption[label]`でキャプションとラベルを設定
  - 参照は(@label)を使用

* YAML表記でtitle,date,authorを設定

### 認識できるコード

````md
  # h1
  ## h2
  ### h3
  #### h4
  ##### h5
  <!--
    コメント
  -->
   ```cpp
    #include <cstdint>
    int main(int argc, char const *argv[]) {
      /* code */
      return 0;
    }
   ```
   ```math
    \int_{-\infty}^{\infty}x^2 dx
   ```
   inlinecode`hoge`
   inline$e^{i\theta}$
   | Header One     | Header Two     |
   | :------------- | :------------- |
   | Item One       | Item Two       |

   * item1
   * item2
      - item3
        -item4
   * item5
   **bold text** *italic text*
   ![hogehoge](fugafuga.png "it is piyopiyo")
````
### 生成されるコード
```latex
\section{h1}
\subsection{h2}
\subsubsection{h3}
\paragraph{h4}
\subparagraph{h5}
%
%  コメント
\par
 \scriptsize \hrulefill
 \begin{description}

\item[1] \texttt{\ \ \#include\ \textless cstdint\textgreater }
\item[2] \texttt{\ \ int\ main(int\ argc,\ char\ const\ *argv[])\ \{}
\item[3] \texttt{\ \ \ \ /*\ code\ */}
\item[4] \texttt{\ \ \ \ return\ 0;}
\item[5] \texttt{\ \ \}}
\end{description}
 \hrulefill
 \normalsize
 \par
\begin{gather}
  \int_{-\infty}^{\infty}x^2 dx
\end{gather}
 inlinecode\texttt{hoge}
 inline$e^{i\theta}$
\begin{table}[h]
 \caption{}\centering
  \begin{tabular}{|l|l|}
\hline
\textbf{ Header One     }&\textbf{ Header Two     }\\ \hline
 Item One       & Item Two       \\ \hline

\end{tabular}
\end{table}
\par
\begin{itemize}
 \item item1
\item item2
\begin{itemize}
 \item item3
\begin{itemize}
 \item item4
\end{itemize}
\end{itemize}
\item item5
\end{itemize}
 \textbf{bold text} \textit{italic text}
\begin{figure}[h]
\centering
  \includegraphics[keepaspectratio,width=0.8\linewidth]{fugafuga.png}
  \caption{it is piyopiyo}
  \label{hogehoge}
\end{figure}
```
# 変更履歴
### Date: 2022-4-28
アップロード
<!-- *** -->
