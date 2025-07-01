# nie_faq_chatbot.py

# 1. FAQs dictionary
from difflib import get_close_matches
faqs = {
    "when was nie mysuru established": "NIE was established in 1946.",
    "is nie affiliated": "Yes, NIE is autonomous under VTU and accredited by AICTE, NAAC, and NBA Tier‑1.",
    "what courses are offered": "NIE offers B.E./B.Tech in CSE, ISE, ECE, ME, etc. PG includes M.Tech, MCA, and PhD.",
    "how do i get admission": "UG via KCET/COMEDK, PG via PGCET/GATE or management quota.",
    "what is the annual fee": "The annual fee is approximately ₹58,200 for B.E. (excluding hostel and mess).",
    "how are placements": "In 2022–23, 708 students were placed with offers up to ₹56 LPA. CSE/ISE have strong placement rates.",
    "are there two campuses": "Yes, South Campus (main) and North Campus (IT branches like CSE, ISE, MCA).",
    "how is the hostel": "South hostels are good. North hostels get filled quickly. Many students stay in PGs near the campus.",
    "what is student life like": "Active in sports, clubs, and fests. Coding culture strong in CSE/ISE branches.",
    "how is the crowd": "Generally friendly. Some language barrier for outsiders, but overall inclusive."
}
def find_best_match(user_input, questions):
    matches = get_close_matches(user_input, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None
# 2. Simple chatbot function
def chatbot():
    print("📘 NIE Mysuru FAQ Chatbot (type 'exit' to quit)")

    while True:
        user_input = input("\nYou: ").strip().lower()

        if user_input == 'exit':
            print("👋 Goodbye!")
            break

        best_match = find_best_match(user_input, faqs.keys())

        if best_match:
            print(f"Bot: {faqs[best_match]}")
        else:
            print("Bot: Sorry, I don't have an answer for that yet.")
# 3. Run the chatbot
if __name__ == "__main__":
    chatbot()
