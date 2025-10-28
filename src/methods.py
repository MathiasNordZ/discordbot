import discord
import json
import os

# Path to your reputation data file
FILE_PATH = "data/rep.json"


# -------------------------------
# JSON Handling
# -------------------------------

def load_reps():
    """Load reputation data from JSON file."""
    if not os.path.exists(FILE_PATH):
        # Make sure the folder exists
        os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
        return {}

    with open(FILE_PATH, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}  # In case the file is empty or corrupted


def save_reps(data):
    """Save reputation data to JSON file."""
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)


# -------------------------------
# Reputation Commands
# -------------------------------

def pRep(message, user):
    """Give +1 reputation to a user."""
    emoji = discord.utils.get(message.guild.emojis, name="plusrep")
    if emoji is None:
        emoji = "👍"

    reps = load_reps()

    # Update user’s score (case-insensitive)
    user_key = user.capitalize()
    reps[user_key] = reps.get(user_key, 0) + 1

    save_reps(reps)

    return f"✅ Gave +1 rep to **{user_key}**! Total: **{reps[user_key]}** {emoji}"


def mRep(message, user):
    """Give -1 reputation to a user."""
    emoji = discord.utils.get(message.guild.emojis, name="minusrep")
    if emoji is None:
        emoji = "👎"

    reps = load_reps()

    # Update user’s score
    user_key = user.capitalize()
    reps[user_key] = reps.get(user_key, 0) - 1

    save_reps(reps)

    return f"⚠️ Gave -1 rep to **{user_key}**! Total: **{reps[user_key]}** {emoji}"


# -------------------------------
# Utility Command (optional)
# -------------------------------

def getLeaderboard(limit=10):
    """Return a formatted string of the top rep users."""
    reps = load_reps()

    if not reps:
        return "No reputation data yet!"

    # Sort by score (highest first)
    sorted_users = sorted(reps.items(), key=lambda x: x[1], reverse=True)

    leaderboard = "**🏆 Reputation Leaderboard 🏆**\n"
    for i, (user, score) in enumerate(sorted_users[:limit], start=1):
        leaderboard += f"{i}. **{user}** — {score} points\n"

    return leaderboard