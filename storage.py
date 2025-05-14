import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use an absolute path to ensure consistent file location
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(DATA_DIR, "data.json")

def load_data():
    try:
        if not os.path.exists(DATA_FILE):
            logger.info(f"Data file {DATA_FILE} not found. Creating new data structure.")
            initial_data = {"inventory": [], "sales": []}
            # Create the file immediately to ensure it exists
            with open(DATA_FILE, "w") as f:
                json.dump(initial_data, f, indent=4)
            return initial_data
        
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            logger.info(f"Successfully loaded data from {DATA_FILE}")
            return data
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from {DATA_FILE}. Creating new data structure.")
        initial_data = {"inventory": [], "sales": []}
        with open(DATA_FILE, "w") as f:
            json.dump(initial_data, f, indent=4)
        return initial_data
    except Exception as e:
        logger.error(f"Unexpected error loading data: {str(e)}. Creating new data structure.")
        initial_data = {"inventory": [], "sales": []}
        try:
            with open(DATA_FILE, "w") as f:
                json.dump(initial_data, f, indent=4)
        except Exception as write_err:
            logger.error(f"Failed to create new data file: {str(write_err)}")
        return initial_data

def save_data(data):
    try:
        # Create a backup of the existing file
        if os.path.exists(DATA_FILE):
            backup_file = f"{DATA_FILE}.bak"
            try:
                with open(DATA_FILE, "r") as src, open(backup_file, "w") as dst:
                    dst.write(src.read())
                logger.info(f"Created backup at {backup_file}")
            except Exception as e:
                logger.warning(f"Failed to create backup: {str(e)}")
        
        # Save the new data
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
            logger.info(f"Successfully saved data to {DATA_FILE}")
            
        # Verify the file was created
        if os.path.exists(DATA_FILE):
            logger.info(f"Verified data file exists at {DATA_FILE}")
        else:
            logger.error(f"Data file was not created at {DATA_FILE}")
            
    except Exception as e:
        logger.error(f"Error saving data: {str(e)}")
        raise

# Test the functions directly
if __name__ == "__main__":
    print(f"Testing storage module. Data file location: {DATA_FILE}")
    test_data = {"inventory": [{"item_id": "1", "name": "Test Item", "price": 9.99}], "sales": []}
    save_data(test_data)
    loaded_data = load_data()
    print(f"Loaded data: {loaded_data}")