"""
Project 3 - Tech Stack Recommender (Content-Based Filtering)
Pipeline: Ingestion -> Scoring (TF-IDF + Cosine) -> Sorting -> Filtering (Top-N)
Pure Python: sirf csv + math use hota hai, koi external library nahi.
"""
import csv
import math
import sys
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "raw_skills.csv"
TOP_N = 3
MIN_INPUTS = 3

ALIASES = {
    "cloud computing": "cloud", "ml": "machine learning", "ai": "machine learning",
    "js": "javascript", "node": "node.js", "nodejs": "node.js",
    "k8s": "kubernetes", "cicd": "ci/cd", "api": "apis", "dsa": "data structures",
    "algorithms": "data structures", "frontend development": "web design",
    "scikit learn": "scikit-learn", "powerbi": "power bi",
}


def normalize(skill):
    s = skill.strip().lower()
    return ALIASES.get(s, s)


# ---------- Data loading ----------
def load_roles(path=DATA_FILE):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}\nPlease keep raw_skills.csv in the same folder as task3.py")

    roles = {}
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if not row or None in row:
                continue
            role = (row.get("role") or "").strip()
            skills = (row.get("skills") or "").strip()
            if role and skills:
                roles[role] = [normalize(s) for s in skills.split(";")]
    return roles


# ---------- TF-IDF ----------
def compute_idf(docs):
    """IDF = log(Total Documents / Documents with term t)"""
    n = len(docs)
    df = Counter()
    for terms in docs.values():
        df.update(set(terms))
    return {t: math.log(n / c) for t, c in df.items()}


def tfidf_vector(terms, idf):
    """TF = count(t in d) / total terms in d ; weight = TF * IDF"""
    if not terms:
        return {}
    counts = Counter(terms)
    total = len(terms)
    return {t: (c / total) * idf[t] for t, c in counts.items() if t in idf}


# ---------- Cosine Similarity ----------
def cosine_similarity(a, b):
    """cos(theta) = (A . B) / (||A|| * ||B||)"""
    dot = sum(a[t] * b.get(t, 0.0) for t in a)
    norm_a = math.sqrt(sum(v * v for v in a.values()))
    norm_b = math.sqrt(sum(v * v for v in b.values()))
    if norm_a == 0 or norm_b == 0:   # zero vector -> division by zero se bachna
        return 0.0
    return dot / (norm_a * norm_b)


# ---------- 4-step pipeline ----------
def recommend(user_skills, roles, top_n=TOP_N):
    # Step 1: Ingestion
    user_terms = [normalize(s) for s in user_skills]
    idf = compute_idf(roles)
    user_vec = tfidf_vector(user_terms, idf)

    # Cold start bypass: user ki skills dataset mein hain hi nahi -> trending fallback
    if not user_vec or all(v == 0 for v in user_vec.values()):
        return None

    # Step 2: Scoring
    scores = []
    for role, skills in roles.items():
        role_vec = tfidf_vector(skills, idf)
        scores.append((role, cosine_similarity(user_vec, role_vec), skills))

    # Step 3: Sorting (descending)
    scores.sort(key=lambda x: x[1], reverse=True)

    # Step 4: Filtering (Top-N)
    return scores[:top_n]


def trending_fallback(roles, top_n=TOP_N):
    """Cold start: global popularity - jo skills sabse zyada roles mein hain."""
    pop = Counter(s for sk in roles.values() for s in set(sk))
    print("\n[Cold Start] Aapki skills dataset se match nahi hui.")
    print("Trending skills abhi:", ", ".join(s for s, _ in pop.most_common(top_n + 2)))


def main():
    try:
        roles = load_roles(DATA_FILE)
    except FileNotFoundError as e:
        print(e)
        print("\nTip: keep raw_skills.csv in the same folder as task3.py and run from that folder.")
        sys.exit(1)

    vocab = sorted({s for sk in roles.values() for s in sk})
    print("=== Tech Stack Recommender ===")
    print("Available skills:", ", ".join(vocab), "\n")

    skills = []
    try:
        while len(skills) < MIN_INPUTS:
            s = input(f"Skill #{len(skills) + 1} enter karein: ").strip()
            if s:
                skills.append(s)
        while True:  # optional extra skills
            s = input("Aur skill? (Enter dabayein agar bas): ").strip()
            if not s:
                break
            skills.append(s)
    except EOFError:
        if not skills:
            print("\nNo input provided. Using default example skills: python, sql, machine learning")
            skills = ["python", "sql", "machine learning"]
        else:
            print("\nInput stopped early. Continuing with entered skills.")

    result = recommend(skills, roles)
    if result is None:
        trending_fallback(roles)
        return

    print(f"\nTop {TOP_N} career paths for {skills}:\n")
    user_set = {normalize(s) for s in skills}
    for rank, (role, score, role_skills) in enumerate(result, 1):
        matched = sorted(user_set & set(role_skills))
        missing = sorted(set(role_skills) - user_set)
        print(f"{rank}. {role}  -  {score * 100:.1f}% match")
        print(f"   Matched: {', '.join(matched) or '-'}")
        print(f"   Seekhna baaki: {', '.join(missing)}\n")


if __name__ == "__main__":
    main()