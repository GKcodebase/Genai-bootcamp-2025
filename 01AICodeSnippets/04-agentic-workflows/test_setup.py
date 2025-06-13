from src.workflows import ResearchWorkflow
from dotenv import load_dotenv
import os

def test_setup():
    """Test the basic setup and environment variables."""
    # Load environment variables
    load_dotenv()
    
    # Verify environment variables
    required_vars = ['GROQ_API_KEY', 'ANTHROPIC_API_KEY', 'GOOGLE_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Missing required environment variables:", missing_vars)
        return False
    else:
        print("✅ Environment variables loaded successfully")
    
    try:
        # Initialize research workflow
        workflow = ResearchWorkflow(
            model_name="llama-3.1-8b-instant",
            temperature=0.7
        )
        print("✅ Workflow initialization successful")
        return True
    except Exception as e:
        print("❌ Error initializing workflow:", str(e))
        return False

def test_research_execution():
    """Test the research workflow execution."""
    try:
        # Initialize research workflow
        research = ResearchWorkflow(
            model_name="llama-3.1-8b-instant",
            temperature=0.7
        )
        print("✅ Workflow initialization successful")
        
        # Execute research
        results = research.execute_research("AI Safety and Ethics")
        print("✅ Research execution successful")
        print("\nResearch Results:")
        print("----------------")
        print(results.get('synthesis', 'No synthesis available'))
        return True
    except Exception as e:
        print("❌ Error executing research:", str(e))
        return False

if __name__ == "__main__":
    print("Testing project setup...")
    setup_success = test_setup()
    
    if setup_success:
        print("\n✅ Project setup verified successfully!")
        print("\nTesting research execution...")
        research_success = test_research_execution()
        if research_success:
            print("\n✅ All tests completed successfully!")
        else:
            print("\n❌ Research execution test failed.")
    else:
        print("\n❌ Project setup verification failed. Please check the errors above.") 