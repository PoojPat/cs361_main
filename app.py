from flask import Flask, render_template, request, redirect, url_for
import requests
from datetime import datetime

app = Flask(__name__)

# Fake data for testing
fake_decks = [
    {"id": 1, "name": "Biology", "new": 5, "learn": 0, "due": 0},
    {"id": 2, "name": "Chemistry", "new": 3, "learn": 2, "due": 1},
]

# Fake data for flashcards
fake_flashcards = [
    {
        "id": 1,
        "deck_id": 1,
        "front": "What is the powerhouse of the cell?",
        "back": "Mitochondria",
        "extra": "- Produces most of the cell's energy (ATP)\n- Have their own DNA"

    }
]


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # # Call User Authentication Microservice here
        # response = requests.post(
        #     "http://localhost:5001/login",  # Replace with your microservice URL
        #     json={"username": username, "password": password}
        # )
        # if response.status_code == 200:
        #     return redirect(url_for("decks"))
        # else:
        #     return "Login failed. Please try again."

        # Fake login logic for now (accept any username/password)
        return redirect(url_for("decks"))

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Call User Authentication Microservice to register the user
        response = requests.post(
            "http://localhost:5001/register",  # Replace with your microservice URL
            json={"username": username, "password": password}
        )
        if response.status_code == 200:
            return redirect(url_for("login"))
        else:
            return "Sign up failed. Please try again."
    return render_template("signup.html")


@app.route("/decks")
def decks():

    # # Fetch decks from the Deck Management Microservice
    # response = requests.get("http://localhost:5002/decks")  # Replace with microservice URL
    # decks = response.json() if response.status_code == 200 else []

    return render_template("decks.html", decks=fake_decks)


@app.route("/delete_deck/<deck_id>", methods=["POST"])
def delete_deck(deck_id):

    # # Call Deck Management Microservice to delete the deck
    # response = requests.delete(f"http://localhost:5002/decks/{deck_id}")
    # if response.status_code == 200:
    #     return redirect(url_for("decks"))
    # else:
    #     return "Failed to delete deck. Please try again."

    # Fake delete logic
    global fake_decks
    print(f"Deleting deck with ID: {deck_id}")  # Debugging
    fake_decks = [deck for deck in fake_decks if int(deck["id"]) != int(deck_id)]
    print(f"Updated decks: {fake_decks}")  # Debugging
    return redirect(url_for("decks"))


@app.route("/create_deck", methods=["GET", "POST"])
def create_deck():
    if request.method == "POST":
        deck_name = request.form["deck_name"]

        # # Call Deck Management Microservice to create a new deck
        # response = requests.post(
        #     "http://localhost:5002/decks",  # Replace with your microservice URL
        #     json={"name": deck_name}
        # )
        # if response.status_code == 200:
        #     return redirect(url_for("decks"))
        # else:
        #     return "Failed to create deck. Please try again."

        # Check if we're editing an existing deck
        deck_id = request.form.get("deck_id")
        if deck_id:
            deck_id = int(deck_id)
            for deck in fake_decks:
                if deck["id"] == deck_id:
                    deck["name"] == deck_name
                    break
        else:
            # Fake Create logic
            new_deck = {
                "id": len(fake_decks) + 1,
                "name": deck_name,
                "new": 0,
                "learn": 0,
                "due": 0,
            }
            fake_decks.append(new_deck)
        return redirect(url_for("decks"))
    # If editing, pass the deck name and ID to the template
    deck_name = request.args.get("deck_name", "")
    deck_id = request.args.get("deck_id", "")
    return render_template("create_deck.html", deck_name=deck_name, deck_id=deck_id)


@app.route("/edit_deck/<int:deck_id>", methods=["GET", "POST"])
def edit_deck(deck_id):
    if request.method == "POST":
        deck_name = request.form["deck_name"]
        # Update the deck name in the fake data
        for deck in fake_decks:
            if deck["id"] == deck_id:
                deck["name"] = deck_name
                break
        return redirect(url_for("decks"))
    # Pre-fill the form with the current deck name
    deck_to_edit = next((deck for deck in fake_decks if deck["id"] == deck_id), None)
    if deck_to_edit:
        return render_template("create_deck.html", deck_name=deck_to_edit["name"])
    else:
        return "Deck not found.", 404


@app.route("/add_flashcards", methods=["GET", "POST"])
def add_flashcards():
    if request.method == "POST":
        deck_id = int(request.form["deck_id"])
        front = request.form["front"]
        back = request.form["back"]
        extra = request.form.get("extra", "")  # Optional field

        # Add the flashcard to the fake data
        new_flashcard = {
            "id": len(fake_flashcards) + 1,
            "deck_id": deck_id,
            "front": front,
            "back": back,
            "extra": extra,
        }
        fake_flashcards.append(new_flashcard)
        return redirect(url_for("decks"))
    return render_template("add_flashcards.html", decks=fake_decks)


@app.route("/review_preview/<int:deck_id>")
def review_preview(deck_id):
    # Fetch the selected deck from fake data
    deck = next((deck for deck in fake_decks if deck["id"] == deck_id), None)
    if not deck:
        return "Deck not found.", 404
    return render_template("review_preview.html", deck=deck)


# @app.route("/review_flashcards/<int:deck_id>")
# def review_flashcards(deck_id):
#     # Filter flashcards for the selected deck
#     deck_flashcards = [card for card in fake_flashcards if card["deck_id"] == deck_id]
#     return render_template("review_flashcards.html", deck_id=deck_id, flashcards=deck_flashcards)


@app.route("/review_flashcards/<int:deck_id>")
def review_flashcards(deck_id):
    # Filter flashcards for the selected deck
    deck_flashcards = [card for card in fake_flashcards if card["deck_id"] == deck_id]
    # if not deck_flashcards:
    #     return "No flashcards to review in this deck.", 404
    # Get the current flashcard index from the query parameter
    current_index = int(request.args.get("current_index", 0))
    return render_template("review_flashcards.html", deck_id=deck_id, flashcards=deck_flashcards, current_index=current_index)


@app.route("/rate_flashcard/<int:flashcard_id>", methods=["POST"])
def rate_flashcard(flashcard_id):
    rating = request.form["rating"]  # "again", "hard", "good", or "easy"
    # Update the flashcard's review status based on the rating (fake logic for now)
    for card in fake_flashcards:
        if card["id"] == flashcard_id:
            # Simulate spaced repetition logic (e.g., update review intervals)
            card["last_reviewed"] = datetime.utcnow()
            card["interval"] = calculate_interval(card.get("interval", 1), rating)
            break
    return redirect(url_for("review_flashcards", deck_id=request.form["deck_id"]))


def calculate_interval(current_interval, rating):
    # Simple spaced repetition logic (can be improved later)
    if rating == "again":
        return 1  # Review again immediately
    elif rating == "hard":
        return current_interval * 1.5
    elif rating == "good":
        return current_interval * 2
    elif rating == "easy":
        return current_interval * 3
    return current_interval


@app.route("/help")
def help():
    return render_template("help.html")


@app.route("/logout")
def logout():
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
