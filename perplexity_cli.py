#!/usr/bin/env python3
"""
Perplexity AI CLI - A command-line interface for Perplexity AI

Version: 2.2.0
Author: zahidoverflow (Enhanced from original by redscorpse)
Repository: https://github.com/zahidoverflow/perplexity-cli
License: MIT License

A powerful command-line tool that brings Perplexity AI's web-search powered
conversational AI directly to your terminal. Optimized for pipx installation.
"""

__version__ = "2.2.0"
__author__ = "zahidoverflow"
__email__ = "imzooel@gmail.com"
__license__ = "MIT"
__url__ = "https://github.com/zahidoverflow/perplexity-cli"

from uuid import uuid4
from time import sleep, time
from threading import Thread
from json import loads, dumps
from random import getrandbits
from websocket import WebSocketApp
from requests import Session
import subprocess
import sys


class Perplexity:
    def __init__(self):
        self.session = Session()
        self.user_agent = {
            "User-Agent": "Ask/2.4.1/224 (iOS; iPhone; Version 18.1) isiOSOnMac/false",
            "X-Client-Name": "Perplexity-iOS",
        }
        self.session.headers.update(self.user_agent)
        self.t = format(getrandbits(32), "08x")
        URL = f"https://www.perplexity.ai/socket.io/?EIO=4&transport=polling&t={self.t}"
        self.sid = loads(self.session.get(url=URL).text[1:])["sid"]
        self.n = 1
        self.base = 420
        self.finished = True
        self.last_uuid = None
        
        # Test the anonymous user authentication
        auth_response = self.session.post(
            url=f"https://www.perplexity.ai/socket.io/?EIO=4&transport=polling&t={self.t}&sid={self.sid}",
            data='40{"jwt":"anonymous-ask-user"}',
        )
        if auth_response.text != "OK":
            raise Exception("Failed to authenticate anonymous user.")
            
        self.ws = self._init_websocket()
        self.ws_thread = Thread(target=self.ws.run_forever).start()
        
        # Wait for connection
        retry_count = 0
        while not (self.ws.sock and self.ws.sock.connected) and retry_count < 50:
            sleep(0.1)
            retry_count += 1
        
        if retry_count >= 50:
            raise Exception("WebSocket connection timeout")

    def _init_websocket(self):
        def on_open(ws):
            ws.send("2probe")
            ws.send("5")

        def on_message(ws, message):
            try:
                if message == "2":
                    ws.send("3")
                elif not self.finished:
                    if message.startswith("42"):
                        message_data = loads(message[2:])
                        content = message_data[1]
                        
                        self.queue.append(content)
                        
                        # Check if this is the final message
                        if content.get("final") and content.get("status") == "COMPLETED":
                            self.finished = True
                            
                    elif message.startswith("43"):
                        message_data = loads(message[3:])[0]
                        self.queue.append(message_data)
                        self.finished = True
            except Exception as e:
                pass  # Ignore parsing errors

        def on_error(ws, error):
            pass  # Ignore WebSocket errors

        cookies = ""
        for key, value in self.session.cookies.get_dict().items():
            cookies += f"{key}={value}; "
            
        return WebSocketApp(
            url=f"wss://www.perplexity.ai/socket.io/?EIO=4&transport=websocket&sid={self.sid}",
            header=self.user_agent,
            cookie=cookies[:-2],
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
        )

    def generate_answer(self, query):
        self.finished = False
        if self.n == 9:
            self.n = 0
            self.base *= 10
        else:
            self.n += 1
        self.queue = []
        
        self.ws.send(
            str(self.base + self.n)
            + dumps(
                [
                    "perplexity_ask",
                    query,
                    {
                        "frontend_session_id": str(uuid4()),
                        "language": "en-GB",
                        "timezone": "UTC",
                        "search_focus": "internet",
                        "frontend_uuid": str(uuid4()),
                        "mode": "concise",
                    },
                ]
            )
        )
        
        start_time = time()
        while (not self.finished) or len(self.queue) != 0:
            if time() - start_time > 30:
                self.finished = True
                return [{"error": "Timed out."}]
            if len(self.queue) != 0:
                yield self.queue.pop(0)
        self.ws.close()


class tColor:
    reset = '\033[0m'
    bold = '\033[1m'
    red = '\033[91m'
    green = '\033[92m'
    yellow = '\033[93m'
    blue = '\033[94m'
    purple = '\033[38;2;181;76;210m'
    lavand = '\033[38;5;140m'
    aqua = '\033[38;5;109m'
    aqua2 = '\033[38;5;158m'


def extract_answer_from_response(response_list):
    """Extract answer and references from response"""
    answer_text = ""
    references = []
    
    # Find the final response with the complete text
    for item in response_list:
        if isinstance(item, dict) and item.get("final") and item.get("status") == "COMPLETED" and "text" in item:
            try:
                # Parse the text field which contains step information
                steps = loads(item["text"])
                for step in steps:
                    if step.get("step_type") == "FINAL" and "content" in step:
                        content = step["content"]
                        if "answer" in content:
                            try:
                                # The answer is JSON-encoded
                                answer_data = loads(content["answer"])
                                answer_text = answer_data.get("answer", "")
                                references = answer_data.get("web_results", [])
                            except:
                                answer_text = content["answer"]
                        break
                break
            except:
                continue
    
    return answer_text, references


def quick_question():
    prompt = sys.argv[1]
    try:
        answer_list = list(Perplexity().generate_answer(prompt))
        answer, references = extract_answer_from_response(answer_list)
        
        if answer:
            print(tColor.aqua2 + answer + tColor.reset)
        else:
            print(tColor.red + "No answer received" + tColor.reset)
            
    except Exception as e:
        print(f"{tColor.red}Error: {e}{tColor.reset}")


def show_version():
    """Display version information."""
    print(f"{tColor.purple}Perplexity AI CLI{tColor.reset} {tColor.aqua}v{__version__}{tColor.reset}")
    print("A command-line interface for Perplexity AI")
    print(f"License: {__license__}")
    print(f"Repository: {__url__}")


def print_help():
    """Display help information."""
    print(f"{tColor.purple}Perplexity AI CLI{tColor.reset} {tColor.aqua}v{__version__}{tColor.reset}")
    print("A command-line interface for Perplexity AI with web search capabilities")
    print()
    print(f"{tColor.bold}Usage:{tColor.reset}")
    print("  perplexity-cli                    # Interactive mode")
    print("  pplx                              # Short alias (interactive)")
    print("  perplexity-cli 'your question'   # Quick question")
    print("  pplx 'your question'             # Short alias (quick question)")
    print()
    print(f"{tColor.bold}Options:{tColor.reset}")
    print("  --version, -v     Show version information")
    print("  --help, -h        Show this help message")
    print()
    print(f"{tColor.bold}Interactive Commands:{tColor.reset}")
    print("  /help             Show interactive commands")
    print("  /refs             Show references from last answer")
    print("  /clear            Clear the screen")
    print("  /quit             Exit the program")
    print()
    print(f"{tColor.bold}Installation:{tColor.reset}")
    print("  pipx install git+https://github.com/zahidoverflow/perplexity-cli.git")
    print()
    print(f"{tColor.bold}Examples:{tColor.reset}")
    print("  perplexity-cli 'What is quantum computing?'")
    print("  pplx 'How does AI work?'")


def answer_question(question):
    """Answer a single question (non-interactive mode)."""
    try:
        print(f"{tColor.aqua}🔍 Question: {question}{tColor.reset}")
        print(f"{tColor.aqua}🔄 Searching the web...{tColor.reset}\n")
        
        answer_list = list(Perplexity().generate_answer(question))
        answer, references = extract_answer_from_response(answer_list)
        
        if answer:
            print(f"{tColor.bold}🤖 Answer:{tColor.reset}")
            print(f"{tColor.bold}{'─' * 50}{tColor.reset}")
            print(f"{tColor.aqua2}{answer}{tColor.reset}")
            
            if references:
                print(f"\n{tColor.bold}📚 References ({len(references)} sources):{tColor.reset}")
                for i, ref in enumerate(references[:5]):  # Show max 5 references
                    name = ref.get('name', 'Unknown Source')
                    url = ref.get('url', 'No URL')
                    print(f"{tColor.blue}[{i+1}]{tColor.reset} {name}")
                    print(f"    {url}")
                if len(references) > 5:
                    print(f"    {tColor.yellow}... and {len(references)-5} more sources{tColor.reset}")
        else:
            print(f"{tColor.red}❌ No answer received. Please try again or rephrase your question.{tColor.reset}")
            
    except Exception as e:
        print(f"{tColor.red}💥 Error: {e}{tColor.reset}")


def interactive_mode():
    """Run the CLI in enhanced interactive mode."""
    # Display welcome banner
    print(f"\n{tColor.bold}┌─────────────────────────────────────────────┐{tColor.reset}")
    print(f"{tColor.bold}│{tColor.reset} {tColor.purple}🤖 Perplexity AI CLI{tColor.reset} {tColor.aqua}v{__version__}{tColor.reset} {tColor.bold}              │{tColor.reset}")
    print(f"{tColor.bold}│{tColor.reset} Interactive mode with web search powered AI {tColor.bold}│{tColor.reset}")
    print(f"{tColor.bold}└─────────────────────────────────────────────┘{tColor.reset}\n")
    
    # Show enhanced usage instructions
    print(f"{tColor.bold}💡 Quick Start:{tColor.reset}")
    print(f"  • Type your question and press {tColor.aqua}Enter{tColor.reset} twice")
    print(f"  • Use {tColor.green}/help{tColor.reset} for commands")
    print(f"  • Press {tColor.yellow}Ctrl+C{tColor.reset} to exit\n")

    prompt = ""
    references = []
    conversation_count = 0
    
    while True:
        try:
            # Show conversation number for clarity
            if conversation_count > 0:
                line = input(f"{tColor.lavand}[{conversation_count+1}] ❯{tColor.reset} ")
            else:
                line = input(f"{tColor.lavand}❯{tColor.reset} ")
                
            # Handle special commands
            if line.strip().startswith('/'):
                command = line.strip().lower()
                
                if command == '/help':
                    show_interactive_help()
                    continue
                elif command == '/clear':
                    print("\033[2J\033[H")  # Clear screen
                    print(f"{tColor.green}✨ Screen cleared!{tColor.reset}\n")
                    continue
                elif command == '/refs':
                    show_references(references)
                    continue
                elif command == '/quit' or command == '/exit':
                    print(f"{tColor.yellow}👋 Goodbye!{tColor.reset}")
                    break
                elif command == '/version':
                    show_version()
                    continue
                else:
                    print(f"{tColor.red}❌ Unknown command: {command}{tColor.reset}")
                    print(f"   Type {tColor.green}/help{tColor.reset} for available commands\n")
                    continue
            
            # Handle regular input
            if line.strip():
                prompt += line + " "
            else:
                # Empty line - check if we have a complete prompt
                if prompt.strip():
                    # Send the prompt
                    conversation_count += 1
                    answer, references = process_query(prompt.strip(), conversation_count)
                    prompt = ""
                # Continue collecting input if no prompt yet
                continue
                
        except EOFError:
            # Handle Ctrl+D gracefully
            if prompt.strip():
                conversation_count += 1
                answer, references = process_query(prompt.strip(), conversation_count)
                prompt = ""
            continue
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print(f"\n\n{tColor.yellow}👋 Session ended. Have a great day!{tColor.reset}")
            break


def show_interactive_help():
    """Show interactive mode commands."""
    print(f"\n{tColor.bold}📋 Interactive Commands:{tColor.reset}")
    print(f"  {tColor.green}/help{tColor.reset}    - Show this help message")
    print(f"  {tColor.green}/refs{tColor.reset}    - Show references from last answer")
    print(f"  {tColor.green}/clear{tColor.reset}   - Clear the screen")
    print(f"  {tColor.green}/version{tColor.reset} - Show version information")
    print(f"  {tColor.green}/quit{tColor.reset}    - Exit the program")
    print(f"\n{tColor.bold}💬 Chat Tips:{tColor.reset}")
    print(f"  • Press {tColor.aqua}Enter{tColor.reset} twice to send your question")
    print(f"  • Ask follow-up questions naturally")
    print(f"  • References are saved for each answer")
    print(f"  • Use {tColor.yellow}Ctrl+C{tColor.reset} to exit anytime\n")


def show_references(references):
    """Display references in a nice format."""
    if references:
        print(f"\n{tColor.bold}📚 REFERENCES FROM LAST ANSWER:{tColor.reset}")
        print(f"{tColor.bold}{'─' * 50}{tColor.reset}")
        for i, ref in enumerate(references[:8]):  # Show max 8 references
            name = ref.get('name', 'Unknown Source')[:60]  # Truncate long names
            url = ref.get('url', 'No URL')
            print(f"{tColor.aqua}[{i+1:2d}]{tColor.reset} {name}")
            print(f"     {tColor.blue}{url}{tColor.reset}")
        if len(references) > 8:
            print(f"     {tColor.yellow}... and {len(references)-8} more sources{tColor.reset}")
        print()
    else:
        print(f"\n{tColor.yellow}📭 No references available from the last answer.{tColor.reset}")
        print(f"   Ask a question first to see web sources!\n")


def process_query(query, count):
    """Process a user query and return the response."""
    print(f"\n{tColor.aqua}🔍 Searching the web...{tColor.reset}")
    
    try:
        # Show a simple progress indicator
        import threading
        stop_spinner = threading.Event()
        spinner_thread = threading.Thread(target=show_spinner, args=(stop_spinner,))
        spinner_thread.daemon = True
        spinner_thread.start()
        
        answer_list = list(Perplexity().generate_answer(query))
        stop_spinner.set()
        spinner_thread.join(timeout=0.1)
        
        answer, references = extract_answer_from_response(answer_list)
        
        if answer:
            print(f"\r{tColor.aqua}✅ Found answer from {len(references) if references else 0} sources{tColor.reset}")
            print(f"\n{tColor.bold}🤖 Response #{count}:{tColor.reset}")
            print(f"{tColor.bold}{'─' * 60}{tColor.reset}")
            
            # Stream the response with better formatting
            print(f"{tColor.aqua2}", end='', flush=True)
            for i, char in enumerate(answer):
                print(char, end='', flush=True)
                if i % 80 == 0 and i > 0:  # Add slight pause every 80 chars for readability
                    sleep(0.01)
                else:
                    sleep(0.005)  # Faster typing effect
            print(f"{tColor.reset}")
            
            # Show reference count
            if references:
                print(f"\n{tColor.blue}📎 {len(references)} web sources used • Type {tColor.green}/refs{tColor.reset}{tColor.blue} to view{tColor.reset}")
            
            print()  # Extra spacing
            return answer, references
        else:
            print(f"\r{tColor.red}❌ No answer received. Please try rephrasing your question.{tColor.reset}")
            print(f"   {tColor.yellow}Tip: Try being more specific or check your internet connection{tColor.reset}\n")
            return None, []
            
    except Exception as e:
        print(f"\r{tColor.red}💥 Error occurred: {str(e)}{tColor.reset}")
        print(f"   {tColor.yellow}Try again in a moment or rephrase your question{tColor.reset}\n")
        return None, []


def show_spinner(stop_event):
    """Show a simple spinner while processing."""
    spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    i = 0
    while not stop_event.is_set():
        print(f'\r{tColor.aqua}{spinner_chars[i % len(spinner_chars)]} Processing...{tColor.reset}', end='', flush=True)
        sleep(0.1)
        i += 1
    print('\r' + ' ' * 20 + '\r', end='', flush=True)  # Clear the spinner line


def main():
    """Main entry point for the CLI application."""
    try:
        # Check for version flags
        if len(sys.argv) > 1:
            arg = sys.argv[1].lower()
            if arg in ['--version', '-v', 'version']:
                show_version()
                return
            elif arg in ['--help', '-h', 'help']:
                print_help()
                return
            else:
                # Single question mode - join all arguments
                question = ' '.join(sys.argv[1:])
                answer_question(question)
                return
        
        # Interactive mode
        interactive_mode()
    except KeyboardInterrupt:
        print(f"\\n\\n{tColor.red}Goodbye!{tColor.reset}")
    except Exception as e:
        print(f"\\n{tColor.red}Unexpected error: {e}{tColor.reset}")


if __name__ == "__main__":
    main()
