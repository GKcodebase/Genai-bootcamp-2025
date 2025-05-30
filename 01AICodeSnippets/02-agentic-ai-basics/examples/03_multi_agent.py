import sys
import argparse
from src.agents.research_agent import ResearchAgent
from src.agents.calculator_agent import CalculatorAgent

def main():
    parser = argparse.ArgumentParser(description='Multi-Agent System - Research and Calculator')
    parser.add_argument('--mode', choices=['research', 'calculate', 'both'], default='both',
                       help='Choose agent mode')
    parser.add_argument('--query', help='Research query or calculation expression')
    parser.add_argument('--interactive', '-i', action='store_true', help='Interactive mode')
    
    args = parser.parse_args()
    
    # Initialize agents
    research_agent = ResearchAgent()
    calculator_agent = CalculatorAgent()
    
    if args.interactive:
        print("\n🤖 Multi-Agent Interactive Mode")
        print("=" * 40)
        print("Commands:")
        print("  research: <topic> - Research a topic")
        print("  calculate: <expression> - Calculate expression")
        print("  quit - Exit")
        print("-" * 40)
        
        while True:
            try:
                user_input = input("\n🎯 Enter command: ").strip()
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if user_input.startswith('research:'):
                    topic = user_input[9:].strip()
                    if topic:
                        print(f"\n🔍 Researching: {topic}")
                        result = research_agent.run(f"Research and summarize: {topic}")
                        print(f"✅ {result['output']}")
                
                elif user_input.startswith('calculate:'):
                    expression = user_input[10:].strip()
                    if expression:
                        print(f"\n🔢 Calculating: {expression}")
                        result = calculator_agent.run(f"Calculate: {expression}")
                        print(f"✅ {result['output']}")
                
                else:
                    print("❌ Invalid command. Use 'research: <topic>' or 'calculate: <expression>'")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")
        return
    
    # Single query mode
    if args.query:
        if args.mode == 'research':
            print(f"\n🔍 Researching: {args.query}")
            result = research_agent.run(args.query)
            print(f"✅ {result['output']}")
            
        elif args.mode == 'calculate':
            print(f"\n🔢 Calculating: {args.query}")
            result = calculator_agent.run(f"Calculate: {args.query}")
            print(f"✅ {result['output']}")
            
        elif args.mode == 'both':
            # Try to determine if it's a math expression or research topic
            if any(op in args.query for op in ['+', '-', '*', '/', '(', ')', 'sqrt', 'sin', 'cos', 'log']):
                print(f"\n🔢 Detected calculation: {args.query}")
                result = calculator_agent.run(f"Calculate: {args.query}")
                print(f"✅ {result['output']}")
            else:
                print(f"\n🔍 Detected research topic: {args.query}")
                result = research_agent.run(args.query)
                print(f"✅ {result['output']}")
    else:
        parser.print_help()
        print("\n💡 Examples:")
        print("  python examples/03_multi_agent.py --query 'quantum computing'")
        print("  python examples/03_multi_agent.py --mode calculate --query '2+2*3'")
        print("  python examples/03_multi_agent.py --interactive")

if __name__ == "__main__":
    main() 