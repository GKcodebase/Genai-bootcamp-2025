import sys
import argparse
from src.agents.research_agent import ResearchAgent
from src.memory.simple_memory import SimpleMemory
from src.utils.error_handler import retry_on_error

@retry_on_error(max_attempts=3)
def run_research_task(agent: ResearchAgent, task: str, memory: SimpleMemory):
    # Execute the task
    result = agent.run(task)
    
    # Store in memory
    memory.add_to_short_term(result['output'])
    memory.add_to_long_term(task, result['output'])
    
    return result

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Advanced Research Agent with Memory - AI-powered research assistant')
    parser.add_argument('query', nargs='*', help='Research topic or question')
    parser.add_argument('--detailed', '-d', action='store_true', 
                       help='Perform detailed research with multiple aspects')
    parser.add_argument('--memory', '-m', action='store_true',
                       help='Show memory contents after research')
    parser.add_argument('--save', '-s', metavar='FILENAME',
                       help='Save research results to a file')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='Start interactive research mode')
    
    args = parser.parse_args()
    
    # Initialize components
    agent = ResearchAgent()
    memory = SimpleMemory()
    
    # Handle interactive mode
    if args.interactive:
        print("\n🔬 Interactive Research Mode")
        print("=" * 40)
        print("Enter research topics or 'quit' to exit")
        print("Commands:")
        print("  research <topic> - Research a topic")
        print("  memory - Show memory contents")
        print("  clear - Clear memory")
        print("  quit - Exit")
        print("-" * 40)
        
        while True:
            try:
                user_input = input("\n🔍 Research prompt: ").strip()
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if user_input.lower() == 'memory':
                    print("\n📚 Memory Contents:")
                    short_term = memory.get_short_term_memory()
                    if short_term:
                        for i, item in enumerate(short_term, 1):
                            print(f"{i}. {item['timestamp']}: {item['content'][:100]}...")
                    else:
                        print("No items in memory.")
                    continue
                
                if user_input.lower() == 'clear':
                    memory.short_term.clear()
                    memory.long_term.clear()
                    print("✅ Memory cleared!")
                    continue
                
                if not user_input:
                    continue
                
                # Remove 'research' prefix if present
                if user_input.lower().startswith('research '):
                    user_input = user_input[9:].strip()
                
                print(f"\n🔍 Researching: {user_input}")
                print("=" * 50)
                
                result = run_research_task(agent, user_input, memory)
                print("\n✅ Research Results:")
                print("-" * 30)
                print(result['output'])
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")
        return
    
    # Determine the research task
    if args.query:
        task = ' '.join(args.query)
    else:
        # Show help if no query provided
        parser.print_help()
        print("\n💡 Examples:")
        print("  python examples/02_research_agent.py 'quantum computing'")
        print("  python examples/02_research_agent.py --detailed 'artificial intelligence ethics'")
        print("  python examples/02_research_agent.py --interactive")
        print("  python examples/02_research_agent.py 'blockchain' --save research_results.txt")
        return
    
    # Modify task based on flags
    if args.detailed:
        task = f"""
        Research and provide a comprehensive analysis on:
        Topic: {task}
        
        Please include:
        1. Overview and current state
        2. Latest developments and trends
        3. Key players and companies
        4. Challenges and opportunities
        5. Future implications
        """
    
    print(f"\n🔍 Researching: {task}")
    print("=" * 50)
    
    # Run the research
    try:
        result = run_research_task(agent, task, memory)
        
        print("\n✅ Research Results:")
        print("-" * 30)
        print(result['output'])
        
        # Save to file if requested
        if args.save:
            try:
                with open(args.save, 'w', encoding='utf-8') as f:
                    f.write(f"Research Topic: {task}\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(result['output'])
                    f.write(f"\n\nGenerated on: {memory.get_short_term_memory()[-1]['timestamp']}")
                print(f"\n💾 Results saved to: {args.save}")
            except Exception as e:
                print(f"\n❌ Failed to save file: {str(e)}")
        
        # Show memory contents if requested
        if args.memory:
            print("\n📚 Short-term Memory Contents:")
            print("-" * 30)
            for i, item in enumerate(memory.get_short_term_memory(), 1):
                print(f"{i}. {item['timestamp']}: {item['content'][:100]}...")
                
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 