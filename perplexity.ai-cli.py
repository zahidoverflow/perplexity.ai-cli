#!/usr/bin/env python3
"""
Perplexity AI CLI

A command-line interface for interacting with Perplexity AI.

Author: Fixed and improved by AI Assistant
Original: Based on HelpingAI's implementation
License: MIT
Version: 2.0.0
"""

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


def main():
    print(f"{tColor.purple}Welcome to perplexity.ai CLI!{tColor.reset} {tColor.aqua}v2.0.0{tColor.reset}")
    print("Enter/Paste your content. Enter + Ctrl-D (or Ctrl-Z in windows) to send it.")
    print("To check the references from last response, type `$refs`.")
    print()

    prompt = ""
    references = []
    
    while True:
        try:
            line = input(f" {tColor.lavand}❯{tColor.reset} ")
            if line.strip():
                prompt += line + "\\n"
            else:
                # Empty line followed by Ctrl+D will send the prompt
                pass
        except EOFError:
            # Ctrl+D pressed
            if not prompt.strip():
                continue
                
            prompt = prompt.strip()
            
            if "$refs" in prompt:
                refs = ""
                for i, ref in enumerate(references):
                    refs += f"[^{i+1}]: [{ref['name']}]({ref['url']})\\n"
                print(f"\\nREFERENCES:\\n{refs}")
                prompt = ""
                continue

            # Generate a response using the Perplexity AI
            try:
                answer_list = list(Perplexity().generate_answer(prompt))
                answer, references = extract_answer_from_response(answer_list)
                
                if answer:
                    print(tColor.aqua2, end='\\n', flush=True)
                    for char in answer:
                        print(char, end='', flush=True)
                        sleep(0.02)
                    print(tColor.reset, end='\\n\\n', flush=True)
                else:
                    print(f"{tColor.red}No answer received. Try again.{tColor.reset}\\n")
                    
            except Exception as e:
                print(f"{tColor.red}Error: {e}{tColor.reset}\\n")
            
            prompt = ""


def show_version():
    print(f"{tColor.purple}Perplexity AI CLI{tColor.reset} {tColor.aqua}v2.0.0{tColor.reset}")
    print("A command-line interface for Perplexity AI")
    print("License: MIT")
    print("Repository: https://github.com/zahidoverflow/perplexity.ai-cli")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        try:
            main()
        except KeyboardInterrupt:
            exit(f"\\n\\n{tColor.red}Aborting!{tColor.reset}")
    elif len(sys.argv) == 2:
        if sys.argv[1] in ['-v', '--version', 'version']:
            show_version()
        else:
            quick_question()
    else:
        print(f"{tColor.red}Usage:{tColor.reset}")
        print(f"  {sys.argv[0]}                    # Interactive mode")
        print(f"  {sys.argv[0]} \"question\"         # Quick query")
        print(f"  {sys.argv[0]} --version          # Show version")
