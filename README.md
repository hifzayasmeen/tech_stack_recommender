
# 🎯 Tech Stack Recommender

> **AI Recommendation Logic: Project 3 | DecodeLabs Industrial Training Kit (Batch 2026)**

A content-based recommendation engine, written in **pure Python** (no ML libraries), that maps a user's skills to the most suitable tech career paths using **TF-IDF weighting** and **Cosine Similarity**.

---

## 📌 Overview

Enter at least three skills (for example `Python`, `Cloud Computing`, `Automation`) and the engine ranks job roles by how closely they match your profile. It then returns the **Top 3** career paths, along with the skills you already match and the skills you still need to learn.

This project shows the core ideas behind real-world recommenders: turning text into vectors, weighting features by importance, and ranking items by similarity.

---

## ✨ Features

- ✅ Takes a minimum of **3 user skills** as input
- ✅ **TF-IDF** weighting: specific skills count for more than generic ones
- ✅ **Cosine Similarity** scoring: compares direction (interest pattern), not vector size
- ✅ **Top-N ranking** to avoid choice overload
- ✅ **Skill alias normalization** (`"Cloud Computing"` → `cloud`, `"k8s"` → `kubernetes`)
- ✅ **Cold-start fallback**: shows trending skills when the input matches nothing in the dataset
- ✅ "Matched" and "Skills to learn" output for each recommendation
- ✅ Zero external dependencies (only `csv`, `math`, `collections`)

---

## 🧠 How It Works

The engine follows the **Input → Process → Output** model, implemented as a 4-step pipeline:

```
 User Skills ──► 1. Ingestion ──► 2. Scoring ──► 3. Sorting ──► 4. Filtering ──► Top 3 Roles
                 (normalize)    (TF-IDF +        (descending)    (Top-N cut)
                                 Cosine)
```

| Step | What happens |
|------|--------------|
| **1. Ingestion** | Collect user skills, then lowercase them and map aliases to a shared vocabulary |
| **2. Scoring** | Convert the user and every job role into TF-IDF vectors, then compute cosine similarity |
| **3. Sorting** | Order all roles by score, highest first |
| **4. Filtering** | Keep only the Top-N (default: 3) results |

### TF-IDF

```
TF  = (count of term t in document d) / (total terms in document d)
IDF = log( total documents / documents containing term t )
Weight = TF × IDF
```

A skill that appears in almost every role (such as `git`) gets a low weight. A rare, descriptive skill (such as `terraform`) gets a high weight.

### Cosine Similarity

```
cos(θ) = (A · B) / (‖A‖ × ‖B‖)
```

- `1` means perfectly aligned.
- `0` means no skills in common.
- Because TF-IDF values are never negative, scores always fall between **0 and 1**, so they read naturally as a percentage match.

### Why Cosine instead of Euclidean distance?

Euclidean distance is sensitive to vector magnitude. A role with a long skill list would look "far" from a short profile, even if both point the same way. Cosine looks only at **orientation**, which makes it the industry standard for text-like data.

---

## 📁 Project Structure

```
task 3/
├── task3.py          # Main recommender script
├── raw_skills.csv    # Dataset: job roles and their required skills
└── README.md         # Project documentation
```

---

## 🚀 Getting Started

### Requirements

- Python **3.8+**
- No `pip install` needed

### Run

```bash
python task3.py
```

### Example session

```
Skill #1 enter karein: Python
Skill #2 enter karein: Cloud Computing
Skill #3 enter karein: Automation
Aur skill? (Enter dabayein agar bas):

Top 3 career paths for ['Python', 'Cloud Computing', 'Automation']:

1. Cloud Architect  -  54.4% match
   Matched: automation, cloud
   Seekhna baaki: aws, azure, kubernetes, networking, security, terraform

2. DevOps Engineer  -  17.1% match
   Matched: automation, python
   Seekhna baaki: aws, ci/cd, docker, git, kubernetes, linux, terraform

3. System Administrator  -  13.8% match
   Matched: automation
   Seekhna baaki: bash, linux, monitoring, networking, security, windows server
```

---

## 🗂️ Dataset Format

`raw_skills.csv` has two columns. Skills are separated by semicolons:

```csv
role,skills
Data Scientist,python;sql;machine learning;statistics;data analysis;pandas
DevOps Engineer,aws;docker;kubernetes;ci/cd;linux;git;automation;terraform;python
Backend Developer,java;python;sql;apis;git;docker;data structures;databases
```

To add a new role, just append a new row. No code changes are needed.

---

## ⚙️ Configuration

You can change these constants at the top of the script:

| Constant | Default | Meaning |
|----------|---------|---------|
| `TOP_N` | `3` | Number of recommendations shown |
| `MIN_INPUTS` | `3` | Minimum skills the user must enter |
| `ALIASES` | dict | Maps alternate skill names to dataset vocabulary |

---

## ❄️ Cold Start Handling

| Problem | Solution used |
|---------|---------------|
| **User cold start**: input skills match nothing, so the vector is all zeros | Division-by-zero guard plus a **trending skills fallback** |
| **Item cold start**: a new role has no history | Not an issue. Content-based filtering recommends new roles immediately from their skill metadata. |

---

## 🔮 Future Improvements

- [ ] Fuzzy matching for typos (`"pyhton"` → `"python"`)
- [ ] Skill ratings (beginner, intermediate, expert) as user-supplied weights
- [ ] Larger dataset (50+ roles) pulled from real job postings
- [ ] Web UI using Flask or Streamlit
- [ ] Comparison against `scikit-learn`'s `TfidfVectorizer` to validate the results
- [ ] Hybrid approach with collaborative filtering

---

## 🛠️ Skills Demonstrated

`Logic Building` · `Pattern Matching` · `Vector Mapping` · `TF-IDF` · `Cosine Similarity` · `Recommendation Systems` · `Python`

---

## 👤 Author

Hifza Yasmeen
AI Engineering Intern @ **DecodeLabs** | Batch 2026


---

<p align="center">Built with ❤️ as part of the DecodeLabs Industrial Training Kit</p>
