---
title: How to write def_beam_table_file.yml
author: Masaya Sakamoto
date: 2025-08-21
language: Japanese
---

# `def_beam_table_file.yml`の表記法

## 概要
`def_beam_table_file.yml`は、ビームテーブルを単純なYAML形式で記述するためのファイルです。いくつかのプリセットと、設定情報からビームテーブルを作成します。

## 構成

### 線形ビームテーブル

```yaml
beams:
    origin:
    dB: 0
    theta: 0
    phi: 0

    # originを除いて、名称の昇順に実行される
    lin_1:
        type: linear
        amp: const   # 電波強度の増減 -- const以外は未実装
        config:
            dB: 0
            theta_start_d: 1
            theta_end_d: 25
            theta_step_d: 1
            pattern_rotation_d: 0
            pattern_center_d: [0, 0] # 未実装

    lin_2:
        type: linear
        amp: const
        config:
            dB: 0
            theta_start_d: 1
            theta_end_d: 25
            theta_step_d: 1
            pattern_rotation_d: 180
            pattern_center_d: [0, 0] # 未実装
```

### Fibonacciビームテーブル

```yaml
beams:
    fib:
        type: fibonacci
        amp: const
        config:
            dB: 0
            delta: 0.5      # 中心部分のビーム密度緩和 [0, 1)
            beams: 64
            pattern_rotation_d: 0
            pattern_center_d: [0, 0] # 未実装
```

### 円形ビームテーブル

*現在は未実装です*
```yaml
beams:
    origin:
        dB: 0
        theta: 0
        phi: 0
    
    circ_1:
        type: circular
        amp: const
        config:
            dB: 0
            zenith_angle_d: 10
            azimuth_angle_start_d: 0
            azimuth_angle_end_d: 360
            pattern_rotation_d: 0
            pattern_center_d: [0, 0] # 未実装
    circ_2:
        type: circular
        amp: const
        config:
            dB: 0
            zenith_angle_d: 20
            azimuth_angle_start_d: 0
            azimuth_angle_end_d: 360
            pattern_rotation_d: 0
            pattern_center_d: [0, 0] # 未実装
```


