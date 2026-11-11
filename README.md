sleepi4-utils
==========

slee-Pi 4 / slee-Pi 4 Lite を操作するためのツール類を提供します。

slee-Pi 4 Lite では次の点に注意してください。

* sleepi4ctl
  + get サブコマンド
    - current, power, energy は測定できません。  
    - extin, extin-count, extin-powerdown, extin-trigger, extout の CHANNEL に 2 を指定しないでください。  
  + set サブコマンド
    - extin-powerdown, extin-trigger, extout の CHANNEL に 2 を指定しないでください。  
    - restore-voltage は定格電圧の 24000 未満に設定してください。  
* /etc/default/sleepi4
  + EXTIN2_FORCED_SHUTDOWN は 0 に設定してください。

## 提供ファイル
次のファイルがパッケージに含まれています。

### /usr/sbin/sleepi4alarm
RTC のアラームを操作するスクリプトです。  
/sys/class/rtc/${RTC_DEVICE}/wakealarm にアクセスします。  
RTC_DEVICE の値は /etc/default/sleepi4 に記述します。

* -g, get  
  アラーム時刻を取得します。  
  未設定の場合は空の文字列を返します。  

* -s, set \<STRING\>  
  アラーム時刻を設定します。  
  翌年同日の一日前までが指定可能です。  

  \<STRING\> : 時刻を指定します。

  次に例を示します。

  - 2017/03/17 19:00:00 に設定する場合
    ``` bash
    sleepi4alarm set "2017/03/17 19:00:00"
    ```
    日時を指定してアラームを設定できます。  
    時刻のみの指定も可能です。

  - 五分後に設定する場合  
    ``` bash
    sleepi4alarm set "+5min"
    ```
    相対値を指定してアラームを設定できます。  
    year, month, day, hour, min, sec 等の指定が可能です。  

  - 翌日午前九時に設定する場合  
    ``` bash
    sleepi4alarm set "tomorrow 9:00"
    ```
    相対値と絶対値を組み合わせてアラームを設定することもできます。

  以上の例で示した文字列のフォーマットは GNU date コマンドに準拠しています。  
  フォーマットの詳細については次の URL を参照してください。  
  https://www.gnu.org/software/coreutils/manual/html_node/Date-input-formats.html

* -c, clear  
  アラーム設定を解除します。

* -h, help  
  ヘルプを表示します。

* -v, version  
  バージョンを表示します。

### /usr/sbin/sleepi4ctl
slee-Pi 4 を操作するための実行ファイルです。  
使用可能なオプションを次に示します。

* -g, get PARAMETER [\<CHANNEL\>]  
  指定したパラメータの値を取得します。  

  パラメータには次のいずれかを指定します。

  - current  
    供給電流の値を表示します。  
    単位は [mA] です。

  - energy  
    積算電力量の値を表示します。  
    単位は [mWh] です。  
    4294967295 の次は 0 に戻ります。

  - extin \<1|2\>  
    + \<CHANNEL\>  
      1 : CN4 の状態を表示します。  
      2 : CN6 の状態を表示します。  
      slee-Pi 4 Lite では 2 を指定しないでください。  

    0 : 外部入力はオフです。  
    1 : 外部入力はオンです。

  - extin-count \<1|2\>  
    + \<CHANNEL\>  
      1 : CN4 のカウント値を表示します。  
      2 : CN6 のカウント値を表示します。  
      slee-Pi 4 Lite では 2 を指定しないでください。  

    カウント値の単位は [秒] です。  
    最大値は 255 です。

  - extin-powerdown \<1|2\>  
    + \<CHANNEL\>  
      1 : CN4 による強制電源断の設定を表示します。  
      2 : CN6 による強制電源断の設定を表示します。  
      slee-Pi 4 Lite では 2 を指定しないでください。  

    0 : 外部入力による強制電源断が無効です。  
    1 : 外部入力による強制電源断が有効です。

  - extin-trigger \<1|2\>  
    + \<CHANNEL\>  
      1 : CN4 の起動トリガの設定を表示します。  
      2 : CN6 の起動トリガの設定を表示します。  
      slee-Pi 4 Lite では 2 を指定しないでください。  

    0 : エッジ検出で起動します。  
    1 : レベル検出で起動します。

  - extout \<1|2\>  
    + \<CHANNEL\>  
      1 : CN5 の出力を表示します。  
      2 : CN7 の出力を表示します。  
      slee-Pi 4 Lite では 2 を指定しないでください。  

    0 : 外部出力はオフです。  
    1 : 外部出力はオンです。

  - measurement-interval  
    入力電圧の計測間隔を表示します。  
    単位は [秒] です。

  - power  
    供給電力の値を表示します。  
    単位は [mW] です。

  - restart  
    システムが無応答と判定された場合の動作設定を表示します。  

    0 : 電源断を行います。  
    1 : 電源の再投入を行います。

  - restore-voltage \<1|2\>  
    + \<CHANNEL\>  
      1 : CN1 の復帰電圧を表示します。  
      2 : CN2 の復帰電圧を表示します。  

    単位は [mV] です。  
    0 の場合は無効です。

  - ri-trigger  
    RI 信号の起動トリガの設定を表示します。  

    0 : エッジ検出で起動します。  
    1 : レベル検出で起動します。

  - sleep-timeout  
    スリープ動作へ移行するタイムアウト値を表示します。  
    単位は [秒] です。  
    0 の場合は無効です。

  - switch  
    プッシュスイッチの状態を表示します。  

    0 : プッシュスイッチはオフです。  
    1 : プッシュスイッチはオンです。

  - switch-count  
    プッシュスイッチが押下されている時間のカウント値を表示します。  
    単位は [秒] です。  
    最大値は 255 です。

  - uvlo \<1|2\>  
    + \<CHANNEL\>  
      1 : CN1 のアラーム発生時の低電圧動作防止機能の状態を表示します。  
      2 : CN2 のアラーム発生時の低電圧動作防止機能の状態を表示します。  

    0 : 低電圧動作防止機能は無効です。  
    1 : 低電圧動作防止機能は有効です。

  - voltage \[1|2|active|all\]  
    入力電圧の値を表示します。  
    単位は [mV] です。  
    オプションは省略できます。  
    省略した場合は active になります。  

    1 : CN1 の入力電圧の値を表示します。  
    2 : CN2 の入力電圧の値を表示します。  
    active : CN1, CN2 の入力電圧のうち大きい方の値を表示します。  
    all : CN1, CN2 の入力電圧の値を表示します。

  - wakeup-flag  
    起動ステータスレジスタのフラグを表示します。  

    poweron : 電源接続が起動要因です。  
    watchdog : ウォッチドッグタイマのタイムアウトによる再起動が起動要因です。  
    alarm : リアルタイムクロックのアラーム発生が起動要因です。  
    switch : プッシュスイッチの押下が起動要因です。  
    extin1 : CN4 の検出が起動要因です。  
    extin2 : CN6 の検出が起動要因です。  
    ri : RI 信号の検出が起動要因です。  
    restoration1 : CN1 の電源復旧の検知が起動要因です。  
    restoration2 : CN2 の電源復旧の検知が起動要因です。  
    uvlo1 : CN1 の低電圧によりアラーム起動を見送ったことを示します。  
    uvlo2 : CN2 の低電圧によりアラーム起動を見送ったことを示します。

  - wakeup-status  
    起動ステータスレジスタの値を表示します。

  - watchdog-boot-timeout  
    Raspberry Pi への電源供給開始時に初回の応答を検知するまでのタイムアウト値を表示します。  
    単位は [秒] です。  
    0 の場合は即座にシステムの応答の検知に移行します。

  - watchdog-timeout  
    システムの応答を検知するタイムアウト値を表示します。  
    単位は [秒] です。  
    0 の場合は無効です。
    
* -s, set PARAMETER [\<CHANNEL\>] \<VALUE\>  
  指定したパラメータに値を設定します。  
  パラメータには次のいずれかを指定します。

  - energy \<0\>  
    + \<VALUE\>  
      0 : 積算電力量をクリアします。  
      0 クリアのみ可能です。  

  - extin-powerdown \<1|2\> \<0|1\>  
    + \<CHANNEL\>  
      1 : CN4 による強制電源断を設定します。  
      2 : CN6 による強制電源断を設定します。  
      slee-Pi 4 Lite では 2 を指定しないでください。  

    + \<VALUE\>  
      0 : 外部入力による強制電源断が無効です。  
      1 : 外部入力による強制電源断が有効です。  

  - extin-trigger \<1|2\> \<0|1\>  
    + \<CHANNEL\>  
      1 : CN4 の起動トリガを設定します。  
      2 : CN6 の起動トリガを設定します。  
      slee-Pi 4 Lite では 2 を指定しないでください。  

    + \<VALUE\>  
      0 : エッジ検出で起動します。  
      1 : レベル検出で起動します。  

  - extout \<1|2\> \<0|1\>  
    + \<CHANNEL\>  
      1 : CN5 の出力を設定します。  
      2 : CN7 の出力を設定します。  
      slee-Pi 4 Lite では 2 を指定しないでください。  

    + \<VALUE\>  
      0 : 外部出力はオフです。  
      1 : 外部出力はオンです。  

  - measurement-interval \<0..255\>  
    + \<VALUE\>  
      入力電圧の計測間隔を設定します。  
      単位は [秒] です。  
      最大値は 255 です。  
      0 を設定すると計測を行いません。

  - restart \<0|1\>  
    + \<VALUE\>  
      システムが無応答と判定された場合の動作を設定します。  

      0 : 電源断を行います。  
      1 : 電源の再投入を行います。

  - restore-voltage \<1|2\> \<0..48000\>  
    + \<CHANNEL\>  
      1 : CN1 の復帰電圧を設定します。  
      2 : CN2 の復帰電圧を設定します。  

    + \<VALUE\>  
      スリープ時に計測された入力電圧が設定した値を上回った場合に起動します。  
      単位は [mV] です。  
      0 の場合は無効です。  
      slee-Pi 4 Lite の入力電圧は 6〜24V のため、24000 を超える値では起動できません。

  - ri-trigger \<0|1\>  
    + \<VALUE\>  
      RI 信号の起動トリガを設定します。  

      0 : エッジ検出で起動します。  
      1 : レベル検出で起動します。

  - sleep-timeout \<0..255\>  
    + \<VALUE\>  
      スリープ動作へ移行するタイムアウト値を設定します。  
      単位は [秒] です。  

      0 : スリープ動作へ移行しません。  
      1..255 : 設定値を超えても応答を検知できない場合はスリープ動作へ移行します。

  - uvlo \<1|2\> \<0|1\>  
    + \<CHANNEL\>  
      1 : CN1 のアラーム発生時の低電圧動作防止機能を設定します。  
      2 : CN2 のアラーム発生時の低電圧動作防止機能を設定します。  

    + \<VALUE\>  
      0 : 低電圧動作防止機能は無効です。  
      1 : 低電圧動作防止機能は有効です。

  - watchdog-boot-timeout \<0..255\>  
    + \<VALUE\>  
      Raspberry Pi への電源供給開始時に初回の応答を検知するまでのタイムアウト値を設定します。  
      単位は [秒] です。  
      0 の場合は即座にシステムの応答の検知に移行します。

  - watchdog-timeout \<0..255\>  
    + \<VALUE\>  
      システムの応答を検知するタイムアウト値を設定します。  
      単位は [秒] です。  

      0 : 応答を検知しません。  
      1..255 : 設定値を超えても応答を検知できない場合は無応答と判定されます。

* -h, help  
  ヘルプを表示します。

* -v, version  
  バージョンを表示します。

### /etc/default/sleepi4   
slee-Pi 4 の設定を行うためのファイルです。  
設定可能な項目を次に示します。

* RTC_DEVICE  
  slee-Pi 4 のリアルタイムクロックモジュール部のデバイス名を記述します。  
  デフォルトは rtc0 です。

* HCTOSYS  
  リアルタイムクロックからシステムへ時刻を同期する動作の設定です。  
  デフォルトは yes です。  

  yes : 起動時に時刻を同期します。  
  no : 起動時に時刻を同期しません。  

* SYSTOHC  
  システムからリアルタイムクロックへ時刻を同期する動作の設定です。  
  デフォルトは yes です。  

  yes : 終了時に時刻を同期します。  
  no : 終了時に時刻を同期しません。  

* I2C_ADDRESS  
  slee-Pi 4 のパワーマネジメントモジュール部の I2C アドレスを指定します。  
  デフォルトは 0x6E です。

* HEARTBEAT_PIN  
  ソフトウェアハートビートを出力する GPIO の番号です。  
  JP3 の設定に合わせて 5 または 24 を指定します。  
  デフォルトは 5 です。

* HEARTBEAT_TIMEOUT  
  システムの応答がない場合に電源を再投入するまでの時間です。  
  単位は [秒] です。  
  無効にするには 0 を指定します。  
  デフォルトは 60 です。

* RETRY_BOOT  
  起動に失敗してシステムの応答がない場合に電源の再投入を行う設定です。  
  有効にするには 1 を指定します。  
  無効にするには 0 を指定します。  
  デフォルトは 1 です。

* BOOT_TIMEOUT  
  システムの起動時にウォッチドッグタイマが動作を開始するまでの時間です。  
  単位は [秒] です。  
  無効にするには 0 を指定します。  
  デフォルトは 90 です。

* POWEROFF_DELAY  
  システムのシャットダウンが完了してから電源断までの時間です。  
  単位は [秒] です。  
  無効にするには 0 を指定します。  
  デフォルトは 10 です。

* EXTIN1_FORCED_SHUTDOWN  
  外部入力 1（CN4）が 10 秒以上検出された場合に強制電源断を行う設定です。  
  有効にするには 1 を指定します。  
  無効にするには 0 を指定します。  
  デフォルトは 0 です。  

* EXTIN2_FORCED_SHUTDOWN  
  外部入力 2（CN6）が 10 秒以上検出された場合に強制電源断を行う設定です。  
  有効にするには 1 を指定します。  
  無効にするには 0 を指定します。  
  デフォルトは 0 です。

### /usr/lib/sleepi4-utils/hctosys.sh  
リアルタイムクロックからシステムへ時刻を同期するスクリプトファイルです。

### /usr/lib/sleepi4-utils/config.py  
slee-Pi 4 の起動、再起動、停止の設定を行うスクリプトファイルです。

### /usr/lib/sleepi4-utils/systohc.sh  
システムからリアルタイムクロックへ時刻を同期するスクリプトファイルです。

### /usr/lib/sleepi4-utils/timeoutpid.sh  
コマンド実行時にタイムアウト動作を行うスクリプトファイルです。

### /usr/share/bash-completion/completions/sleepi4alarm
sleepi4alarm のコマンド補完を行うための設定ファイルです。

### /usr/share/bash-completion/completions/sleepi4ctl
sleepi4ctl のコマンド補完を行うための設定ファイルです。

### /usr/share/sleepi4-utils/sleepi4_util.py
slee-Pi 4 をコマンド操作するためのヘルパクラスが実装されたファイルです。

### /usr/share/doc/sleepi4-utils/changelog.gz  
パッケージの変更履歴を記録したファイルです。

### /usr/share/doc/sleepi4-utils/copyright  
ソースの著作権とライセンスを記載したファイルです。

### /usr/lib/udev/rules.d/85-sleepi4-utils.rules  
slee-Pi 4 のデバイスを定義した設定ファイルです。

### /usr/lib/systemd/system/sleepi4-halt.service  
システムの停止（halt）時に slee-Pi 4 の設定を行うサービスです。  
電源断は行いません。

### /usr/lib/systemd/system/sleepi4-hctosys.service  
リアルタイムクロックからシステムへ時刻を同期するサービスです。

### /usr/lib/systemd/system/sleepi4-heartbeat.service  
ソフトウェアハートビートを実行するサービスです。

### /usr/lib/systemd/system/sleepi4-restart.service  
slee-Pi 4 の再起動設定を行うサービスです。

### /usr/lib/systemd/system/sleepi4-start.service  
slee-Pi 4 の起動設定を行うサービスです。

### /usr/lib/systemd/system/sleepi4-stop.service  
システムの電源オフ（poweroff）時に slee-Pi 4 の設定を行うサービスです。  
POWEROFF_DELAY の時間が経過すると電源断を行います。

### /usr/lib/systemd/system/sleepi4-systohc.service  
システムからリアルタイムクロックへ時刻を同期するサービスです。
