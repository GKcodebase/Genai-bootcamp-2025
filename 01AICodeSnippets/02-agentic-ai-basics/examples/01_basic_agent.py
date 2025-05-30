import sys
import argparse
from src.agents.research_agent import ResearchAgent

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Research Agent - AI-powered research assistant')
    parser.add_argument('query', nargs='*', help='Research topic or question (if not provided, will use default)')
    parser.add_argument('--default', action='store_true', help='Use default research topic')
    
    args = parser.parse_args()
    
    # Create research agent
    agent = ResearchAgent()
    
    # Determine the research task
    if args.query:
        task = ' '.join(args.query)
    elif args.default:
        task = "Research and summarize the latest developments in quantum computing"
    else:
        # Interactive mode if no arguments provided
        task = input("Enter your research topic: ").strip()
        if not task:
            task = "Research and summarize the latest developments in quantum computing"
    
    print(f"\n🔍 Researching: {task}")
    print("=" * 50)
    
    # Run the agent
    try:
        result = agent.run(task)
        
        # Print results
        print("\n✅ Research Results:")
        print("-" * 30)
        print(result['output'])
        
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 