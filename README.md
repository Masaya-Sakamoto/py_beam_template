# ビーム動的制御プログラム

## 操作手順

1. 設定ファイルを作成
  - メイン設定ファイル
  - ビームテーブル構成ファイル
  - ビーム制御テーブル構成ファイル

2. DUの`nr-softmodem`を起動

3. UE接続まで待つ

4. DU上で本ソフトウェアを起動

```shell
python main.py --conf /path/to/main/conf.json
```

または、`main.py`を以下のように編集する
```python
if __name__ == "__main__":
    config = arg_parser("/path/to/main/conf.json")
    beam_template_lst = get_beam_template_from_json(config)
    beam_control_program_lst = get_beam_control_program_from_json(config)
    main(config, beam_template_lst, beam_control_program_lst)
```

いずれかを実行すると、ビームコントロール実行待ち状態に移行する

```shell
Press Enter to start beam control or Ctrl+C to exit...
```

5. CU上で`oaibox_xapp_ue_measurements`起動

6. コントロール実行