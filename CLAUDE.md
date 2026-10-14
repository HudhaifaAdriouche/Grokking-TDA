# Phase 2 — Build It: Session Checklist

Each session is about 2–3 hours. Do them in order, and only move on once every **Done when** box is ticked.

---

## Every session: routine

**Start (5 min)**
- [ ] Open `Grokking-TDA` in VS Code and activate the virtual environment.
- [ ] Run `git pull` (harmless habit; matters if you ever work from two machines).
- [ ] Reread yesterday's LOG.md entry.

**End (10 min)**
- [ ] Write today's LOG.md entry. It has three parts: *what I did / what happened / what confused me*.
- [ ] Run `git add .`, then `git commit -m "<what you did>"`, then `git push`.
- [ ] Note the first task for next session at the bottom of the log entry.

---

## Session 1 — Dataset (`src/data.py`)

**Goal:** all (a, b) pairs, a train/test split, and correct labels.

- [ ] Build all pairs for a, b ∈ {0, …, 112}, which gives 12,769 examples.
- [ ] Turn each input into tokens `[a, b, =]`, where `=` has id 113 (vocabulary size 114).
- [ ] Set the label to (a + b) mod 113.
- [ ] Shuffle with a **fixed seed** and keep 30% for training.
- [ ] Write `assert` checks for three things: the train size, no overlap between train and test, and correct labels on random examples.

**Done when**
- [ ] All asserts pass.
- [ ] You can state how many training examples there are without looking.

**Commit:** `add dataset and train/test split with checks`

---

## Session 2 — Model, part 1 (`src/model.py`)

**Goal:** embeddings and attention, with every shape checked.

- [ ] Reread the attention pseudocode in Phuong & Hutter.
- [ ] Add the token embedding `W_E` (114 × 128) and the positional embedding (3 × 128).
- [ ] Write attention with 4 heads (d_head = 32) and a causal mask.
- [ ] Shape test: pass a batch of 5 examples through and print or assert the shape of each intermediate tensor.

**Done when**
- [ ] You can explain every tensor shape on paper.

**Commit:** `add embeddings and attention`

---

## Session 3 — Model, part 2

**Goal:** the full forward pass works and the model can learn.

- [ ] Add the MLP (128 → 512 → 128, ReLU) with residual connections. **No LayerNorm.**
- [ ] Add the unembedding `W_U`, which produces 113 logits.
- [ ] Take the logits **at the last position only**.
- [ ] Tiny overfit test: train on 20 examples. The model should reach 100% on them within a few hundred steps.

**Done when**
- [ ] The tiny overfit test passes.

**Send to Claude for review:** `data.py`, `model.py`, and the shape-test output.

**Commit:** `complete one-layer transformer + overfit test`

---

## Session 4 — Training loop (`src/train.py`)

**Goal:** a full-batch AdamW training loop with logging.

- [ ] Use full-batch training: every step uses the whole training set.
- [ ] Set up AdamW with lr 1e-3, weight decay 1.0, and betas (0.9, 0.98).
- [ ] Use cross-entropy loss on the last-position logits.
- [ ] Every 10 epochs, log train and test loss and accuracy **to a file** (CSV or JSON), not just the screen.
- [ ] Do a short trial run of about 1,000 epochs. Train accuracy should climb.

**Done when**
- [ ] The trial run works and the log file is readable.

**Commit:** `add training loop with logging`

---

## Session 5 — Snapshots and config

**Goal:** saved checkpoints, configurable runs, and a full run launched.

- [ ] Save the weights every 100 epochs to `runs/<run_name>/`.
- [ ] Save the run's config (seed, weight decay, train fraction, …) next to the checkpoints.
- [ ] Make these settable from the command line: `seed`, `weight_decay`, `train_frac`, `shuffle_labels`.
- [ ] Check that `runs/` and `*.pt` are in `.gitignore`.
- [ ] Launch the full run of about 40,000 epochs.

**Done when**
- [ ] Checkpoints appear on disk.
- [ ] A different setting runs with one command and no code edit.

**Commit:** `add checkpointing and run config`

---

## Session 6 — Milestone: reproduce grokking

**Goal:** your own version of Power et al.'s Figures 1 and 4.

- [ ] In a notebook, plot train and test accuracy against epoch with a **log-scale x-axis**.
- [ ] Plot train and test loss the same way.
- [ ] Mark roughly where memorization happens and where test accuracy jumps.
- [ ] If there's no grokking, check weight decay, train fraction, and the loss position. Write down what you tried.
- [ ] Record any oddities, such as loss spikes, in LOG.md.

**Done when**
- [ ] The plot shows test accuracy jumping well after train accuracy reaches ~100%.

**Send to Claude for review:** the plots and the run config.

**Commit:** `reproduce grokking + plots`

---

## Session 7 — TDA pipeline, part 1 (`src/tda.py`)

**Goal:** a persistence function, tested on circles.

- [ ] Write a function that takes a point cloud and returns persistence diagrams (H0, H1) using ripser.
- [ ] Add summaries: the length of the longest H1 bar, and the gap between the longest and second-longest bars.
- [ ] Test on a circle in ℝ². You should get one long H1 bar.
- [ ] Test on a circle embedded in ℝ¹²⁸ with noise. Increase the noise until the bar disappears and record that level. This is exercise 3.
- [ ] Scale test: multiply a circle by 0.1 and see what happens to the persistence values.

**Done when**
- [ ] Every circle test behaves as you predicted, or you can explain why it doesn't.

**Commit:** `add TDA pipeline + circle tests`

---

## Session 8 — TDA pipeline, part 2 and design decisions

**Goal:** harder synthetic tests and your written design choices.

- [ ] Fourier curve from exercise 2: a ↦ (cos ω₁a, sin ω₁a, …, cos ωₘa, sin ωₘa), sampled at 113 points.
- [ ] Torus, (cos θ, sin θ, cos φ, sin φ). You should get two long H1 bars and one long H2 bar.
- [ ] Random Gaussian cloud. You should get only short bars.
- [ ] Write a short answer in LOG.md to each design question:
  - [ ] **Norm shrinkage:** how to make persistence comparable across epochs.
  - [ ] **Distance:** Euclidean or cosine, and why.
  - [ ] **Point cloud:** embeddings or activations, and which one the hypothesis is about.

**Done when**
- [ ] All synthetic tests pass.
- [ ] All three design questions have a written position.

**Send to Claude for review:** the test results and your design answers.

**Commit:** `synthetic TDA tests + design decisions`

---

## Session 9 — First look and Phase 2 wrap-up

**Goal:** connect the pipeline end to end.

- [ ] Load `W_E` rows 0–112 from every checkpoint.
- [ ] Run the TDA pipeline on each, using your chosen normalization and distance.
- [ ] Plot max H1 persistence over epochs next to test accuracy.
- [ ] Write in LOG.md what you see, **without over-interpreting**; validation comes in Phase 3.
- [ ] Update the README with a short "Phase 2 status" section.

**Done when**
- [ ] One figure shows topology and accuracy on the same time axis.

**Send to Claude for review:** the figure. We then plan Phase 3 together.

**Commit:** `first look: H1 persistence of W_E over training`

---

## Libraries for this phase

`torch`, `numpy`, `matplotlib`, `ripser`, `persim`, `tqdm`, `jupyter`. Keep them listed in `requirements.txt`.
