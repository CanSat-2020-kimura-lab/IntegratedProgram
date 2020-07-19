# プログラム概要
・スタック回避のためのプログラム

# 関数一覧
## ● get_accdata
九軸センサから加速度センサとを読み取るプログラム
### 引数
・なし
### 返り値
・accx , accy , accz : 加速度センサのx,y,z軸成分 <br>

***

## ● stuck_detection1
スタック検知のためにGPSから緯度、経度を事前に保持しておくプログラム
### 引数
・なし
### 返り値
・longitude_past,latitude_past : 取得した緯度、経度

***

## ● stuck_detection2
スタック検知のために新たにGPSから取得した緯度、経度と、stuck_detection1で記憶した値を用いてその2点間の距離を計算する。<br>
gps_navigate.py(path : Detection/Run_phase)を用いて計算している
### 引数
・longitude_past,latitude_past : stuck_detection1で得た緯度、経度
### 返り値
・distance : gps_navigate.pyの返り値の内、2点間の距離を表す値のみ

***

## ● stuck_confirm
スタックしているかを確認するプログラム。<br> 
はじめに前進し、加速度センサの値に正の相関がみられなかった場合はスタックしていると判定する。(加速していないため)
### 引数
・なし
### 返り値
・move_judge : 加速度センサx軸の値の相関係数

***

## ● stuck_escape
前進できない場合に一度後ろに下がってから、方向を変えて再び前進することでスタック回避するプログラム
### 引数
・move_judge : 加速度センサx軸の値の相関係数。stuck_confirmの返り値。
### 返り値
・なし

***

## ● plot_data
加速度センサと時間の相関を図示して視覚的に確かめるテスト用プログラム
### 引数
・accx_data : 加速度センサの行列。stuck_confirmで得た値。<br> 
・time_array : 加速度センサの値を取得した時間の行列。stuck_confirmで得た値。<br> 
どちらも返り値として返していないがglobal関数でつなげているため大丈夫だった気がする。(20/07/20)
### 返り値
・なし

***

## ● cober / cor
相関係数を求めるためのプログラム。corの返り値「cor」のみ使えばよい。<br> 
詳しくは参考文献へ

***
## ● timer
並列処理をすることで「x秒間プログラムを実行する」ことが可能。
### 引数
・t : 実行したい時間を自由に定義できる
### 返り値
・なし
### 使い方
```
    global cond
    cond = True
    thread = Thread(target = timer,args=([t])) #tに任意の数を入れることで実行した時間を決められる。
    thread.start()
    while cond:
        処理したいプログラム
```

***

# 参考文献
## 関数の呼び出し方
・[Pythonでreturnを使う方法【初心者向け】](https://techacademy.jp/magazine/18886) : 返り値がある場合どのように呼び出せばいいか <br> 
・[Python 〜複数の戻り値（返り値）にタプルやオブジェクトを使う](https://itstudio.co/2019/06/05/9313/) : 複数返り値がある場合はタプルになる <br> 
・[タプルの要素の取り出し方](https://www.javadrive.jp/python/tuple/index2.html) <br> 
・[辞書でキーを指定して値を取得する](https://www.javadrive.jp/python/dictionary/index2.html) <br>
## プログラムの詳細
・[Pythonで相関係数を計算する練習](https://qiita.com/FujiedaTaro/items/f06e3d49c319b26322eb) : 相関係数を計算する <br>
・[【NumPy入門 np.append】配列末尾に要素を追加するappend関数](https://www.sejuku.net/blog/68941)<br>
・[python で [:,0] といった記法があるのですが、どういった意味でしょうか？](https://teratail.com/questions/13705)<br>
・[matplotlibでのプロットの基本](https://qiita.com/KntKnk0328/items/5ef40d9e77308dd0d0a4)<br>
