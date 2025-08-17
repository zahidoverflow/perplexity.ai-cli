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
import signal
import readline


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


def get_multiline_input(prompt_text):
    """Get input with Enter to send, Shift+Enter/Ctrl+Enter for new lines."""
    import sys
    import tty
    import termios
    
    print(f"{tColor.bold}╭──────────────────────────────────────────────────────────────────────────────╮{tColor.reset}")
    print(f"{tColor.bold}│{tColor.reset}  {tColor.aqua}>{tColor.reset} ", end='', flush=True)
    
    lines = []
    current_line = ""
    
    # Save terminal settings
    old_settings = termios.tcgetattr(sys.stdin)
    
    try:
        while True:
            try:
                # Use regular input for simplicity - we'll handle Enter logic differently
                user_input = input()
                
                # Check if input ends with special sequence for newline
                if user_input.endswith('\\n') or user_input.endswith('\\\\'):
                    # Remove the escape sequence and add as new line
                    current_line = user_input.rstrip('\\n').rstrip('\\\\')
                    lines.append(current_line)
                    current_line = ""
                    print(f"{tColor.bold}│{tColor.reset}    ", end='', flush=True)  # Continue on next line in box
                    continue
                else:
                    # Regular input - this will be sent
                    if current_line:
                        current_line += " " + user_input
                    else:
                        current_line = user_input
                    
                    if current_line.strip():
                        lines.append(current_line)
                        break
                    
            except KeyboardInterrupt:
                raise
            except EOFError:
                if current_line.strip():
                    lines.append(current_line)
                    break
                continue
                
    finally:
        # Restore terminal settings
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    
    print(f"{tColor.bold}╰──────────────────────────────────────────────────────────────────────────────╯{tColor.reset}")
    print()
    
    return "\\n".join(lines) if lines else ""


def interactive_mode():
    """Run the CLI in enhanced interactive mode."""
    # Setup signal handling for cleaner Ctrl+C experience
    ctrl_c_count = 0
    last_ctrl_c_time = 0
    
    def signal_handler(signum, frame):
        nonlocal ctrl_c_count, last_ctrl_c_time
        current_time = time()
        
        # Reset counter if more than 5 seconds have passed
        if current_time - last_ctrl_c_time > 5:
            ctrl_c_count = 0
        
        ctrl_c_count += 1
        last_ctrl_c_time = current_time
        
        if ctrl_c_count == 1:
            print(f"\r{' ' * 50}\r", end='', flush=True)  # Clear any ^C characters
            print(f"{tColor.yellow}🛑 Press Ctrl+C again to exit.{tColor.reset}")
            print(f"{tColor.lavand}❯{tColor.reset} ", end='', flush=True)
        else:
            print(f"\r{' ' * 80}\r", end='', flush=True)  # Clear the warning message line
            print(f"\r{tColor.yellow}🛑 Session ended. Have a great day!{tColor.reset}")
            print(f"{tColor.bold}╰──────────────────────────────────────────────────────────────────────────────╯{tColor.reset}")
            sys.exit(0)
    
    # Set up the signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    # Display beautiful ASCII art banner
    print(f"\n{tColor.purple}")
    print("██████╗ ███████╗██████╗ ██████╗ ██╗     ███████╗██╗  ██╗██╗████████╗██╗   ██╗")
    print("██╔══██╗██╔════╝██╔══██╗██╔══██╗██║     ██╔════╝╚██╗██╔╝██║╚══██╔══╝╚██╗ ██╔╝")
    print("██████╔╝█████╗  ██████╔╝██████╔╝██║     █████╗   ╚███╔╝ ██║   ██║    ╚████╔╝ ")
    print("██╔═══╝ ██╔══╝  ██╔══██╗██╔═══╝ ██║     ██╔══╝   ██╔██╗ ██║   ██║     ╚██╔╝  ")
    print("██║     ███████╗██║  ██║██║     ███████╗███████╗██╔╝ ██╗██║   ██║      ██║   ")
    print("╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝      ╚═╝   ")
    print(f"{tColor.reset}")
    
    print(f"{tColor.aqua}                    🔍 Web-Search Powered AI CLI {tColor.purple}v{__version__}{tColor.reset}")
    print()
    
    # Show tips like gemini-cli
    print(f"{tColor.bold}Tips for getting started:{tColor.reset}")
    print(f"1. Ask questions and get web-sourced answers instantly.")
    print(f"2. Press {tColor.green}Enter{tColor.reset} to send your question.")
    print(f"3. Use {tColor.yellow}\\\\n{tColor.reset} at the end of line for new lines (advanced).")
    print(f"4. /help for more commands and information.")
    print()

    references = []
    conversation_count = 0
    
    while True:
        try:
            # Reset Ctrl+C counter on new input
            ctrl_c_count = 0
            
            # Get user input with modern behavior
            line = get_multiline_input("")
                
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
                # Send the prompt immediately
                conversation_count += 1
                answer, references = process_query(line.strip(), conversation_count)
                
        except EOFError:
            continue
        except KeyboardInterrupt:
            # This should not be reached due to signal handler, but keep as fallback
            continue


def show_interactive_help():
    """Show interactive mode commands."""
    print(f"\n{tColor.bold}📋 Interactive Commands:{tColor.reset}")
    print(f"  {tColor.green}/help{tColor.reset}    - Show this help message")
    print(f"  {tColor.green}/refs{tColor.reset}    - Show references from last answer")
    print(f"  {tColor.green}/clear{tColor.reset}   - Clear the screen")
    print(f"  {tColor.green}/version{tColor.reset} - Show version information")
    print(f"  {tColor.green}/quit{tColor.reset}    - Exit the program")
    print(f"\n{tColor.bold}💬 Input Tips:{tColor.reset}")
    print(f"  • Press {tColor.aqua}Enter{tColor.reset} to send your question")
    print(f"  • Use {tColor.yellow}\\\\n{tColor.reset} at end of line for multiline input")
    print(f"  • Ask follow-up questions naturally")
    print(f"  • References are saved for each answer")
    print(f"  • Press {tColor.yellow}Ctrl+C{tColor.reset} twice (within 5s) to exit safely\n")


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
            # Clear the search messages before showing response
            print(f"\r{' ' * 50}\r", end='', flush=True)  # Clear current line
            print(f"\033[A\r{' ' * 50}\r", end='', flush=True)  # Clear previous line (Searching...)
            print(f"\033[A\r{' ' * 50}\r\033[B", end='', flush=True)  # Clear empty line and return
            
            # Clean response display without search messages
            print(f" {tColor.purple}✦{tColor.reset} {tColor.bold}Response{tColor.reset}")
            print()
            
            # Stream the response with better formatting
            print(f"  {tColor.aqua2}", end='', flush=True)
            for i, char in enumerate(answer):
                print(char, end='', flush=True)
                sleep(0.005)  # Faster typing effect
            print(f" {tColor.reset}")
            print()
            
            # Show reference count
            if references:
                print(f"{tColor.blue}📎 {len(references)} web sources used • Type {tColor.green}/refs{tColor.reset}{tColor.blue} to view{tColor.reset}")
            
            print()  # Extra spacing
            return answer, references
        else:
            # Clear the search messages before showing error
            print(f"\r{' ' * 50}\r", end='', flush=True)  # Clear current line
            print(f"\033[A\r{' ' * 50}\r", end='', flush=True)  # Clear previous line (Searching...)
            print(f"\033[A\r{' ' * 50}\r\033[B", end='', flush=True)  # Clear empty line and return
            
            print(f"{tColor.red}❌ No answer received. Please try rephrasing your question.{tColor.reset}")
            print(f"   {tColor.yellow}Tip: Try being more specific or check your internet connection{tColor.reset}\n")
            return None, []
            
    except Exception as e:
        # Clear the search messages before showing error
        print(f"\r{' ' * 50}\r", end='', flush=True)  # Clear current line
        print(f"\033[A\r{' ' * 50}\r", end='', flush=True)  # Clear previous line (Searching...)
        print(f"\033[A\r{' ' * 50}\r\033[B", end='', flush=True)  # Clear empty line and return
        
        print(f"{tColor.red}💥 Error occurred: {str(e)}{tColor.reset}")
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
        # This handles Ctrl+C in non-interactive modes
        print(f"\n{tColor.yellow}👋 Goodbye!{tColor.reset}")
    except Exception as e:
        print(f"\n{tColor.red}Unexpected error: {e}{tColor.reset}")


if __name__ == "__main__":
    main()
