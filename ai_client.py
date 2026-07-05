import os
import openai
from openai import OpenAI

class AIClient:
    """
    OpenRouter API Wrapper for Mohith AI Assistant (using OpenAI Python SDK)
    """

    def __init__(self, api_key: str):
        # Step 3 & 13: Sanitize key input
        if api_key:
            api_key = str(api_key).strip()
            if api_key.lower() in ("none", ""):
                api_key = None
                
        self.api_key = api_key

        # Step 7: Add masked debugging output
        if self.api_key:
            masked_key = self.api_key[:12] + "..." if len(self.api_key) > 12 else self.api_key
            print("Key Loaded:", masked_key)
            
            # Step 4 & 14: Initialize OpenAI client pointing to OpenRouter API (reusing connection pool)
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://openrouter.ai/api/v1",
                default_headers={
                    "HTTP-Referer": "http://localhost:8501",
                    "X-Title": "Mohith AI Assistant",
                }
            )
        else:
            print("OPENROUTER_API_KEY not found")
            self.client = None

    def is_configured(self):
        return self.client is not None

    def validate_api_key(self):
        # Step 8: Return "Valid" or "Invalid" instead of crashing
        if not self.client:
            return "Invalid"
        try:
            # Performs a lightweight list models request
            self.client.models.list()
            return "Valid"
        except Exception:
            return "Invalid"

    def generate_chat_response(
        self,
        messages,
        model="meta-llama/llama-3.3-8b-instruct:free",
        temperature=0.7,
        max_tokens=2048,
    ):
        # Step 7: If the key is None show OPENROUTER_API_KEY not found instead of calling the API
        if not self.client:
            raise Exception("OPENROUTER_API_KEY not found. Please set your key in Settings or .env file.")

        # Clean messages & optimize context size (keep latest 10 messages)
        optimized_messages = []
        for msg in messages:
            optimized_messages.append({
                "role": msg["role"],
                "content": msg["content"].strip()
            })

        if len(optimized_messages) > 10:
            system_msg = None
            if optimized_messages[0]["role"] == "system":
                system_msg = optimized_messages[0]
                history = optimized_messages[1:]
            else:
                history = optimized_messages
            
            history = history[-10:]
            if system_msg:
                optimized_messages = [system_msg] + history
            else:
                optimized_messages = history

        try:
            # Step 6: API request format
            response = self.client.chat.completions.create(
                model=model,
                messages=optimized_messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except openai.AuthenticationError:
            raise Exception("Invalid API Key (401 Unauthorized). Please check your OpenRouter API Key.")
        except openai.PermissionDeniedError:
            raise Exception("Access Denied (403 Forbidden). Check account balance, permissions, or routing rules.")
        except openai.NotFoundError:
            raise Exception(f"Model Not Found (404 Not Found). The model '{model}' could not be located on OpenRouter.")
        except openai.APITimeoutError:
            raise Exception("Request Timeout (408 Request Timeout). The server did not respond in time.")
        except openai.RateLimitError:
            raise Exception("Rate limit exceeded (429 Too Many Requests). Please wait a moment before trying again.")
        except openai.InternalServerError:
            raise Exception("OpenRouter Server Error (500 Internal Server Error). Please try again later.")
        except Exception as e:
            raise Exception(f"OpenRouter API Error: {str(e)}")

    def generate_chat_response_stream(
        self,
        messages,
        model="meta-llama/llama-3.3-8b-instruct:free",
        temperature=0.7,
        max_tokens=2048,
    ):
        # Step 7: If the key is None show OPENROUTER_API_KEY not found instead of calling the API
        if not self.client:
            raise Exception("OPENROUTER_API_KEY not found. Please set your key in Settings or .env file.")

        # Clean messages & optimize context size (keep latest 10 messages)
        optimized_messages = []
        for msg in messages:
            optimized_messages.append({
                "role": msg["role"],
                "content": msg["content"].strip()
            })

        if len(optimized_messages) > 10:
            system_msg = None
            if optimized_messages[0]["role"] == "system":
                system_msg = optimized_messages[0]
                history = optimized_messages[1:]
            else:
                history = optimized_messages
            
            history = history[-10:]
            if system_msg:
                optimized_messages = [system_msg] + history
            else:
                optimized_messages = history

        try:
            # Step 6: API request format with stream=True
            stream = self.client.chat.completions.create(
                model=model,
                messages=optimized_messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            for chunk in stream:
                yield chunk
        except openai.AuthenticationError:
            raise Exception("Invalid API Key (401 Unauthorized). Please check your OpenRouter API Key.")
        except openai.PermissionDeniedError:
            raise Exception("Access Denied (403 Forbidden). Check account balance, permissions, or routing rules.")
        except openai.NotFoundError:
            raise Exception(f"Model Not Found (404 Not Found). The model '{model}' could not be located on OpenRouter.")
        except openai.APITimeoutError:
            raise Exception("Request Timeout (408 Request Timeout). The server did not respond in time.")
        except openai.RateLimitError:
            raise Exception("Rate limit exceeded (429 Too Many Requests). Please wait a moment before trying again.")
        except openai.InternalServerError:
            raise Exception("OpenRouter Server Error (500 Internal Server Error). Please try again later.")
        except Exception as e:
            raise Exception(f"OpenRouter API Error: {str(e)}")