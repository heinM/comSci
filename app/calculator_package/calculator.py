from opentelemetry import trace
from logging_package.logging_config import get_logger

logger = get_logger(__name__)
tracer = trace.get_tracer(__name__)

def perform_calculation(a: float, b: float, operation: str) -> float:
    """
    Docstring for perform_calculation
    Performs basic arithmetic operations on two numbers
    :param a: First number
    :param b: Second number
    :param operation: Operation to perform (add, subtract, multiply, divide)
    :return: Result of the operation
    """
    with tracer.start_as_current_span("perform_calculation"):
        logger.info("Performing calculation", a=a, b=b, operation=operation)
        result = 0
        if operation == "add":
            result = a + b
        elif operation == "subtract":
            result = a - b
        elif operation == "multiply":
            result = a * b
        elif operation == "divide":
            if b != 0:
                result = a / b
            else:
                logger.error("Division by zero attempted")
                raise ValueError("Cannot divide by zero")
        else:
            logger.error("Invalid operation", operation=operation)
            raise ValueError(f"Invalid operation: {operation}")
        
        logger.info("Calculation result", result=result)
        return result