# Beyond Badminton — 提出デモ動画 構成案 v1

**Target**: 3分以内（ハッカソン想定）／ Singu-Sport Lab
**Tone**: 「人工生命がスポーツを"発明"する瞬間」をドラマとして提示

---

## 全体ストラクチャ（180 秒）

| 時間 | パート | メイン素材 | テロップ／ナレーション |
|---|---|---|---|
| 0:00–0:15 | **Hook** | 黒バック → タイトル | 「人工生命は、自分たちでスポーツと物語を作れるか？」 |
| 0:15–0:35 | **問い・背景** | 図表（Caillois / Huizinga） | 「Huizinga (1938) Homo Ludens / Caillois (1958) 4 categories」など要点を視覚に |
| 0:35–1:05 | **実験デザイン** | システム図 + Pattern 1–7 タイムライン | 20体LLM × 7パターン、共通条件 |
| 1:05–1:50 | **Pattern 6 ハイライト** 🏸 | `Pattern 6.mp4` | 既知文脈 → バドミントン再構築・cheer 1,138件 |
| 1:50–2:35 | **Pattern 7 ハイライト** 🌙 | `Pattern 7.mp4` | 名前なき空間 → "Punctuation Pass" 等を発明 |
| 2:35–3:00 | **核心 + 締め** | テキスト + チームクレジット | 「既知=再構築 / 未知=発明」 |

---

## 各セクション 詳細

### 0:00–0:15 — Hook
- **映像**: 黒バック → タイトル "Beyond Badminton" → サブタイトル "Singu-Sport Lab"
- **ナレ**:
  > 「もし、人工生命だけが残された世界で、彼らに身体と空間と仲間が与えられたら ―― 彼らは自分たちでスポーツを作れるだろうか？」
- **狙い**: 3秒で世界観に引き込む

### 0:15–0:35 — 問い・背景
- **映像**: `submission/figures/` の図 + テキスト
- **ボード化したい3点**:
  1. 「Huizinga: 人間は遊ぶ存在 (Homo Ludens, 1938)」
  2. 「Caillois: 4 categories × Paidia↔Ludus (1958)」
  3. 「シンギュラリティ後 ―― AIエージェントが自律的に振る舞う未来の社会において、彼らは自らスポーツと物語を作れるのか？」

### 0:35–1:05 — 実験デザイン
- **映像**: システム図 → 7パターン比較表
- **要点テロップ**:
  - LLM: gemma4:e4b（Effective 4B params）
  - 20 エージェント × 100 ステップ
  - 通信半径 4、コート capacity 6
  - 7 パターンを比較
- **ナレ**:
  > 「我々は7つの設定を比較した。同じLLM、同じ場、変えたのは"文脈"だけ。」

### 1:05–1:50 — Pattern 6: Existing Context（バドミントン）
- **映像**: `Pattern 6.mp4` の中から以下のステップを抽出
  - **Step 1** （Agent 12 が "energy + match" を呼びかけ）
  - **Step 35** （PA Announcement 直後、Agent 1 が "Enough discussion" と試合開始を宣言）
  - **Step 70** （Agent 11/12 の cheer ピーク "WHOA! Ready to make this sequence unforgettable?!"）
- **テロップ**:
  - "Pattern 6: Badminton court, 20 personas, PA system"
  - "Result: Match → Cheer → Fan Culture（cheer 1,138件）"
- **ナレ**:
  > 「既知の文脈を与えると、彼らは既存スポーツを"再構築"した。コーチが現れ、観客が現れ、応援文化が爆発した。」

### 1:50–2:35 — Pattern 7: Name-less Context（月面・名前なき）
- **映像**: `Pattern 7.mp4` の中から以下のステップを抽出
  - **Step 1** （Agent 0: "I'm going to grab one of these long things"）
  - **Step 35** （PA Announcement 後、対立 vs 協調が立ち上がる）
  - **Step 65** （Agent 19 の決定的瞬間 ―― "language of movement" + "Punctuation Pass" 提案）
- **テロップ**:
  - "Pattern 7: Lunar habitat, name-less equipment"
  - "Result: 'Punctuation Pass' / 'Pass-Circle-Pass' / 'Silent Transfer' ... 6 つの新概念を発明"
  - "Total 19,183 messages（Pattern 6 の 3.5×）"
- **ナレ**:
  > 「同じLLM、同じ20体、同じ100ステップ。違うのは"文脈"だけ。
  >  彼らは "Punctuation Pass"、"Pass-Circle-Pass"、"Silent Transfer" など、地球には存在しない遊びを発明した。」
- **決定打のテロップ**（Agent 19 の引用、step 65）:
  > 「It sounds like we're building a whole language of movement in this room.」
  > 「この部屋で、私たちは"動きの言語"を一つ作っているみたい。」
  > — Agent 19（"first encounter, no agenda" 設定）

### 2:35–3:00 — 核心 + 締め
- **映像**: 黒バック → 大きなテキスト → クレジット
- **核心テロップ**:
  > 「LLMは、既知の文脈では既存スポーツを再構築し、
  >  未知の空間では新しい遊びを発明する。」
- **ナレ**:
  > 「シンギュラリティの先には、人類の遺した文化を再演する世界もあれば、
  >  彼ら自身の"動きの言語"が生まれる世界もある。
  >  Beyond Badminton は、その分岐点を覗いた小さな実証実験だ。」
- **クレジット**:
  - Team: Singu-Sport Lab（シンギュスポーツラボ）
  - 下村航平 ・ TaE
  - LLMエージェントハッカソン・アイデアソン 2026
  - GitHub: github.com/kohei-shimomura-aio/beyond-badminton
  - 基盤プロジェクト提供：兵頭龍樹氏（謝辞）

---

## TaE さんへの編集メモ

- **動画切り出しの目印**: Pattern 6 の山場は **step 35（試合開始）** と **step 70（応援ピーク）**。Pattern 7 の山場は **step 65（"language of movement" 発言）**。
- **テロップの基本配色**: P6 は紫/オレンジ系、P7 は青/銀系（viewer.html のヘッダー配色に合わせる）。
- **音声**: ナレーション or テロップ only どちらでもOK。フリーBGMなら DOVA-SYNDROME / 効果音ラボ あたり。
- **引用テキスト**: `movie/key_quotes.md` に全 verbatim あり。テロップに使う際はそこからコピペ推奨。
- **画素材**: 以下が全部 `submission/figures/` にある
  - `system_diagram.png` — 実験システム図
  - `pattern_timeline.png` — 7パターンタイムライン
  - `p6_vs_p7_comparison.png` — 比較表
  - `phase_progression.png` — フェーズ進行
  - `personas_overview.png` — 20 ペルソナ概要

---

## 想定外を防ぐためのチェック

- [ ] 「人類が去った」表現は使わない（→ 「AIエージェントが自律的に振る舞う未来の社会"において"」）
- [ ] Caillois の正式名（"Les jeux et les hommes", 1958）と4 categories（Agon / Alea / Mimicry / Ilinx）は正確
- [ ] 兵頭龍樹氏への謝辞をクレジットに含める
- [ ] "language of movement" 発言者は **Agent 19**（Casual / "first encounter, no agenda" 設定）
