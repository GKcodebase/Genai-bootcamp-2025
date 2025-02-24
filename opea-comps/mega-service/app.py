# Import necessary libraries
import json
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse
from comps.cores.proto.api_protocol import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionResponseChoice,
    ChatMessage,
    UsageInfo
)
from comps.cores.mega.constants import ServiceType, ServiceRoleType
from comps import MicroService, ServiceOrchestrator
import os
import aiohttp
from comps.cores.mega.utils import handle_message
from comps.cores.proto.docarray import LLMParams

# Initialize FastAPI application
app = FastAPI()

# Environment variables for service configuration
EMBEDDING_SERVICE_HOST_IP = os.getenv("EMBEDDING_SERVICE_HOST_IP", "0.0.0.0")
EMBEDDING_SERVICE_PORT = os.getenv("EMBEDDING_SERVICE_PORT", 6000)
LLM_SERVICE_HOST_IP = os.getenv("LLM_SERVICE_HOST_IP", "0.0.0.0")
LLM_SERVICE_PORT = os.getenv("LLM_SERVICE_PORT", 9000)


class ExampleService:
    """Main service class for handling LLM interactions"""
    def __init__(self, host="0.0.0.0", port=8000):
        # Initialize service with default host and port
        self.host = host
        self.port = port
        self.endpoint = "/v1/example-service"
        self.megaservice = ServiceOrchestrator()
        os.environ["LOGFLAG"] = "true"  # Enable detailed logging

    async def check_ollama_connection(self):
        """Verify connection to Ollama LLM service"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"http://{LLM_SERVICE_HOST_IP}:{LLM_SERVICE_PORT}/api/tags"
                print(f"\nTesting Ollama connection to: {url}")
                async with session.get(url) as response:
                    print(f"Ollama check status: {response.status}")
                    if response.status == 200:
                        models = await response.json()
                        print(f"Available models: {models}")
                    return response.status == 200
        except Exception as e:
            print(f"Failed to connect to Ollama: {e}")
            return False

    def add_remote_service(self):
        """Configure and add LLM service to the orchestrator"""
        llm = MicroService(
            name="llm",
            host=LLM_SERVICE_HOST_IP,
            port=LLM_SERVICE_PORT,
            endpoint="/v1/chat/completions",
            use_remote_service=True,
            service_type=ServiceType.LLM,
        )
        # Log LLM service configuration
        print(f"\nConfiguring LLM service:")
        print(f"- Host: {LLM_SERVICE_HOST_IP}")
        print(f"- Port: {LLM_SERVICE_PORT}")
        print(f"- Endpoint: {llm.endpoint}")
        print(f"- Full URL: http://{LLM_SERVICE_HOST_IP}:{LLM_SERVICE_PORT}{llm.endpoint}")
        self.megaservice.add(llm)

    async def handle_request(self, request: Request):
        """Process incoming chat completion requests"""
        # Parse request data
        data = await request.json()
        print("\n\ndata:\n", data)
        stream_opt = data.get("stream", True)
        print("\n\nstream_opt:\n", stream_opt)
        chat_request = ChatCompletionRequest.model_validate(data)
        print("\n\nchat_request:\n", chat_request)

        # Configure LLM parameters with defaults if not provided
        parameters = LLMParams(
            max_tokens=chat_request.max_tokens if chat_request.max_tokens else 1024,
            top_k=chat_request.top_k if chat_request.top_k else 10,
            top_p=chat_request.top_p if chat_request.top_p else 0.95,
            temperature=chat_request.temperature if chat_request.temperature else 0.01,
            frequency_penalty=chat_request.frequency_penalty if chat_request.frequency_penalty else 0.0,
            presence_penalty=chat_request.presence_penalty if chat_request.presence_penalty else 0.0,
            repetition_penalty=chat_request.repetition_penalty if chat_request.repetition_penalty else 1.03,
            stream=stream_opt,
            model=chat_request.model,
            chat_template=chat_request.chat_template if chat_request.chat_template else None,
        )

        # Prepare input for LLM
        initial_inputs = {
            "messages": chat_request.messages,
        }
        print("\n\n\n\nPAYLOAD:\n")
        print(json.dumps(initial_inputs))
        print("\n\n\n\n")

        # Process request through service orchestrator
        result_dict, runtime_graph = await self.megaservice.schedule(
            initial_inputs=initial_inputs,
            llm_parameters=parameters
        )

        # Handle streaming responses
        print("\n\nresult_dict:\n", result_dict)
        for node, response in result_dict.items():
            if isinstance(response, StreamingResponse):
                print("\n\nStreaming response:", response)
                return response

        # Handle non-streaming responses
        print("\n\nNo streaming response")
        print("runtime_graph:\n", runtime_graph)
        last_node = runtime_graph.all_leaves()[-1]
        print("last_node:\n", last_node)

        # Process the result and handle errors
        if last_node in result_dict:
            service_result = result_dict[last_node]

            # Parse OpenAI-style response format
            if isinstance(service_result, dict):
                if 'choices' in service_result and len(service_result['choices']) > 0:
                    message = service_result['choices'][0].get('message', {})
                    response = message.get('content', '')
                elif 'error' in service_result:
                    error = service_result['error']
                    error_msg = error.get('message', 'Unknown error')
                    error_type = error.get('type', 'internal_error')
                    raise HTTPException(
                        status_code=400 if error_type == 'invalid_request_error' else 500,
                        detail=error_msg
                    )
                else:
                    print(f"Unexpected response format: {service_result}")
                    raise HTTPException(
                        status_code=500,
                        detail="Unexpected response format from LLM service"
                    )
            else:
                response = service_result
        else:
            print(f"No result found for node {last_node}")
            raise HTTPException(
                status_code=500,
                detail="No response received from LLM service"
            )

        # Format and return final response
        print("\n\n not a streaming response:\n", response)
        choices = []
        usage = UsageInfo()

        choices.append(
            ChatCompletionResponseChoice(
                index=0,
                message=ChatMessage(role="assistant", content=response),
                finish_reason="stop",
            )
        )
        return JSONResponse(content=ChatCompletionResponse(model="chatqna", choices=choices, usage=usage).dict())


# Initialize service and add remote LLM service
example_service = ExampleService()
example_service.add_remote_service()

# Define FastAPI endpoint
@app.post("/v1/example-service")
async def handle_request(request: Request):
    """FastAPI endpoint for handling chat completion requests"""
    return await example_service.handle_request(request)