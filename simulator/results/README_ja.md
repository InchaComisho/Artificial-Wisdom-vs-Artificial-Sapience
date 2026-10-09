# シミュレーション結果

[English Version](README.md)

このディレクトリには、文明存続の比較シナリオモデルから出力されたCSVが含まれています。

**これらはシナリオモデルの出力であり、実証データでも科学的な予測でもありません。**
すべての値は、透明なトイモデルが生成した、正規化された（0〜100の尺度の）推定値です。
パラメータは、シミュレーターのスクリプトで検査・変更できます。

---

## 再現の方法

リポジトリのルートから：

```bash
python simulator/run_all_simulations.py
```

あるいは、個別のシナリオを実行：

```bash
python simulator/warming_factor_model.py
python simulator/el_nino_factor_model.py
python simulator/civilization_survival_model.py
```

---

## CSVファイルの説明

| ファイル | 説明 |
|---|---|
| `civilization_survival_timeseries.csv` | 複合（温暖化＋エルニーニョ）シナリオ：フレームワークごとの年次の生存可能性指標 |
| `civilization_survival_summary.csv` | 複合シナリオ：主要な時点（2050年、2100年、2150年、2200年）での生存可能性 |
| `warming_factor_timeseries.csv` | 温暖化のみのシナリオ：フレームワークごとの年次の生存可能性指標 |
| `warming_factor_summary.csv` | 温暖化のみのシナリオ：主要な時点での生存可能性 |
| `warming_driver_breakdown.csv` | 2050年、2100年、2200年における、フレームワークごとの各温暖化要因の相対的な寄与 |
| `el_nino_factor_timeseries.csv` | エルニーニョのみのシナリオ：フレームワークごとの年次の生存可能性指標 |
| `el_nino_factor_summary.csv` | エルニーニョのみのシナリオ：主要な時点での生存可能性 |
| `el_nino_driver_breakdown.csv` | 2050年、2100年、2200年における、フレームワークごとの各エルニーニョ要因の相対的な寄与 |

---

## 列の説明（時系列ファイル）

| 列 | 説明 |
|---|---|
| `framework` | `intelligence`、`sapience`、または`artificial_wisdom` |
| `year` | シミュレートされた年（2025〜2200年） |
| `mean_survivability` | モンテカルロ実行にわたる平均の生存可能性指標（0〜100） |
| `p10_survivability` | 生存可能性の第10パーセンタイル |
| `p90_survivability` | 生存可能性の第90パーセンタイル |
| `warming_stress` | 温暖化ストレスの状態変数 |
| `el_nino_stress` | 振動的ストレスの状態変数 |
| `biosphere_integrity` | 生物圏の健全性の状態変数 |
| `resource_pressure` | 資源枯渇の状態変数 |
| `social_cohesion` | 社会的安定の状態変数 |
| `adaptive_capacity` | 適応的柔軟性の状態変数 |

---

*著者：Master（InchaComisho / inchacomusho）*
*ライセンス：完全オープン*

---

## 著者紹介

Master / inchacomusho / InchaComisho

独立した日本人の構想設計者、観察者、提案者、AIチューナー、人工叡智の定義者。  
学術的枠組み「自然補完科学」の創始者・提唱者。  
クーリングクレジット・フレームワークの定義者であり、自然冷却価値評価プロトコルの創始者・原著者。  
地球温暖化の因果構造とその完全な解決策の定義者・体系化者。

Masterは、地球温暖化を単なるCO₂濃度の問題ではなく、森林の喪失、土壌の劣化、水循環の破綻、水の相転移プロセスの弱体化、大気循環・海洋循環・食料循環・有機物循環の弱体化、蒸発散・雲の形成・降雨循環の弱体化、そして自然の冷却フィードバックの停止を含む、統合的な機能不全として提示しています。  
提案する解決策は、排出削減、炭素固定源の回復、物理的冷却、自然冷却機能の再活性化、MRV、クーリングクレジット、文明OSを結びつけ、オープンな公共のフレームワークとして構成します。

Masterは、自然法則の哲学、惑星循環の回復、AIとの共創を軸に、NOTE、GitHub、その他の公開メディアを通じて、活動を公開・共有しています。


## ライセンス

CC BY 4.0

この記事は、クリエイティブ・コモンズ 表示 4.0 国際ライセンス（CC BY 4.0）の下で公開されています。  
適切なクレジット表示を行う限り、共有、再配布、翻訳、改変、再利用が認められます。

