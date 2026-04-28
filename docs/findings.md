# Detailed Findings — Beyond Badminton

This document captures the empirical observations from each pattern in detail.

## Pattern 1 — qwen2.5 / Japanese / radius 3 (with hazards)
- 37 steps before being stopped (judged unproductive)
- Conversations drifted into mystical/philosophical territory:
  > "我々は、この静寂の共鳴体である" (We are the resonant body of silence)
- 0 mentions of badminton-specific actions
- Lesson: too-strong communication + abstract LLM = philosophical drift

## Pattern 2 — gemma4:e2b / radius 2 (with hazards)
- Full 120 steps; 0 messages sent
- Agents physically isolated due to small radius
- "指示がないため、現在の位置にとどまる" (No instructions → stay)
- Lesson: communication breakdown leads to passive paralysis

## Pattern 3 — gemma4:e2b / Japanese / intervention prompts
- "Doubles", "rules" emerged in conversations
- Hazard detection observed
- But still mostly drill-talk, limited play
- Lesson: prompt engineering helps but model capability matters

## Pattern 4 — gemma4:e2b / no hazards / 1 room / 2 courts
- 2,619 mentions of "ウォームアップ" — agents stuck in eternal preparation
- 0 actual matches initiated
- Lesson: removing pressure without adding alternative motivation = stagnation

## Pattern 5 — gemma4:e4b / English / real rectangular courts
- match: 567, shuttle: 480, doubles: 272 — sport vocabulary explosion
- **Agent 13's career arc** observed:
  - Step 1: Initiator ("Anyone up for a casual game?")
  - Step 20: Drill designer
  - Step 30: Performer (audience-aware)
  - Step 60: **Coach** ("establish a coaching spot")
  - Step 70: Director ("hype up the final sequence")
- Lesson: with proper LLM and language, individuals develop multi-step roles

## Pattern 6 — gemma4:e4b / English / 20 personas / PA announcements
- **Cheer (応援) explosion**: 1 → 1,138 mentions vs Pattern 5
- match: 1,062, game: 828, drill: 3,288
- Capacity 6 + 20 agents = forced spectator role for 14 agents
- Lesson: persona diversity + capacity constraint + announcements = fan culture

## Pattern 7 — gemma4:e4b / English / lunar / name-less equipment
- All badminton terms (court, racket, shuttle, doubles, singles) = 0 mentions
- **Invented activities**:
  - "Punctuation Pass": 413 mentions
  - "Pass-Circle-Pass": 309
  - "Silent Transfer": 196
  - "Shape-Pass": 168
  - "Light-Led": 150
- Total messages: 19,183 (3.5× Pattern 6)
- "Language of movement" — explicit meta-cognition
- Lesson: removing existing labels lets LLMs construct novel activity vocabularies

---

## Cross-Pattern Comparison

| Metric | P5 | P6 | P7 |
|---|---|---|---|
| Total messages | 4,978 | 5,442 | **19,183** |
| cheer mentions | 1 | **1,138** | 357 |
| rule mentions | 22 | 233 | **2,536** |
| rhythm mentions | (low) | 899 | **10,371** |
| Court occupancy peak | ~6 | ~5 | ~6 (briefly) |
| Court usage style | Active matches | Active w/ rotation | Brief, then external |
| Activity vocabulary | Existing badminton | Existing badminton | Newly invented |

## Key Takeaways

1. **LLMs reconstruct known sports when given familiar context** — they do not "invent from zero" with familiar labels.
2. **LLMs invent new activity vocabularies when given unfamiliar context** — they construct novel "languages of movement" when existing terms are absent.
3. **Persona diversity drives role differentiation** — homogeneous agent groups produce homogeneous behavior; diverse personas produce ensemble drama.
4. **Physical constraints (capacity) force role specialization** — when not everyone can play, observers and supporters emerge organically.
5. **Announcements (event injection) amplify focus** — a simple "PA system" message can shift the dominant activity mode within 5–10 steps.
