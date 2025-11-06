"""Calculator agent for mathematical operations."""

import re
from ..models import AgentCard, Skill, TaskMessage, InteractionMode
from .base_agent import BaseAgent


class CalculatorAgent(BaseAgent):
    """An agent that performs mathematical calculations."""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 5001):
        """Initialize the calculator agent."""
        super().__init__(
            name="CalculatorAgent",
            description="An agent that performs basic mathematical calculations",
            host=host,
            port=port
        )
    
    def get_agent_card(self) -> AgentCard:
        """Return the agent card for the calculator."""
        return AgentCard(
            name=self.name,
            description=self.description,
            url=f"http://{self.host}:{self.port}",
            skills=[
                Skill(
                    name="calculate",
                    description="Perform mathematical calculations (addition, subtraction, multiplication, division)",
                    parameters={
                        "expression": {
                            "type": "string",
                            "description": "Mathematical expression to evaluate"
                        }
                    },
                    interaction_modes=[InteractionMode.TEXT]
                ),
                Skill(
                    name="solve_equation",
                    description="Solve simple linear equations",
                    parameters={
                        "equation": {
                            "type": "string",
                            "description": "Linear equation to solve (e.g., '2x + 5 = 15')"
                        }
                    },
                    interaction_modes=[InteractionMode.TEXT]
                )
            ],
            supported_interaction_modes=[InteractionMode.TEXT],
            metadata={"version": "1.0.0", "type": "calculator"}
        )
    
    def handle_task(self, task_id: str, message: TaskMessage) -> str:
        """Process a calculation request.
        
        Args:
            task_id: The task ID
            message: The message containing the calculation request
            
        Returns:
            The calculation result as a string
        """
        content = message.content.lower().strip()
        
        # Try to solve equations first
        if "=" in content and any(var in content for var in ['x', 'y', 'z']):
            return self._solve_equation(content)
        
        # Otherwise, treat as a calculation expression
        return self._calculate(content)
    
    def _calculate(self, expression: str) -> str:
        """Evaluate a mathematical expression.
        
        Args:
            expression: The expression to evaluate
            
        Returns:
            The result as a string
        """
        try:
            # Remove common phrases
            expression = expression.replace("calculate", "").replace("what is", "").strip()
            
            # Only allow safe characters for evaluation
            if not re.match(r'^[\d\s+\-*/().]+$', expression):
                return f"Invalid expression. Please use only numbers and operators (+, -, *, /, parentheses)."
            
            result = eval(expression)
            return f"The result of {expression} is {result}"
        except Exception as e:
            return f"Error calculating expression: {str(e)}"
    
    def _solve_equation(self, equation: str) -> str:
        """Solve a simple linear equation.
        
        Args:
            equation: The equation to solve (e.g., "2x + 5 = 15")
            
        Returns:
            The solution as a string
        """
        try:
            # Parse equation like "2x + 5 = 15"
            equation = equation.replace("solve", "").strip()
            parts = equation.split("=")
            if len(parts) != 2:
                return "Invalid equation format. Please use format like '2x + 5 = 15'"
            
            left, right = parts[0].strip(), parts[1].strip()
            
            # Find the variable
            var = None
            for v in ['x', 'y', 'z']:
                if v in left:
                    var = v
                    break
            
            if not var:
                return "No variable found. Please include x, y, or z in your equation."
            
            # For demonstration, solve by trying different values
            # In a real implementation, use proper algebraic solving
            right_val = float(eval(right))
            
            for test_val in range(-1000, 1001):
                # Replace variable with test value
                test_expr = left.replace(var, str(test_val))
                
                # Handle cases like "x" -> need to treat as just the number
                # Add * before numbers that come after variables
                test_expr = re.sub(r'(\d)([a-z])', r'\1*\2', test_expr)
                test_expr = re.sub(r'([a-z])(\d)', r'\1*\2', test_expr)
                
                try:
                    if abs(eval(test_expr) - right_val) < 0.001:
                        return f"The solution is {var} = {test_val}"
                except:
                    continue
            
            return "Could not find a solution in the range [-1000, 1000]"
            
        except Exception as e:
            return f"Error solving equation: {str(e)}"


if __name__ == "__main__":
    agent = CalculatorAgent()
    agent.run(debug=True)
