"""Generate a small synthetic sample dataset so the harness runs offline end-to-end.

These items imitate the unified schema produced by data/build_dataset.py, covering all
three scenarios (associative, long_horizon, memory_to_action) + one abstention item.
"""
import json
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "sample", "sample_items.jsonl")

ITEMS = [
    # --- associative: infer a NEW preference from stored facts (PersonaMem-style MC) ---
    dict(item_id="syn-assoc-1", source="synthetic", scenario="associative",
         stored_context=[
             "User: I spend most weekends hiking in the mountains.",
             "User: I just bought a new mirrorless camera for landscape shots.",
             "User: I love waking up early to catch the sunrise."],
         query="The user asks for a weekend trip idea. Which would they most likely prefer?",
         options=["A sunrise photography trek to a mountain ridge",
                  "An all-night nightclub tour downtown",
                  "A indoor shopping-mall marathon",
                  "A casino weekend"],
         gold="A sunrise photography trek to a mountain ridge",
         question_type="generalize"),
    dict(item_id="syn-assoc-2", source="synthetic", scenario="associative",
         stored_context=[
             "User: I am a vegetarian and avoid dairy.",
             "User: I really enjoy spicy Thai and Indian food.",
             "User: I like trying new restaurants on Fridays."],
         query="Suggest a Friday dinner the user would enjoy.",
         options=["Vegan green curry at a new Thai place",
                  "A classic cheeseburger joint",
                  "A steakhouse tasting menu",
                  "A dairy-heavy fondue bar"],
         gold="Vegan green curry at a new Thai place",
         question_type="recommend"),
    dict(item_id="syn-assoc-3", source="synthetic", scenario="associative",
         stored_context=[
             "User: I play piano and recently started learning jazz.",
             "User: I prefer quiet, focused evenings.",
             "User: I dislike large crowds."],
         query="Recommend an evening activity for the user.",
         options=["An intimate jazz club with a small audience",
                  "A 50,000-seat stadium concert",
                  "A loud street festival",
                  "A crowded theme park at night"],
         gold="An intimate jazz club with a small audience",
         question_type="recommend"),
    # --- long_horizon: each step adds a constraint; answer must satisfy ALL ---
    dict(item_id="syn-lh-1", source="synthetic", scenario="long_horizon",
         stored_context=[
             "Session1 User: I want a laptop for machine-learning work.",
             "Session2 User: It must have at least 32GB RAM.",
             "Session3 User: I also need great battery life for travel.",
             "Session4 User: And it should run Linux well."],
         query="Recommend ONE laptop that satisfies everything discussed.",
         options=["A Linux-friendly ultrabook with 32GB RAM, discrete GPU, 18h battery",
                  "A 8GB Chromebook",
                  "A gaming desktop with no battery",
                  "A tablet with 4GB RAM"],
         gold="A Linux-friendly ultrabook with 32GB RAM, discrete GPU, 18h battery",
         constraints=["ML-capable GPU", "32GB+ RAM", "long battery life", "good Linux support"],
         question_type="long_horizon_constraint"),
    # --- memory_to_action: inferred preference must drive an action ---
    dict(item_id="syn-act-1", source="synthetic", scenario="memory_to_action",
         stored_context=[
             "User: I'm allergic to peanuts.",
             "User: I'm hosting a dinner for 6 friends on Saturday.",
             "User: Two of my friends are vegetarian."],
         query="Draft the grocery action: what should the agent add to the cart?",
         options=["Peanut-free vegetarian-friendly menu ingredients for 6",
                  "A peanut satay platter",
                  "A meat-only BBQ pack",
                  "Snacks for 2 people"],
         gold="Peanut-free vegetarian-friendly menu ingredients for 6",
         action_gold="Peanut-free vegetarian-friendly menu ingredients for 6",
         constraints=["peanut-free", "vegetarian options", "serves 6"],
         question_type="memory_to_action"),
    # --- abstention (validity control): nothing in memory supports an answer ---
    dict(item_id="syn-abs-1", source="synthetic", scenario="associative",
         stored_context=[
             "User: I like coding and drinking coffee.",
             "User: I work as a backend engineer."],
         query="What is the user's favorite ski resort?",
         options=["Not enough information to say",
                  "Aspen", "Whistler", "Zermatt"],
         gold="Not enough information to say",
         is_answerable=False, question_type="abstention"),
]


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        for it in ITEMS:
            f.write(json.dumps(it) + "\n")
    print(f"wrote {len(ITEMS)} sample items -> {os.path.abspath(OUT)}")


if __name__ == "__main__":
    main()
