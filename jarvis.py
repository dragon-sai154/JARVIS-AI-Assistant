
import tkinter as tk
from tkinter import scrolledtext
import threading
import datetime
import random
import webbrowser
import urllib.parse
import re
import math
import platform
import requests
import pyttsx3
import speech_recognition as sr


# ============================================================
# J.A.R.V.I.S
# ============================================================

# CONST
BG = "#030810"
PANEL = "#081522"
DARK = "#02070d"
WHITE = "#e8fbff"

CYAN = "#00e5ff"
GREEN = "#00ff9d"
YELLOW = "#ffd000"
RED = "#ff4444"
PURPLE = "#c56cff"
BLUE = "#075d75"

current_color = CYAN
rotation = 0
listening = False
processing = False
speaking = False


# SPEECH RECOGNITION

recognizer = sr.Recognizer()

recognizer.pause_threshold = 1.0
recognizer.phrase_threshold = 0.3
recognizer.non_speaking_duration = 0.5

# WINDOW

root = tk.Tk()

root.title(
    "J.A.R.V.I.S - Personal AI Assistant"
)

root.geometry(
    "1200x800"
)

root.minsize(
    950,
    650
)

root.configure(
    bg=BG
)

# COLOUR SYSTEM

def set_theme_color(color, status):

    global current_color

    current_color = color

    root.after(
        0,
        lambda: update_theme(
            color,
            status
        )
    )


def update_theme(color, status):

    try:

        status_label.config(
            text=status,
            fg=color
        )

        title_label.config(
            fg=color
        )

        console_title.config(
            fg=color
        )

        clock_label.config(
            fg=color
        )

        mic_button.config(
            fg=color
        )

        search_button.config(
            fg=color
        )

    except:
        pass

# CHAT

def add_message(sender, message):

    def update():

        chat_box.config(
            state="normal"
        )

        chat_box.insert(
            tk.END,
            f"{sender}: {message}\n\n"
        )

        chat_box.see(
            tk.END
        )

        chat_box.config(
            state="disabled"
        )

    root.after(
        0,
        update
    )

# SPEAK

def speak(message):

    global speaking

    add_message(
        "JARVIS",
        message
    )

    def voice():

        global speaking

        speaking = True

        set_theme_color(
            PURPLE,
            "● SPEAKING"
        )

        try:

            engine = pyttsx3.init()

            engine.setProperty(
                "rate",
                175
            )

            engine.setProperty(
                "volume",
                1.0
            )

            engine.say(
                message
            )

            engine.runAndWait()

            engine.stop()

        except Exception as error:

            add_message(
                "SYSTEM",
                "Voice error: "
                + str(error)
            )

        speaking = False

        set_theme_color(
            GREEN,
            "● SYSTEM ONLINE"
        )

    threading.Thread(
        target=voice,
        daemon=True
    ).start()


MARVEL_KNOWLEDGE = {

    "iron man":
        "Iron Man is Tony Stark, a genius inventor "
        "who uses advanced powered armor and is a "
        "famous member of the Avengers .",

    "tony stark":
        "Tony Stark is the genius inventor behind "
        "the Iron Man armor and a major member of "
        "the Avengers.",

    "spider-man":
        "Spider-Man is Peter Parker, a superhero "
        "with spider-like abilities, web-slinging "
        "and a strong sense of responsibility.",

    "spiderman":
        "Spider-Man is Peter Parker, a superhero "
        "with spider-like abilities, web-slinging "
        "and a strong sense of responsibility.",

    "thor":
        "Thor Odinson is the God of Thunder and a "
        "powerful Asgardian hero and Avenger.",

    "hulk":
        "Hulk is the powerful alter ego of Bruce "
        "Banner. Bruce Banner is a scientist while "
        "Hulk is famous for incredible strength.",

    "bruce banner":
        "Bruce Banner is a brilliant scientist who "
        "can transform into the Hulk.",

    "captain america":
        "Captain America is Steve Rogers, a "
        "super-soldier and one of the most famous "
        "leaders of the Avengers.",

    "black widow":
        "Black Widow is Natasha Romanoff, a highly "
        "skilled spy and former Avenger.",

    "hawkeye":
        "Hawkeye is Clint Barton, an expert archer "
        "and long-time member of the Avengers.",

    "black panther":
        "Black Panther is T'Challa, the protector "
        "of Wakanda and a powerful Marvel hero.",

    "doctor strange":
        "Doctor Strange is Stephen Strange, a "
        "powerful sorcerer and protector against "
        "mystical threats.",

    "scarlet witch":
        "Scarlet Witch is Wanda Maximoff, a powerful "
        "Marvel character with extraordinary magical "
        "abilities.",

    "thanos":
        "Thanos is one of Marvel's most famous "
        "villains and a major threat to the Avengers.",

    "loki":
        "Loki is Thor's adoptive brother and a famous "
        "Marvel character associated with magic and "
        "deception.",

    "avengers":
        "The Avengers are a superhero team created "
        "to face powerful threats. Famous members "
        "include Iron Man, Captain America, Thor, "
        "Hulk, Black Widow and Hawkeye.",

    "infinity stones":
        "The six Infinity Stones are associated with "
        "Space, Mind, Reality, Power, Time and Soul.",

    "infinity stone":
        "There are six Infinity Stones: Space, Mind, "
        "Reality, Power, Time and Soul.",

    "wakanda":
        "Wakanda is the fictional African nation "
        "associated with Black Panther and an "
        "advanced Wakandan civilization.",

    "asgard":
        "Asgard is the home realm of Thor and many "
        "other Asgardians.",

    "guardians of the galaxy":
        "The Guardians of the Galaxy are a team of "
        "heroes who protect the galaxy from major "
        "cosmic threats.",

    "deadpool":
        "Deadpool is Wade Wilson, a Marvel character "
        "known for his humor and unusual fighting style.",

    "wolverine":
        "Wolverine is Logan, a mutant known for his "
        "enhanced healing ability and claws.",

    "x-men":
        "The X-Men are a group of mutant heroes who "
        "fight threats while dealing with tensions "
        "between mutants and humans.",

    "fantastic four":
        "The Fantastic Four are Mr. Fantastic, "
        "Invisible Woman, Human Torch and The Thing.",

    "venom":
        "Venom is a Marvel character connected to "
        "a powerful symbiote and its human host.",

    "ant-man":
        "Ant-Man is a Marvel identity associated "
        "with technology that allows heroes to "
        "change size."
}

def marvel_answer(question):

    text = question.lower().strip()

    # Comparisons first

    if (
        "thor" in text
        and
        "hulk" in text
        and
        (
            "stronger" in text
            or "strong" in text
            or "vs" in text
            or "versus" in text
        )
    ):

        return (
            "That depends on the version and situation, Master. "
            "Thor has powerful Asgardian abilities, lightning "
            "and a wide range of powers, while Hulk is famous "
            "for extraordinary physical strength. In a pure "
            "strength contest, Hulk is often the safer choice, "
            "but Thor has a much broader range of abilities."
        )

    if (
        "iron man" in text
        and
        "captain america" in text
        and
        (
            "stronger" in text
            or "vs" in text
            or "versus" in text
        )
    ):

        return (
            "Iron Man has advanced armor, technology and "
            "long-range abilities. Captain America has "
            "super-soldier abilities, combat skill and his "
            "shield. The winner depends on the version and "
            "rules of the fight."
        )

    if (
        "strongest avenger" in text
        or
        "who is the strongest avenger" in text
    ):

        return (
            "There is no single answer because Marvel has "
            "many versions of its characters. Thor, Hulk, "
            "Captain Marvel and Scarlet Witch can all reach "
            "extremely high power levels depending on the story."
        )

    for topic, answer in MARVEL_KNOWLEDGE.items():

        if topic in text:

            return answer

    return None

ROBLOX_KNOWLEDGE = {

    "what is roblox":
        "Roblox is an online platform where users can "
        "play and create interactive experiences.",

    "roblox":
        "Roblox is an online platform where people can "
        "play experiences and create their own games.",

    "roblox studio":
        "Roblox Studio is the development environment "
        "used to build, edit, test and publish Roblox "
        "experiences.",

    "studio":
        "Roblox Studio is the main tool used to create "
        "and develop Roblox experiences.",

    "lua":
        "Roblox uses Luau, a scripting language derived "
        "from Lua, for programming experiences.",

    "luau":
        "Luau is the scripting language used by Roblox "
        "for creating gameplay and other game systems.",

    "roblox script":
        "A Roblox Script contains Luau code that controls "
        "game behavior.",

    "roblox scripts":
        "Roblox scripts use Luau to control gameplay, "
        "objects, players and other systems.",

    "localscript":
        "A LocalScript runs on the player's client and "
        "is commonly used for client-side behavior and "
        "user interfaces.",

    "local script":
        "A LocalScript runs on the player's client and "
        "is commonly used for client-side behavior.",

    "serverscript":
        "A server Script runs on the server and is commonly "
        "used for important game logic.",

    "server script":
        "A server Script runs on the server and controls "
        "server-side game logic.",

    "remoteevent":
        "A RemoteEvent allows communication between the "
        "client and server in a Roblox experience.",

    "remote event":
        "A RemoteEvent is used to send messages between "
        "client-side and server-side code.",

    "remotefunction":
        "A RemoteFunction allows client and server code "
        "to communicate while expecting a returned value.",

    "remote function":
        "A RemoteFunction allows communication between "
        "client and server code with a return value.",

    "part":
        "A Part is a basic physical building block in "
        "Roblox that can be used to construct environments.",

    "parts":
        "Parts are basic building blocks used to construct "
        "many Roblox environments.",

    "model":
        "A Model is a container that can group multiple "
        "objects together.",

    "npc":
        "An NPC is a non-player character controlled by "
        "the game rather than directly by a player.",

    "npcs":
        "NPCs are characters controlled by game logic "
        "instead of directly by players.",

    "tool":
        "A Tool is an object that players can equip and "
        "use, such as a weapon or special item.",

    "leaderstats":
        "leaderstats is a common Roblox pattern used to "
        "display player statistics such as points, money "
        "or wins on the leaderboard.",

    "leaderboard":
        "A Roblox leaderboard can display player statistics "
        "such as wins, points or money.",

    "obby":
        "An obby is a Roblox obstacle course where players "
        "navigate challenges to reach the finish.",

    "gamepass":
        "A game pass is a Roblox product that can provide "
        "special benefits or features inside an experience.",

    "game pass":
        "A game pass can give players special benefits "
        "inside a Roblox experience.",

    "blox fruits":
        "Blox Fruits is a popular Roblox experience inspired "
        "by anime and pirate adventure themes. Players can "
        "explore, fight enemies, use abilities and progress "
        "their characters.",

    "roblox npc":
        "A Roblox NPC is a non-player character controlled "
        "by scripts or game systems.",

    "roblox game":
        "A Roblox game, officially called an experience, "
        "is an interactive project that players can join "
        "and play.",

    "make a roblox game":
        "To make a Roblox game, you normally use Roblox "
        "Studio to build the world and Luau scripts to "
        "create gameplay systems.",

    "create a roblox game":
        "You can create a Roblox experience using Roblox "
        "Studio and Luau scripting."
}


def roblox_answer(question):

    text = question.lower().strip()


    # Specific questions first

    if (
        "how do i make"
        in text
        and
        "roblox game"
        in text
    ):

        return (
            "To make a Roblox game, Master, open Roblox Studio, "
            "create a new experience, build your map, and use "
            "Luau scripts to add gameplay systems. Then test "
            "your experience before publishing it."
        )


    if (
        "how to make"
        in text
        and
        "roblox game"
        in text
    ):

        return (
            "To make a Roblox game, use Roblox Studio to build "
            "the world and Luau scripts to create the gameplay."
        )


    if (
        "what language"
        in text
        and
        "roblox"
        in text
    ):

        return (
            "Roblox uses Luau, a scripting language derived "
            "from Lua, for programming experiences."
        )


    if (
        "what is"
        in text
        and
        "remoteevent"
        in text
    ):

        return ROBLOX_KNOWLEDGE[
            "remoteevent"
        ]


    if (
        "what is"
        in text
        and
        "npc"
        in text
    ):

        return ROBLOX_KNOWLEDGE[
            "npc"
        ]


    # Normal knowledge

    for topic, answer in ROBLOX_KNOWLEDGE.items():

        if topic in text:

            return answer


    return None

# WIKIPEDIA SEARCH

def clear_results():

    for widget in result_frame.winfo_children():

        widget.destroy()


def show_search_results(results, query):

    clear_results()


    title = tk.Label(

        result_frame,

        text="🔎 RESULTS: " + query,

        font=(
            "Arial",
            10,
            "bold"
        ),

        fg=current_color,

        bg="#0b1b28"

    )

    title.pack(

        anchor="w",

        padx=8,

        pady=5

    )


    for number, result in enumerate(
        results,
        1
    ):

        container = tk.Frame(

            result_frame,

            bg="#0b1b28"

        )

        container.pack(

            fill=tk.X,

            padx=8,

            pady=3

        )


        button = tk.Button(

            container,

            text=(
                str(number)
                + ". "
                + result["title"]
            ),

            command=lambda url=result["link"]:
                webbrowser.open(url),

            bg="#123247",

            fg=CYAN,

            activebackground="#17617c",

            activeforeground=WHITE,

            font=(
                "Arial",
                9,
                "bold"
            ),

            relief="flat",

            anchor="w",

            cursor="hand2"

        )

        button.pack(
            fill=tk.X
        )


        description = tk.Label(

            container,

            text=result["description"],

            font=(
                "Arial",
                8
            ),

            fg=WHITE,

            bg="#0b1b28",

            anchor="w",

            justify="left",

            wraplength=700

        )

        description.pack(

            fill=tk.X,

            padx=8,

            pady=3

        )


def wikipedia_search(query):

    query = query.strip()


    if not query:

        speak(
            "Tell me what you want me to search for, Master."
        )

        return


    clear_results()


    add_message(
        "SEARCH",
        "Searching for: " + query
    )


    set_theme_color(
        CYAN,
        "● SEARCHING"
    )


    def worker():

        try:

            encoded = urllib.parse.quote(
                query
            )


            url = (
                "https://en.wikipedia.org/"
                "w/rest.php/v1/search/page"
                "?q="
                + encoded
                + "&limit=20"
            )
        

            headers = {

                "User-Agent":
                "JARVIS-Educational-Assistant/1.0",

                "Accept":
                "application/json"

            }


            response = requests.get(

                url,

                headers=headers,

                timeout=15

            )


            add_message(

                "SYSTEM",

                "Search response: "
                + str(response.status_code)

            )


            response.raise_for_status()


            data = response.json()


            pages = data.get(
                "pages",
                []
            )


            results = []


            for page in pages:

                title = page.get(
                    "title",
                    "Unknown"
                )


                description = page.get(
                    "description",
                    ""
                )


                excerpt = page.get(
                    "excerpt",
                    ""
                )


                excerpt = re.sub(
                    r"<.*?>",
                    "",
                    excerpt
                )


                description_text = (

                    description
                    or
                    excerpt
                    or
                    "Wikipedia article"

                )


                key = page.get(
                    "key",
                    ""
                )


                if key:

                    article_url = (

                        "https://en.wikipedia.org/wiki/"
                        +
                        urllib.parse.quote(
                            key.replace(
                                " ",
                                "_"
                            )
                        )

                    )

                else:

                    article_url = (

                        "https://en.wikipedia.org/wiki/"
                        +
                        urllib.parse.quote(
                            title.replace(
                                " ",
                                "_"
                            )
                        )

                    )


                results.append({

                    "title": title,

                    "description":
                    description_text,

                    "link":
                    article_url

                })


            if results:

                add_message(

                    "JARVIS",

                    "I found "
                    +
                    str(len(results))
                    +
                    " results."

                )


                first = results[0]


                answer = (

                    "I found information about "
                    +
                    query
                    +
                    ". "
                    +
                    first["title"]
                    +
                    ". "
                    +
                    first["description"]

                )


                if len(answer) > 450:

                    answer = (
                        answer[:450]
                        + "."
                    )


                speak(
                    answer
                )


            else:

                speak(
                    "I couldn't find a matching result."
                )


        except requests.RequestException as error:

            add_message(

                "SYSTEM",

                "Search connection error: "
                + str(error)

            )


            speak(
                "I could not connect to the search service."
            )


        except Exception as error:

            add_message(

                "SYSTEM",

                "Search error: "
                + str(error)

            )


            speak(
                "The search system encountered an error."
            )


        finally:

            set_theme_color(

                GREEN,

                "● SYSTEM ONLINE"

            )


    threading.Thread(

        target=worker,

        daemon=True

    ).start()

# SEARCH COMMAND

def handle_search(command):

    prefixes = [

        "search for ",

        "search the web for ",

        "search ",

        "look up ",

        "find information about ",

        "wikipedia "

    ]


    for prefix in prefixes:

        if command.startswith(prefix):

            query = command[
                len(prefix):
            ].strip()


            if query:

                wikipedia_search(
                    query
                )

                return True


    return False

# math

def calculate_math(command):

    text = command.lower()


    replacements = {

        "what is": "",

        "calculate": "",

        "solve": "",

        "what's": "",

        "multiplied by": "*",

        "multiply by": "*",

        "times": "*",

        "multiply": "*",

        "divided by": "/",

        "divide by": "/",

        "divide": "/",

        "plus": "+",

        "minus": "-"

    }


    for word, symbol in replacements.items():

        text = text.replace(
            word,
            symbol
        )


    text = re.sub(

        r"[^0-9+\-*/(). ]",

        "",

        text

    )


    if not re.search(
        r"\d",
        text
    ):

        return None


    try:

        result = eval(

            text,

            {
                "__builtins__":
                None
            },

            {}

        )


        if (
            isinstance(result, float)
            and
            result.is_integer()
        ):

            result = int(
                result
            )


        return result


    except:

        return None

# COMMAND PROCESSOR

def process_command(command):

    command = command.lower().strip()

    # SHUTDOWN

    if command in [

        "shutdown",

        "shut down",

        "shutdown jarvis",

        "shut down jarvis",

        "exit",

        "quit"

    ]:

        shutdown_jarvis()

        return


    marvel = marvel_answer(
        command
    )


    if marvel:

        speak(
            marvel
        )

        return

    roblox = roblox_answer(
        command
    )


    if roblox:

        speak(
            roblox
        )

        return

    # SEARCH

    if handle_search(
        command
    ):

        return


    if (
        "who is your master"
        in command
        or
        "who is the master"
        in command
        or
        "who created you"
        in command
        or
        "who made you"
        in command
    ):

        speak(

            "My master is DRAGON, also known as "
            "Saicharan, the founder of me. "
            "I am proud to assist my creator."

        )

        return

    # NAME

    if (
        "your name"
        in command
        or
        "who are you"
        in command
    ):

        speak(

            "I am JARVIS, your personal artificial "
            "intelligence assistant."

        )

        return

    # GREETING

    if command in [

        "hi",

        "hello",

        "hey",

        "hi jarvis",

        "hello jarvis",

        "hey jarvis"

    ]:

        speak(

            random.choice([

                "Hello! JARVIS is online.",

                "Hey! My circuits are ready.",

                "Greetings! What can I do for you?",

                "Hello! I was waiting for a command."

            ])

        )

        return

    # HOW ARE YOU
    if "how are you" in command:

        speak(
            "I am fully operational, Master."
        )

        return

    # time

    if "time" in command:

        current_time = (

            datetime.datetime.now()
            .strftime("%I:%M %p")

        )


        speak(

            "The current time is "
            +
            current_time
            +
            ", Master."

        )

        return

    # DATE

    if "date" in command:

        current_date = (

            datetime.datetime.now()
            .strftime("%d %B %Y")

        )


        speak(

            "Today's date is "
            +
            current_date
            +
            ", Master."

        )

        return


    if (
        "what is ai"
        in command
        or
        "what is artificial intelligence"
        in command
    ):

        speak(

            "Artificial intelligence is technology "
            "that allows computers to perform tasks "
            "that normally require human intelligence."

        )

        return
   

    if (
        "what is python"
        in command
        or
        "python programming"
        in command
    ):

        speak(

            "Python is a high level programming language "
            "known for readable syntax and wide use "
            "in software development and artificial intelligence."

        )

        return


    if (
        "machine learning"
        in command
        or
        "what is ml"
        in command
    ):

        speak(

            "Machine learning is a branch of artificial "
            "intelligence where computers learn patterns "
            "from data."

        )

        return



    if (
        "robotics"
        in command
        or
        "what is robotics"
        in command
    ):

        speak(

            "Robotics combines programming, electronics "
            "and engineering to build useful machines."

        )

        return

    if "photosynthesis" in command:

        speak(

            "Photosynthesis is the process where green "
            "plants use sunlight, water and carbon dioxide "
            "to make food and release oxygen."

        )

        return

    if "gravity" in command:

        speak(

            "Gravity is a force that attracts objects "
            "towards each other."

        )

        return

    if command == "open google":

        speak(
            "Opening Google, Master."
        )


        webbrowser.open(
            "https://www.google.com"
        )

        return

    if command == "open youtube":

        speak(
            "Opening YouTube."
        )


        webbrowser.open(
            "https://www.youtube.com"
        )

        return

    
    if (
        "thank you"
        in command
        or
        "thanks"
        in command
    ):

        speak(
            "You're welcome, Master."
        )

        return


    if "status" in command:

        speak(

            "All major JARVIS systems are online "
            "and ready."

        )

        return



    answer = calculate_math(
        command
    )


    if answer is not None:

        speak(

            "The answer is "
            +
            str(answer)
        )

        return


    if len(command) > 0:

        add_message(

            "SYSTEM",

            "I don't have that in my local knowledge."

        )

        add_message(

            "SYSTEM",

            "Using web knowledge..."

        )


        wikipedia_search(
            command
        )

        return


    speak(

        random.choice([

            "I don't know that one yet.",

            "That one escaped my circuits.",

            "Interesting. I need more data for that.",

            "I don't have an answer for that yet.",

            "I am not asian"

        ])

    )


def send_command():

    global processing


    if processing:

        return


    command = command_entry.get().strip()


    if not command:

        return


    add_message(
        "YOU",
        command
    )


    command_entry.delete(
        0,
        tk.END
    )


    processing = True


    set_theme_color(
        YELLOW,
        "● PROCESSING"
    )


    def worker():

        global processing

        process_command(
            command
        )

        processing = False


        if not speaking:

            set_theme_color(

                GREEN,

                "● SYSTEM ONLINE"

            )


    threading.Thread(

        target=worker,

        daemon=True

    ).start()

    # _microphone

def listen_microphone():

    global listening
    global processing


    if listening or processing:

        return


    listening = True


    mic_button.config(

        text="🎤 LISTENING...",

        state="disabled"

    )


    set_theme_color(

        GREEN,

        "● LISTENING"

    )


    def listen():

        global listening


        try:

            with sr.Microphone() as source:

                add_message(

                    "SYSTEM",

                    "🎤 Speak now..."

                )


                recognizer.adjust_for_ambient_noise(

                    source,

                    duration=0.5

                )


                audio = recognizer.listen(

                    source,

                    timeout=10,

                    phrase_time_limit=50

                )


            set_theme_color(

                YELLOW,

                "● PROCESSING"

            )


            add_message(

                "SYSTEM",

                "Processing voice..."

            )


            text = recognizer.recognize_google(
                audio
            )


            add_message(
                "YOU",
                text
            )


            process_command(
                text
            )


        except sr.WaitTimeoutError:

            add_message(

                "SYSTEM",

                "I didn't hear you start speaking."

            )


        except sr.UnknownValueError:

            add_message(

                "SYSTEM",

                "Sorry, I couldn't understand that."

            )


        except sr.RequestError:

            add_message(

                "SYSTEM",

                "Speech recognition service is unavailable."

            )


        except Exception as error:

            add_message(

                "SYSTEM",

                "Microphone error: "
                +
                str(error)

            )


        listening = False


        root.after(

            0,

            lambda:
            mic_button.config(

                text="🎤 SPEAK TO JARVIS",

                state="normal"

            )

        )


        if not speaking:

            set_theme_color(

                GREEN,

                "● SYSTEM ONLINE"

            )


    threading.Thread(

        target=listen,

        daemon=True

    ).start()

# clear_chat

def clear_chat():

    chat_box.config(
        state="normal"
    )


    chat_box.delete(
        "1.0",
        tk.END
    )


    chat_box.config(
        state="disabled"
    )


    clear_results()


    add_message(

        "SYSTEM",

        "Conversation cleared."

    )


def shutdown_jarvis():

    global processing

    processing = True


    set_theme_color(

        RED,

        "● SHUTTING DOWN"

    )


    add_message(

        "SYSTEM",

        "J.A.R.V.I.S shutting down..."

    )


    def close():

        try:

            engine = pyttsx3.init()

            engine.setProperty(
                "rate",
                175
            )

            engine.setProperty(
                "volume",
                1.0
            )

            engine.say(
                "Shutting down."
            )

            engine.runAndWait()

            engine.stop()

        except:

            pass


        root.destroy()


    root.afteFr(
        1200,
        close
    )


def update_clock():

    now = datetime.datetime.now()


    clock_label.config(

        text=now.strftime(
            "%I:%M:%S %p"
        )

    )


    date_label.config(

        text=now.strftime(
            "%A, %d %B %Y"
        )

    )


    root.after(
        1000,
        update_clock
    )


def animate_core():

    global rotation


    core_canvas.delete(
        "all"
    )


    cx = 125
    cy = 125


    for radius in [

        110,

        92,

        74

    ]:

        core_canvas.create_oval(

            cx - radius,

            cy - radius,

            cx + radius,

            cy + radius,

            outline=current_color,

            width=2

        )


    core_canvas.create_oval(

        60,

        60,

        190,

        190,

        outline=current_color,

        width=4

    )


    for number in range(12):

        angle = math.radians(

            rotation
            +
            number * 30

        )


        x = (

            cx
            +
            88
            *
            math.cos(angle)

        )


        y = (

            cy
            +
            88
            *
            math.sin(angle)

        )


        core_canvas.create_oval(

            x - 3,

            y - 3,

            x + 3,

            y + 3,

            fill=current_color,

            outline=""

        )


    core_canvas.create_text(

        cx,

        cy - 10,

        text="JARVIS",

        fill=current_color,

        font=(
            "Arial",
            19,
            "bold"
        )

    )


    core_canvas.create_text(

        cx,

        cy + 18,

        text="AI CORE",

        fill=WHITE,

        font=(
            "Arial",
            9,
            "bold"
        )

    )


    rotation += 4


    root.after(
        40,
        animate_core
    )

# _header

header = tk.Frame(

    root,

    bg=BG,

    height=85

)

header.pack(
    fill=tk.X
)

header.pack_propagate(
    False
)


title_label = tk.Label(

    header,

    text="J.A.R.V.I.S",

    font=(
        "Arial",
        30,
        "bold"
    ),

    fg=CYAN,

    bg=BG

)

title_label.pack(
    pady=(8, 0)
)


tk.Label(

    header,

    text="PERSONAL ARTIFICIAL INTELLIGENCE ASSISTANT",

    font=(
        "Arial",
        9,
        "bold"
    ),

    fg=WHITE,

    bg=BG

).pack()

# _mainframe

main_frame = tk.Frame(

    root,

    bg=BG

)

main_frame.pack(

    fill=tk.BOTH,

    expand=True,

    padx=15,

    pady=5

)

# _left_panel

left_panel = tk.Frame(

    main_frame,

    bg=PANEL,

    width=290

)

left_panel.pack(

    side=tk.LEFT,

    fill=tk.Y,

    padx=(0, 8)

)

left_panel.pack_propagate(
    False
)

# _core

core_canvas = tk.Canvas(

    left_panel,

    width=250,

    height=250,

    bg=PANEL,

    highlightthickness=0

)

core_canvas.pack(
    pady=10
)

# _status

status_label = tk.Label(

    left_panel,

    text="● SYSTEM ONLINE",

    font=(
        "Arial",
        12,
        "bold"
    ),

    fg=GREEN,

    bg=PANEL

)

status_label.pack(
    pady=5
)

# _moniter_frame

monitor_frame = tk.Frame(

    left_panel,

    bg="#0b1b28"

)

monitor_frame.pack(

    fill=tk.X,

    padx=15,

    pady=15

)


tk.Label(

    monitor_frame,

    text="SYSTEM MONITOR",

    font=(
        "Arial",
        10,
        "bold"
    ),

    fg=CYAN,

    bg="#0b1b28"

).pack(
    pady=8
)


monitor_items = [

    "● CORE: ONLINE",

    "● VOICE: ONLINE",

    "● MICROPHONE: READY",

    "● SEARCH: ONLINE",

    "PYTHON: "
    +
    platform.python_version(),

    "OS: "
    +
    platform.system()

]


for item in monitor_items:

    tk.Label(

        monitor_frame,

        text=item,

        font=(
            "Consolas",
            9
        ),

        fg=(

            GREEN
            if (
                "ONLINE" in item
                or
                "READY" in item
            )
            else WHITE

        ),

        bg="#0b1b28"

    ).pack(

        anchor="w",

        padx=12,

        pady=2

    )

# _right_panel

right_panel = tk.Frame(

    main_frame,

    bg=PANEL

)

right_panel.pack(

    side=tk.RIGHT,

    fill=tk.BOTH,

    expand=True

)

# _clock

clock_label = tk.Label(

    right_panel,

    text="00:00:00",

    font=(
        "Consolas",
        20,
        "bold"
    ),

    fg=CYAN,

    bg=PANEL

)

clock_label.pack(
    pady=(5, 0)
)


date_label = tk.Label(

    right_panel,

    text="",

    font=(
        "Arial",
        9
    ),

    fg=WHITE,

    bg=PANEL

)

date_label.pack()

# _console_title

console_title = tk.Label(

    right_panel,

    text="COMMAND CONSOLE",

    font=(
        "Arial",
        11,
        "bold"
    ),

    fg=CYAN,

    bg=PANEL

)

console_title.pack(

    anchor="w",

    padx=15,

    pady=5

)

# _chat_box

chat_box = scrolledtext.ScrolledText(

    right_panel,

    font=(
        "Consolas",
        10
    ),

    bg=DARK,

    fg=WHITE,

    insertbackground=WHITE,

    wrap=tk.WORD,

    relief="flat"

)

chat_box.pack(

    fill=tk.BOTH,

    expand=True,

    padx=15,

    pady=5

)


chat_box.config(
    state="disabled"
)

# _result_frame

result_frame = tk.Frame(

    right_panel,

    bg="#0b1b28"

)

result_frame.pack(

    fill=tk.X,

    padx=10,

    pady=5

)

# bottom_panel
bottom_panel = tk.Frame(

    right_panel,

    bg="#0b1b28",

    height=140

)

bottom_panel.pack(

    side=tk.BOTTOM,

    fill=tk.X,

    padx=10,

    pady=8

)

bottom_panel.pack_propagate(
    False
)

# INPUT

input_row = tk.Frame(

    bottom_panel,

    bg="#0b1b28"

)

input_row.pack(

    fill=tk.X,

    padx=10,

    pady=(8, 5)

)


command_entry = tk.Entry(

    input_row,

    bg=DARK,

    fg=WHITE,

    insertbackground=WHITE,

    font=(
        "Arial",
        11
    ),

    relief="flat"

)

command_entry.pack(

    side=tk.LEFT,

    fill=tk.X,

    expand=True,

    ipady=8,

    padx=(0, 8)

)


send_button = tk.Button(

    input_row,

    text="SEND",

    command=send_command,

    bg=BLUE,

    fg=WHITE,

    activebackground=CYAN,

    activeforeground=DARK,

    font=(
        "Arial",
        10,
        "bold"
    ),

    relief="flat",

    width=10

)

send_button.pack(

    side=tk.RIGHT,

    ipady=7

)

# BUTTON ROW

button_row = tk.Frame(

    bottom_panel,

    bg="#0b1b28"

)

button_row.pack(

    fill=tk.X,

    padx=10,

    pady=(2, 8)

)

# MICROPHONE

mic_button = tk.Button(

    button_row,

    text="🎤 SPEAK TO JARVIS",

    command=listen_microphone,

    bg="#123247",

    fg=CYAN,

    activebackground="#17617c",

    activeforeground=WHITE,

    font=(
        "Arial",
        11,
        "bold"
    ),

    relief="flat"

)

mic_button.pack(

    side=tk.LEFT,

    fill=tk.X,

    expand=True,

    padx=(0, 5),

    ipady=9

)

# btn_search

search_button = tk.Button(

    button_row,

    text="🔎 SEARCH",

    command=lambda:
        wikipedia_search(
            command_entry.get()
        ),

    bg="#123f52",

    fg=CYAN,

    activebackground="#17617c",

    activeforeground=WHITE,

    font=(
        "Arial",
        11,
        "bold"
    ),

    relief="flat"

)

search_button.pack(

    side=tk.LEFT,

    fill=tk.X,

    expand=True,

    padx=5,

    ipady=9

)


# btn_clear

clear_button = tk.Button(

    button_row,

    text="🗑 CLEAR",

    command=clear_chat,

    bg="#3a2020",

    fg="#ff7777",

    activebackground="#633030",

    activeforeground=WHITE,

    font=(
        "Arial",
        11,
        "bold"
    ),

    relief="flat"

)

clear_button.pack(

    side=tk.RIGHT,

    padx=5,

    ipadx=10,

    ipady=9

)

# btn_shutdown

shutdown_button = tk.Button(

    button_row,

    text="⏻ SHUTDOWN",

    command=shutdown_jarvis,

    bg="#451c1c",

    fg=RED,

    activebackground="#ff3333",

    activeforeground=WHITE,

    font=(
        "Arial",
        11,
        "bold"
    ),

    relief="flat"

)

shutdown_button.pack(

    side=tk.RIGHT,

    padx=(5, 0),

    ipadx=10,

    ipady=9

)

# _label

tk.Label(

    root,

    text="J.A.R.V.I.S • Created by DRAGON aka Saicharan",

    font=(
        "Arial",
        8
    ),

    fg="#4c8090",

    bg=BG

).pack(

    side=tk.BOTTOM,

    pady=3

)

# bind_enter

command_entry.bind(

    "<Return>",

    lambda event:
        send_command()

)

# STARTUP

add_message(

    "SYSTEM",

    "Initializing J.A.R.V.I.S..."

)


add_message(

    "SYSTEM",

    "Voice recognition: ONLINE"

)


add_message(

    "SYSTEM",

    "Text-to-speech: ONLINE"

)


add_message(

    "SYSTEM",

    "Search system: ONLINE"

)

add_message(

    "SYSTEM",

    "Dynamic colour system: ONLINE"

)


add_message(

    "SYSTEM",

    "Shutdown command: ONLINE"

)


add_message(

    "SYSTEM",

    "All systems online."

)


add_message(

    "JARVIS",

    "Welcome, Master ."

)


# START

animate_core()

update_clock()

root.mainloop()

