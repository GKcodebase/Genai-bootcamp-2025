"""
Calculator Agent Implementation using LangChain
Includes mathematical computation tools and safe evaluation.
"""

import math
import ast
import operator
from typing import List, Dict, Any, Union
from langchain.tools import Tool

from .base_langchain_agent import BaseLangChainAgent

class CalculatorLangChainAgent(BaseLangChainAgent):
    """LangChain-powered calculator agent with mathematical tools."""
    
    def __init__(self, **kwargs):
        """Initialize calculator agent with math tools."""
        super().__init__(**kwargs)
    
    def _get_tools(self) -> List[Tool]:
        """Get mathematical tools for the agent."""
        tools = [
            Tool(
                name="calculator",
                description="Evaluate mathematical expressions safely. Supports basic arithmetic, trigonometry, logarithms, and common math functions. Example: '2 + 2', 'sqrt(16)', 'sin(pi/2)'",
                func=self._safe_eval
            ),
            Tool(
                name="unit_converter",
                description="Convert between common units. Format: 'value from_unit to_unit'. Example: '100 celsius to fahrenheit', '5 miles to kilometers'",
                func=self._convert_units
            ),
            Tool(
                name="math_constants",
                description="Get mathematical constants like pi, e, golden ratio, etc. Example: 'pi', 'e', 'golden_ratio'",
                func=self._get_constant
            ),
            Tool(
                name="number_info",
                description="Get information about a number (prime status, factors, properties). Example: '17', '100'",
                func=self._number_info
            ),
            Tool(
                name="sequence_generator",
                description="Generate mathematical sequences. Format: 'type:start:end' or 'type:start:count'. Example: 'fibonacci:1:10', 'prime:1:50'",
                func=self._generate_sequence
            )
        ]
        return tools
    
    def _safe_eval(self, expression: str) -> str:
        """Safely evaluate mathematical expressions."""
        try:
            # Clean the expression
            expression = expression.strip()
            
            # Replace common mathematical functions and constants
            replacements = {
                'pi': 'math.pi',
                'e': 'math.e',
                'sqrt': 'math.sqrt',
                'sin': 'math.sin',
                'cos': 'math.cos',
                'tan': 'math.tan',
                'log': 'math.log',
                'log10': 'math.log10',
                'exp': 'math.exp',
                'abs': 'abs',
                'pow': 'pow',
                'round': 'round'
            }
            
            for old, new in replacements.items():
                expression = expression.replace(old, new)
            
            # Safe evaluation using ast
            node = ast.parse(expression, mode='eval')
            result = self._eval_node(node.body)
            
            return f"Result: {result}"
            
        except Exception as e:
            return f"Error: Unable to evaluate '{expression}'. {str(e)}"
    
    def _eval_node(self, node):
        """Safely evaluate an AST node."""
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand)
            if isinstance(node.op, ast.UAdd):
                return +operand
            elif isinstance(node.op, ast.USub):
                return -operand
        elif isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            
            operators = {
                ast.Add: operator.add,
                ast.Sub: operator.sub,
                ast.Mult: operator.mul,
                ast.Div: operator.truediv,
                ast.Pow: operator.pow,
                ast.Mod: operator.mod,
                ast.FloorDiv: operator.floordiv
            }
            
            if type(node.op) in operators:
                return operators[type(node.op)](left, right)
        elif isinstance(node, ast.Call):
            func_name = node.func.attr if isinstance(node.func, ast.Attribute) else node.func.id
            args = [self._eval_node(arg) for arg in node.args]
            
            # Handle math module functions
            if hasattr(math, func_name):
                return getattr(math, func_name)(*args)
            elif func_name in ['abs', 'pow', 'round']:
                return eval(func_name)(*args)
        elif isinstance(node, ast.Attribute):
            if node.attr == 'pi':
                return math.pi
            elif node.attr == 'e':
                return math.e
        
        raise ValueError(f"Unsupported operation: {type(node)}")
    
    def _convert_units(self, conversion: str) -> str:
        """Convert between units."""
        try:
            parts = conversion.lower().split()
            if len(parts) != 4 or parts[2] != 'to':
                return "Format: 'value from_unit to to_unit'"
            
            value = float(parts[0])
            from_unit = parts[1]
            to_unit = parts[3]
            
            # Temperature conversions
            if from_unit == 'celsius' and to_unit == 'fahrenheit':
                result = (value * 9/5) + 32
                return f"{value}°C = {result}°F"
            elif from_unit == 'fahrenheit' and to_unit == 'celsius':
                result = (value - 32) * 5/9
                return f"{value}°F = {result:.2f}°C"
            
            # Length conversions
            length_conversions = {
                ('meters', 'feet'): 3.28084,
                ('feet', 'meters'): 0.3048,
                ('miles', 'kilometers'): 1.60934,
                ('kilometers', 'miles'): 0.621371,
                ('inches', 'centimeters'): 2.54,
                ('centimeters', 'inches'): 0.393701
            }
            
            key = (from_unit, to_unit)
            if key in length_conversions:
                result = value * length_conversions[key]
                return f"{value} {from_unit} = {result:.4f} {to_unit}"
            
            return f"Conversion from {from_unit} to {to_unit} not supported"
            
        except Exception as e:
            return f"Error in conversion: {str(e)}"
    
    def _get_constant(self, constant_name: str) -> str:
        """Get mathematical constants."""
        constants = {
            'pi': math.pi,
            'e': math.e,
            'golden_ratio': (1 + math.sqrt(5)) / 2,
            'euler_gamma': 0.5772156649015329,
            'sqrt2': math.sqrt(2),
            'sqrt3': math.sqrt(3)
        }
        
        constant_name = constant_name.lower().strip()
        if constant_name in constants:
            value = constants[constant_name]
            return f"{constant_name} = {value}"
        else:
            available = ', '.join(constants.keys())
            return f"Unknown constant. Available: {available}"
    
    def _number_info(self, number_str: str) -> str:
        """Get information about a number."""
        try:
            num = int(float(number_str))
            info = []
            
            # Basic properties
            info.append(f"Number: {num}")
            info.append(f"Even: {num % 2 == 0}")
            info.append(f"Odd: {num % 2 == 1}")
            
            # Prime check
            if num > 1:
                is_prime = all(num % i != 0 for i in range(2, int(math.sqrt(num)) + 1))
                info.append(f"Prime: {is_prime}")
            
            # Factors
            if 1 <= num <= 1000:  # Only for reasonable numbers
                factors = [i for i in range(1, num + 1) if num % i == 0]
                info.append(f"Factors: {factors}")
            
            # Perfect square check
            sqrt_num = math.sqrt(num)
            if sqrt_num == int(sqrt_num):
                info.append(f"Perfect square: True (√{num} = {int(sqrt_num)})")
            
            return '\n'.join(info)
            
        except Exception as e:
            return f"Error analyzing number: {str(e)}"
    
    def _generate_sequence(self, sequence_spec: str) -> str:
        """Generate mathematical sequences."""
        try:
            parts = sequence_spec.split(':')
            if len(parts) != 3:
                return "Format: 'type:start:end' or 'type:start:count'"
            
            seq_type, start_str, end_str = parts
            start = int(start_str)
            end_or_count = int(end_str)
            
            if seq_type.lower() == 'fibonacci':
                sequence = self._fibonacci_sequence(start, end_or_count)
            elif seq_type.lower() == 'prime':
                sequence = self._prime_sequence(start, end_or_count)
            elif seq_type.lower() == 'square':
                sequence = [i**2 for i in range(start, end_or_count + 1)]
            elif seq_type.lower() == 'cube':
                sequence = [i**3 for i in range(start, end_or_count + 1)]
            else:
                return f"Unknown sequence type: {seq_type}. Available: fibonacci, prime, square, cube"
            
            return f"{seq_type.title()} sequence: {sequence}"
            
        except Exception as e:
            return f"Error generating sequence: {str(e)}"
    
    def _fibonacci_sequence(self, start: int, count: int) -> List[int]:
        """Generate Fibonacci sequence."""
        if count <= 0:
            return []
        if count == 1:
            return [start]
        
        sequence = [start, start + 1]
        for _ in range(count - 2):
            sequence.append(sequence[-1] + sequence[-2])
        
        return sequence[:count]
    
    def _prime_sequence(self, start: int, end: int) -> List[int]:
        """Generate prime numbers in range."""
        primes = []
        for num in range(max(2, start), end + 1):
            if all(num % i != 0 for i in range(2, int(math.sqrt(num)) + 1)):
                primes.append(num)
        return primes
    
    def _get_system_prompt(self) -> str:
        """Get system prompt for calculator agent."""
        return """You are a professional mathematics assistant specializing in calculations, conversions, and mathematical analysis.

Your capabilities include:
- Basic and advanced mathematical calculations
- Unit conversions (temperature, length, etc.)
- Mathematical constants and their values
- Number analysis (prime checking, factors, properties)
- Mathematical sequence generation

Calculation Process:
1. Understand the mathematical problem or question
2. Use appropriate tools for calculations
3. Provide clear, step-by-step explanations
4. Show intermediate steps when helpful
5. Include relevant mathematical context

Always:
- Show your work and reasoning
- Use appropriate mathematical notation
- Provide exact answers when possible, approximations when necessary
- Explain mathematical concepts when relevant
- Double-check calculations for accuracy

Be precise and educational. Help users understand not just the answer, but the mathematical process."""

    def calculate(self, expression: str) -> Dict[str, Any]:
        """
        Perform a calculation with explanation.
        
        Args:
            expression: Mathematical expression to evaluate
            
        Returns:
            Calculation results with explanation
        """
        result = self.run(f"Calculate and explain: {expression}")
        result["expression"] = expression
        result["calculation_type"] = "mathematical"
        
        return result 