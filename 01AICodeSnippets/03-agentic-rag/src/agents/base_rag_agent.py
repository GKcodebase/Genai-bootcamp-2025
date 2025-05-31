"""
Base RAG Agent that combines retrieval capabilities with agentic behavior
"""

import os
from typing import List, Dict, Any
from langchain_community.vectorstores import Chroma
from langchain_core.vectorstores import VectorStore
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

class BaseRAGAgent:
    """Base class for RAG-enabled agents"""
    
    def __init__(
        self,
        vector_store: VectorStore,
        model_name: str = "llama-3.1-8b-instant",
        temperature: float = 0.7,
        **kwargs
    ):
        """Initialize the RAG agent"""
        self.vector_store = vector_store
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = kwargs.get('max_tokens', 1024)
        self.verbose = kwargs.get('verbose', True)
        
        # Initialize components
        self.llm = self._init_llm()
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.tools = self._get_tools()
        self.agent_executor = self._create_agent()
        
    def _init_llm(self):
        """Initialize the language model"""
        return ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name=self.model_name,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
    
    def _get_tools(self) -> List[Tool]:
        """Get the list of tools for the agent"""
        return [
            Tool(
                name="search_documents",
                func=self._search_documents,
                description="Search through the document collection"
            ),
            Tool(
                name="retrieve_context",
                func=self._retrieve_context,
                description="Get more context about a specific topic"
            )
        ]
    
    def _create_agent(self):
        """Create the agent with proper prompt template"""
        prompt = PromptTemplate.from_template(
            """You are a helpful AI assistant with access to document search capabilities. 
            
            Tool Names: {tool_names}
            Tools: {tools}
            
            IMPORTANT: You must follow these steps in order:
            1. Use search_documents EXACTLY ONCE to find information
            2. Immediately provide a Final Answer using the search results
            
            Use this EXACT format:
            Question: [the input question]
            Thought: Let me search for information about this topic
            Action: search_documents
            Action Input: [concise search query]
            Observation: [search results]
            Thought: Now I can provide a complete answer based on these results
            Final Answer: [concise but comprehensive answer]
            Sources: [list the key sections used]
            
            Previous conversation history:
            {chat_history}
            
            Begin!
            
            Question: {input}
            {agent_scratchpad}"""
        )
        
        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=self.verbose,
            max_iterations=1,  # Force exactly one tool use
            early_stopping_method="force",  # Stop after max_iterations
            handle_parsing_errors=True  # Handle any parsing errors gracefully
        )
    
    def _search_documents(self, query: str) -> str:
        """Search through the document collection"""
        results = self.vector_store.similarity_search(query, k=3)
        formatted_results = []
        for i, doc in enumerate(results, 1):
            formatted_results.append(f"[Source {i}]\n{doc.page_content}\n")
        return "\n".join(formatted_results)
    
    def _retrieve_context(self, topic: str) -> str:
        """Get more context about a specific topic"""
        results = self.vector_store.similarity_search(
            topic,
            k=2,
            fetch_k=4
        )
        return "\n".join([doc.page_content for doc in results])
    
    def run(self, input_text: str) -> Dict[str, Any]:
        """Run the agent with the given input"""
        try:
            result = self.agent_executor.invoke({"input": input_text})
            return {
                "output": result["output"],
                "input": input_text,
                "sources": self._get_sources(result)
            }
        except Exception as e:
            return {
                "output": f"Error: {str(e)}",
                "input": input_text,
                "error": True
            }
    
    def _get_sources(self, result: Dict[str, Any]) -> List[str]:
        """Extract sources from the result"""
        sources = []
        if "intermediate_steps" in result:
            for step in result["intermediate_steps"]:
                if step[0].tool == "search_documents":
                    # Extract source numbers from the observation
                    observation = step[1]
                    if "Source" in observation:
                        sources.append(observation.split("Source")[1].split(":")[0].strip())
        return [f"Source {s}" for s in sources] 