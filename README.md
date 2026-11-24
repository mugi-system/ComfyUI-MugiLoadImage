# mugi_load_image

元のファイル名を覚えていてくれる LoadImage です。

## 何をするノードか

標準の LoadImage は、マスクエディタで塗って保存した瞬間に、選んでいた
ファイル名が clipspace の一時ファイル名に書き換わってしまいます。
このノードは「元のファイル名」欄を別に持ち、絵を選んだときにそこへ
名前を退避させます。マスクを塗っても元の名前は残り、3つ目の出力
（filename）から拡張子なしの名前が文字列で出ます。

保存ノードの filename_prefix にこの出力をつなぐと、元の名前で
保存できます（末尾の連番 _00001_ は ComfyUI の仕様で付きます）。

## 入れ方

1. このフォルダ（mugi_load_image）ごと、ComfyUI の custom_nodes
   フォルダに入れる
   例：Q:\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\custom_nodes\mugi_load_image
2. ComfyUI を再起動する
3. ノード追加メニューの「mugi」カテゴリに
   「Load Image (mugi / keeps filename)」が出ます

## 使い方

- 絵の選び方は標準の LoadImage と同じ（プルダウン／ドラッグ＆ドロップ）
- 選ぶと「original_filename」欄に元のファイル名が自動で入ります
  （間違っていたら手で直しても大丈夫です）
- マスクエディタで塗っても、その欄は書き換わりません
- IMAGE / MASK / filename の3出力です。MASK は標準と同じく、
  塗ったマスクがそのまま出ます

## サンプルワークフロー

`example_workflows/mosaic_workflow_v3.json` に、手動モザイク用ワークフローの
例があります。このノードで絵を読み、マスクエディタで塗ると、ブロックサイズは
長辺/100 で自動計算され、保存名は「元のファイル名_masked」になります。
ComfyUI にドラッグすると読み込めます。
