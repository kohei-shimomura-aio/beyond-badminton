# Beyond Badminton — シンギュラリティ後のスポーツ創発

> *人工生命は、自分たちでスポーツと物語を作れるか？*

20 体の LLM エージェント（多様なペルソナ付き）を 2D 仮想空間に配置し、
**既存スポーツの再構築** と **名前なき空間での新しい遊び発明** を比較した実証実験。

**Team**: Singu-Sport Lab（シンギュスポーツラボ）
**Submitters**: 下村航平 ・ TaE
**Hackathon**: LLMエージェントハッカソン・アイデアソン 2026

---

## 📋 主要発見

| 観察軸 | Pattern 6（バドミントン） | Pattern 7（名前なき月面） |
|---|---|---|
| 既知文脈 | あり | なし（語彙削除） |
| 主な活動 | マッチ・ドリル・コーチング | 独自の動き発明（"Punctuation Pass" 等） |
| 役割分化 | プレーヤー / 観戦者 / 応援者 | 多様な実験者・観察者 |
| 議論量 | 5,442 メッセージ | **19,183 メッセージ（3.5×）** |
| ファン文化 | cheer 1,138 件 | 別形態（rhythm 10,371 件） |

**核心：LLM は既知の文脈を与えると既存スポーツを再構築し、
未知の空間を与えると新しい遊びを発明する。**

---

## 📁 ディレクトリ構造

```
beyond-badminton/
├── simulation/        # 拡張シミュレーションコード
│   ├── agent.py             # ペルソナ・world_description 対応
│   ├── simulation.py        # アナウンス・キャパ制限
│   ├── visualization.py     # 矩形コート・実寸比対応
│   ├── ollama_client.py     # think:false / num_ctx / num_gpu
│   ├── config.yaml          # Pattern 7（月面・名前なき）
│   ├── config_pattern6.yaml # Pattern 6（バドミントン・ペルソナ）
│   └── visualization/viewer.html  # HTML ビューワー
├── submission/        # 提出資料
│   ├── *.pdf
│   ├── *.html
│   ├── figures/             # 図表 PNG
│   └── generate_figures.py  # 図表生成スクリプト
├── samples/           # 各パターンの軽量サンプル
│   ├── pattern_5/    # 既存スポーツ再構築
│   ├── pattern_6/    # ペルソナ群像劇 + ファン文化
│   └── pattern_7/    # 月面・新発明
└── docs/              # 補足ドキュメント
```

---

## 🚀 再現方法

### 必要なもの
- Python 3.10+
- [Ollama](https://ollama.ai/) インストール済み
- gemma4:e4b モデル（`ollama pull gemma4:e4b`）
- Windows / macOS / Linux

### セットアップ
```bash
cd simulation
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

### Pattern 7（月面・名前なき）を実行
```bash
ollama serve  # 別ターミナル
python main.py --config config.yaml --save-frames
```

### Pattern 6（バドミントン・ペルソナ）を実行
```bash
python main.py --config config_pattern6.yaml --save-frames
```

### ビューワーで結果を見る
1. `simulation/visualization/viewer.html` をブラウザで開く（Chrome/Edge推奨）
2. 「ディレクトリを選択」で `output/` を選ぶ
3. ▶ で再生

---

## 🔬 実験デザイン

### 共通設定
- **モデル**: gemma4:e4b（Effective 4B params, "thinking" mode OFF）
- **エージェント数**: 20（男女 10:10 強制）
- **言語**: 英語（推論精度を優先）
- **通信半径**: 4
- **コート capacity**: 6
- **実行時間**: 100 ステップ ≈ 9〜14 時間

### 7 パターンの比較

| # | 設定 | 主な発見 |
|---|---|---|
| 1 | qwen2.5/JP, hazards | 哲学的議論への暴走 |
| 2 | e2b/JP, radius 2 | 通信遮断 → 静止化 |
| 3 | e2b/JP, intervention | ルール議論が発生 |
| 4 | e2b/JP, no hazards, 1 room/2 courts | 「ウォームアップ」無限ループ |
| 5 | e4b/EN, real rectangular courts | Agent 13 がコーチ役へ自発進化 |
| 6 | e4b/EN, 20 personas, PA | ファン文化爆発（cheer 1,138 件）|
| 7 | e4b/EN, lunar / nameless | "Punctuation Pass" など新発明 |

---

## 🌟 Pattern 7 で AI が発明した活動概念

| 概念 | 出現数 | 性質 |
|---|---|---|
| Punctuation Pass | 413 | 新しいゲーム |
| Pass-Circle-Pass | 309 | 循環的なパスゲーム |
| Silent Transfer | 196 | 静かな受け渡し |
| Shape-Pass | 168 | 形を作るパス |
| Light-Led | 150 | 光によるリード |
| **Language of movement** | 16 | **メタ認知** |

> *"It sounds like we're building a whole language of movement in this room."*
> — Agent 19 (Casual / "first encounter, no agenda" persona), Step 65

---

## 📄 詳細

完全な研究内容・図表は [`submission/SinguSportLab_BeyondBadminton_説明資料.pdf`](submission/SinguSportLab_BeyondBadminton_説明資料.pdf) を参照。

---

## 🙏 謝辞

本研究の基盤シミュレーション枠組みは、**本ハッカソンの参加者向けに
兵頭龍樹氏から提供された LLM マルチエージェント 2D シミュレーション
プロジェクト**（`2d-multi-places-simulation-on-fire`）を出発点とし、
本研究では以下を拡張した：
- ペルソナシステム（個別キャラ付け）
- 矩形コート（実寸比 2.33:1）対応
- アナウンス（PA システム）機能
- `world_description` によるシナリオ上書き
- キャパシティ強制
- バドミントンコートマーキング描画

兵頭氏が共有してくださった基盤プロジェクトに深く感謝いたします。

LLM 実行環境として、[Ollama](https://ollama.ai/) と
[Google Gemma 4](https://deepmind.google/models/gemma/gemma-4/) (e4b) を使用。

---

## 📜 ライセンス

GNU General Public License v3.0（ベースプロジェクトを継承）。

詳細は [LICENSE](LICENSE) を参照。
