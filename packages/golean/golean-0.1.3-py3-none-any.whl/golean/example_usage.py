from golean import GoLean
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Initialize the client
    golean = GoLean()  # API key will be read from GOLEAN_API_KEY environment variable

    context = """
    The Industrial Revolution was a period of major industrialization and innovation during the late 18th and early 19th century. 
    The Industrial Revolution began in Great Britain and quickly spread throughout Europe and North America. 
    This era saw the mechanization of agriculture and textile manufacturing and a revolution in power, including steam ships and railroads, 
    that affected social, cultural and economic conditions.
    """
    
    question = "What were the main impacts of the Industrial Revolution?"

    try:
        result = golean.compress_prompt(
            context=context,
            question=question,
            compression_rate=0.5,
            model="gpt-4o"
        )
        logger.info(f"Compressed prompt: {result['compressed_prompt']}")
        logger.info(f"Original length: {len(context)}")
        logger.info(f"Compressed length: {len(result['compressed_prompt'])}")
        savings_percentage = (1 - len(result['compressed_prompt']) / len(context)) * 100
        logger.info(f"Savings percentage: {savings_percentage:.2f}%")
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()