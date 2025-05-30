from typing import List, Dict
from .base_agent import BaseAgent
import math
import re

class CalculatorAgent(BaseAgent):
    def _get_default_tools(self) -> List[Dict]:
        return [
            {
                "name": "calculator",
                "description": "Useful for performing mathematical calculations. Supports basic arithmetic, trigonometry, logarithms, and more.",
                "func": self._calculate
            },
            {
                "name": "math_help",
                "description": "Get help with mathematical concepts and formulas",
                "func": self._math_help
            }
        ]
    
    def _calculate(self, expression: str) -> str:
        """Safely evaluate mathematical expressions"""
        try:
            # Remove any non-mathematical characters for safety
            expression = expression.strip()
            
            # Replace common math terms with Python equivalents
            expression = expression.replace('^', '**')  # Power operator
            expression = expression.replace('π', 'math.pi')
            expression = expression.replace('pi', 'math.pi')
            expression = expression.replace('e', 'math.e')
            
            # Define safe functions and constants
            safe_dict = {
                "abs": abs, "round": round, "min": min, "max": max,
                "pow": pow, "math": math, "sqrt": math.sqrt,
                "sin": math.sin, "cos": math.cos, "tan": math.tan,
                "log": math.log, "log10": math.log10, "exp": math.exp,
                "pi": math.pi, "e": math.e
            }
            
            # Check for dangerous operations
            if any(dangerous in expression.lower() for dangerous in ['import', 'exec', 'eval', '__']):
                return "Error: Unsafe expression detected"
            
            # Evaluate the expression
            result = eval(expression, {"__builtins__": {}}, safe_dict)
            return f"Result: {result}"
            
        except Exception as e:
            return f"Calculation error: {str(e)}"
    
    def _math_help(self, topic: str) -> str:
        """Provide help with mathematical concepts"""
        help_topics = {
            "trigonometry": "Common trig functions: sin(x), cos(x), tan(x). Remember angles are in radians!",
            "logarithms": "log(x) = natural log, log10(x) = base-10 log, exp(x) = e^x",
            "constants": "Available constants: pi (π ≈ 3.14159), e ≈ 2.71828",
            "operations": "Basic: +, -, *, /, **  Advanced: sqrt(), abs(), round()",
            "examples": "Examples: sqrt(16), sin(pi/2), log(e), 2**3, abs(-5)"
        }
        
        topic_lower = topic.lower()
        for key, value in help_topics.items():
            if key in topic_lower:
                return value
        
        return "Available help topics: trigonometry, logarithms, constants, operations, examples" 