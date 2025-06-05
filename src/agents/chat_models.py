import requests

from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Any, Dict, Iterator, List, Mapping, Optional

from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
from langchain_core.outputs import GenerationChunk

from utils.getsecret import get



class CustomLLM(LLM):
    """A custom chat model that uses my custom logic to generate responses."""
    def _call(
        self,
        prompt: str,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Run the LLM on the given input.
        Args:
            prompt: The prompt to generate from
                If stop tokens are not supported consider raising NotImplementedError.
            run_manager: Callback manager for the run.
            **kwargs: Arbitrary additional keyword arguments. These are usually passed
                to the model provider API call.
        Returns:
            The model output as a string. Actual completions SHOULD NOT include the prompt.
        """
        url = "https://genai-manager.onrender.com/query"

        payload = {"query": prompt}
        headers = {
        'accept': 'application/json',
        'x-api-key': get("CUSTOM_SERVER_API")
        }        
        response = requests.get(url, headers=headers, params=payload)
        if response.status_code != 200:
            raise ValueError(f"Error from custom LLM server: {response.text}")
        return response.text

    def _stream(
        self,
        prompt: str,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[GenerationChunk]:
        """Stream the LLM on the given prompt.

        This method should be overridden by subclasses that support streaming.

        If not implemented, the default behavior of calls to stream will be to
        fallback to the non-streaming version of the model and return
        the output as a single chunk.

        Args:
            prompt: The prompt to generate from.
            run_manager: Callback manager for the run.
            **kwargs: Arbitrary additional keyword arguments. These are usually passed
                to the model provider API call.

        Returns:
            An iterator of GenerationChunks.
        """
        for char in prompt[: self.n]:
            chunk = GenerationChunk(text=char)
            if run_manager:
                run_manager.on_llm_new_token(chunk.text, chunk=chunk)

            yield chunk

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Return a dictionary of identifying parameters."""
        return {
            # The model name allows users to specify custom token counting
            # rules in LLM monitoring applications (e.g., in LangSmith users
            # can provide per token pricing for their model and monitor
            # costs for the given LLM.)
            "model_name": "CustomLLM Jugaad",
        }

    @property
    def _llm_type(self) -> str:
        """Get the type of language model used by this chat model. Used for logging purposes only."""
        return "CustomLLM"

# Custom LLM instance
custom_model = CustomLLM()
# Google Gemini models
gemini = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
gemini_strict = ChatGoogleGenerativeAI(model="gemini-2.0-flash",temperature=0)
