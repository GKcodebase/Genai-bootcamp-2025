import sys
import argparse
from src.agents.calculator_agent import CalculatorAgent

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Calculator Agent - AI-powered mathematical assistant')
    parser.add_argument('expression', nargs='*', help='Mathematical expression to calculate')
    parser.add_argument('--interactive', '-i', action='store_true', help='Start in interactive mode')
    parser.add_argument('--help-math', metavar='TOPIC', help='Get help with mathematical topics')
    
    args = parser.parse_args()
    
    # Create calculator agent
    agent = CalculatorAgent()
    
    # Handle math help
    if args.help_math:
        task = f"Help me understand {args.help_math} in mathematics"
        print(f"\n📚 Math Help: {args.help_math}")
        print("=" * 50)
        
        try:
            result = agent.run(task)
            print(result['output'])
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        return
    
    # Handle interactive mode
    if args.interactive:
        print("\n🧮 Calculator Agent - Interactive Mode")
        print("=" * 40)
        print("Enter mathematical expressions or 'quit' to exit")
        print("Examples: 2+2, sqrt(16), sin(pi/2), log(10)")
        print("-" * 40)
        
        while True:
            try:
                expression = input("\n🔢 Enter calculation: ").strip()
                if expression.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                if not expression:
                    continue
                
                task = f"Calculate this mathematical expression: {expression}"
                result = agent.run(task)
                print(f"✅ {result['output']}")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")
        return
    
    # Handle single calculation
    if args.expression:
        expression = ' '.join(args.expression)
        task = f"Calculate this mathematical expression and explain the result: {expression}"
        
        print(f"\n🔢 Calculating: {expression}")
        print("=" * 50)
        
        try:
            result = agent.run(task)
            print("\n✅ Calculation Results:")
            print("-" * 30)
            print(result['output'])
            
        except Exception as e:
            print(f"\n❌ Error occurred: {str(e)}")
            sys.exit(1)
    else:
        # Show help if no arguments provided
        parser.print_help()
        print("\n💡 Examples:")
        print("  python examples/02_calculator_agent.py '2 + 2'")
        print("  python examples/02_calculator_agent.py 'sqrt(16) * 3'")
        print("  python examples/02_calculator_agent.py --interactive")
        print("  python examples/02_calculator_agent.py --help-math trigonometry")

if __name__ == "__main__":
    main() 