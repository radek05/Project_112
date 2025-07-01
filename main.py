"""
main.py: druhý projekt do Engeto Online Python Akademie

author: Radek Doleček
email: radek.dolecek@gmail.com
discord: Radek
discord user: radek0913
"""

# Import knihoven
import random
import time

start_time = time.time()  # Start měření času

# Úvodní výpis
print("Hi there!")
print("Let's play a bulls and cows game.")
line = "-" * 47
print(line)
print("I've generated a random 4 digit number for you.")
print("Your task is to guess it.")
print(line)

def generate_number(show_number=False): 
    """Vygeneruje 4místné číslo s unikátními číslicemi, první není nula."""

    cislo = random.sample("123456789", 1)  # První číslice není nula
    cislo += random.sample([c for c in "0123456789" if c not in cislo], 3)  # Další unikátní číslice
    random.shuffle(cislo)  # Promíchání číslic
    if cislo[0] == '0':  # Zajistí, že první číslice není nula
        for i in range(1, 4):
            if cislo[i] != '0':
                cislo[0], cislo[i] = cislo[i], cislo[0]
                break
    if show_number:
        print(f"Secret number is: {''.join(cislo)}")
        return cislo
    else:
        print("Secret number is: ****")
        return cislo
    
    
def uhodni_cislo(user, secret):
    """Porovná uživatelský tip s tajným číslem, vrací bulls/cows a jejich pozice."""

    uhadnute_cislo = []
    nezarazene_cislo = []
    cows_pos = []
    bulls = 0
    cows = 0
    user = list(user)
    secret = list(str(secret))

    # Bulls: správná číslice na správné pozici
    for i in range(len(secret)):
        if user[i] == secret[i]:
            bulls += 1
            uhadnute_cislo.append((i, user[i]))
            user[i] = None
            secret[i] = None

    # Cows: správná číslice na špatné pozici
    for i in range(len(secret)):
        if user[i] is not None and user[i] in secret:
            cows += 1
            nezarazene_cislo.append(user[i])
            cows_pos.append((i, user[i]))
            secret[secret.index(user[i])] = None
    return bulls, cows, cows_pos, uhadnute_cislo, nezarazene_cislo

secret_num = generate_number()  # Vygeneruj tajné číslo
attempts = 0  # Počet pokusů

# Dotaz na zobrazení tajného čísla
while True:
    zobrazit = input("Do you want to see the secret number? (yes/no): ").lower()
    if zobrazit in ["yes", "y"]:
        secret_num = generate_number(show_number=True)
        print(line)
        break
    elif zobrazit in ["no", "n"]:
        secret_num = generate_number(show_number=False)
        print(line)
        break
    else:
        print("Please type 'yes' or 'no'.")

# Hlavní herní smyčka
while True:
    user_input = input("Enter a 4-digit number (or 'exit'): ")
    print(line)
    if user_input.lower() == 'exit':
        print(f"You exited the game. Secret number was {''.join(secret_num)}.")
        break

    # Kontrola vstupu: 4 číslice, unikátní, pouze čísla
    if len(user_input) != 4 or not user_input.isdigit() or len(set(user_input)) != 4:
        print("Please enter a valid 4-digit number with unique digits.")
        continue
    attempts += 1  # Započítání pokusu

    try:
        # Porovnání tipu s tajným číslem
        (bulls, cows, cows_pos, uhadnute_cislo, nezarazene_cislo) = uhodni_cislo(user_input, ''.join(secret_num))
        if bulls == 4:

            # Výhra
            print(f"🎉 Correct! You guessed the number {''.join(secret_num)} in {attempts} attempt(s).")
            print(line)
            elapsed_time = time.time() - start_time
            print(f"⏱️ Time taken: {elapsed_time:.1f} seconds.")
            print(line)
            print("Thanks for playing!")

            # Získání jména hráče
            while True:
                name = input("Your name: ").strip()
                if not name:
                    name = "Unknown"
                if name:
                    break
                print("Name can't be empty.")

            # Zápis výsledku do scoreboardu
            with open("scoreboard.txt", "a", encoding="utf-8") as f:
                f.write(f"{name},{elapsed_time:.1f},{attempts}\n")

            # Čtení a výpis scoreboardu
            records = []
            with open("scoreboard.txt", "r", encoding="utf-8") as f:
                for line_score in f:
                    parts = line_score.strip().split(",")
                    if len(parts) == 3:
                        jmeno, cas, pokusy = parts
                    elif len(parts) == 2:
                        jmeno, cas = parts
                        pokusy = "?"
                    else:
                        continue
                    try:
                        cas_float = float(cas)
                    except ValueError:
                        continue
                    records.append((jmeno, cas_float, pokusy))
            sorted_records = sorted(records, key=lambda x: x[1])[:10]

            # Výpis TOP 10 hráčů
            print("\n🏆 TOP 10 hráčů:")
            print(f"{'Pořadí':<6} {'Jméno':<20} {'Čas (s)':>8} {'Pokusy':>8}")
            print("-" * 46)
            for i, (jmeno, cas, pokusy) in enumerate(sorted_records, 1):
                if i == 1:
                    print(f"{i:<6} {jmeno:<20} {cas:>8.1f} {str(pokusy):>8} ⭐")
                else:
                    print(f"{i:<6} {jmeno:<20} {cas:>8.1f} {str(pokusy):>8}")
            break

        else:
            # Výpis pokusu a výsledků
            print(f"Attempt {attempts}")
        print(line)

        # Výpis bulls
        if bulls > 0:
            if bulls == 1:
                print("You have 1 bull.")
            else:
                print(f"You have {bulls} bulls")
            for pozice, cislo in uhadnute_cislo:
                print(f"Bull: {cislo} at position {pozice + 1}")
        else:
            print("No correctly placed digits in bull(s) yet.")
        print(line)

        # Výpis cows
        if cows > 0:
            if cows == 1:
                print("You have 1 cow.")
            else:
                print(f"You have {cows} cows")
            for index, digit in cows_pos:
                print(f"Cow: {digit} is correct but in wrong position: {index + 1}")
        else:
            print("No digits guessed in wrong position (cows) yet.")
        print(line)

    except ValueError as input_error:
        print(f"Error: {input_error}")  # Ošetření chybného vstupu