from mdtidy.gemini_processor import process_gemini_conversation
from mdtidy.gpt_processor import process_gpt_conversation
import re
from colorama import init, Fore, Style

init(autoreset=True)  # Initialize colorama

def print_welcome_message():
    welcome_art = r"""
    __  __ _____ _____ _     _       
   |  \/  |  __ \_   _(_)   | |      
   | \  / | |  | || |  _  __| |_   _ 
   | |\/| | |  | || | | |/ _` | | | |
   | |  | | |__| || |_| | (_| | |_| |
   |_|  |_|_____/_____|_|\__,_|\__, |
                                __/ |
                               |___/ 
    """
    print(Fore.CYAN + welcome_art)
    print(Fore.GREEN + "Welcome to MDtidy!".center(50))
    print(Fore.YELLOW + "This tool processes GPT and Gemini conversation data into structured Jupyter notebooks.".center(50))
    print(Fore.MAGENTA + "Please enter the conversation URL to begin or type 'exit' to quit.".center(50))
    print("\n" + "=" * 50 + "\n")

def print_farewell_message():
    farewell_art = r"""
       ______                ____            _ 
      |  ____|              |  _ \          | |
      | |__ __ _ _ __ ___   | |_) |_   _  __| |
      |  __/ _` | '__/ _ \  |  _ <| | | |/ _` |
      | | | (_| | | |  __/  | |_) | |_| | (_| |
      |_|  \__,_|_|  \___|  |____/ \__,_|\__,_|
                                               
    """
    print(Fore.CYAN + farewell_art)
    print(Fore.YELLOW + "Thanks for using MDtidy!".center(50))
    print(Fore.GREEN + "We hope you found it helpful.".center(50))
    print(Fore.MAGENTA + "Have a great day and happy data processing!".center(50))
    print("\n" + "=" * 50 + "\n")

def process_conversation() -> None:
    print_welcome_message()
    while True:
        url = input(Fore.CYAN + "Enter the GPT conversation URL (or type 'exit' to quit): " + Style.RESET_ALL).strip()
        
        if url.lower() == 'exit':
            print_farewell_message()
            break
        
        if re.match(r'^https://chatgpt\.com/share/[0-9a-fA-F-]{36}$', url):
            print(Fore.GREEN + "\nProcessing GPT conversation...")
            process_gpt_conversation(url)
            
            # Prompt for Gemini URL
            gemini_url = input(Fore.CYAN + "\nWould you like to process a Gemini conversation? Enter the URL or type 'skip' to finish: " + Style.RESET_ALL).strip()
            
            if gemini_url.lower() == 'skip':
                print_farewell_message()
                break
            elif re.match(r'^https://g.co/gemini/share/[a-zA-Z0-9]+$', gemini_url):
                print(Fore.GREEN + "\nProcessing Gemini conversation...")
                process_gemini_conversation(gemini_url)
                print_farewell_message()
                break
            else:
                print(Fore.RED + "\nInvalid Gemini URL format. Exiting...")
                print_farewell_message()
                break
        
        elif re.match(r'^https://g.co/gemini/share/[a-zA-Z0-9]+$', url):
            print(Fore.GREEN + "\nProcessing Gemini conversation...")
            process_gemini_conversation(url)
            
            # Prompt for GPT URL
            gpt_url = input(Fore.CYAN + "\nWould you like to process a GPT conversation? Enter the URL or type 'skip' to finish: " + Style.RESET_ALL).strip()
            
            if gpt_url.lower() == 'skip':
                print_farewell_message()
                break
            elif re.match(r'^https://chatgpt\.com/share/[0-9a-fA-F-]{36}$', gpt_url):
                print(Fore.GREEN + "\nProcessing GPT conversation...")
                process_gpt_conversation(gpt_url)
                print_farewell_message()
                break
            else:
                print(Fore.RED + "\nInvalid GPT URL format. Exiting...")
                print_farewell_message()
                break
        
        else:
            print(Fore.RED + "\nInvalid URL format. Please enter a valid GPT or Gemini conversation URL or type 'exit' to quit.")