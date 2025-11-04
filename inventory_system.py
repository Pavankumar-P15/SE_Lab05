"""
Inventory Management System

This module provides functions to manage stock inventory including
adding items, removing items, checking quantities, and persisting data.
"""

import json
import logging
from datetime import datetime


# Global variable for stock data
stock_data = {}


# Set up logging for better tracking
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


def add_item(item="default", qty=0, logs=None):
    """
    Add an item to the inventory.

    Args:
        item (str): Name of the item to add
        qty (int): Quantity to add (must be non-negative)
        logs (list, optional): List to append transaction logs

    Returns:
        None
    """
    if not isinstance(item, str) or not item:
        logging.warning("Invalid item name.")
        return
    if not isinstance(qty, int) or qty < 0:
        logging.warning("Invalid quantity value.")
        return

    # Update stock data
    stock_data[item] = stock_data.get(item, 0) + qty
    if logs is not None:
        logs.append(f"{datetime.now()}: Added {qty} of {item}")
    logging.info("Added %d of %s", qty, item)


def remove_item(item, qty):
    """
    Remove an item from the inventory.

    Args:
        item (str): Name of the item to remove
        qty (int): Quantity to remove (must be positive)

    Returns:
        None
    """
    if not isinstance(item, str) or item not in stock_data:
        logging.warning("Item %s not found in stock.", item)
        return
    if not isinstance(qty, int) or qty <= 0:
        logging.warning("Invalid quantity value.")
        return

    # Check if enough quantity is available
    if stock_data[item] < qty:
        logging.warning("Not enough stock of %s to remove.", item)
        return

    stock_data[item] -= qty
    if stock_data[item] <= 0:
        del stock_data[item]
    logging.info("Removed %d of %s", qty, item)


def get_qty(item):
    """
    Get the quantity of an item in stock.

    Args:
        item (str): Name of the item

    Returns:
        int: Quantity of the item (0 if not found)
    """
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """
    Load inventory data from a JSON file.

    Args:
        file (str): Path to the JSON file

    Returns:
        None
    """
    global stock_data  # pylint: disable=global-statement
    try:
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.load(f)
        logging.info("Data loaded successfully.")
    except FileNotFoundError:
        logging.warning(
            "%s not found. Starting with an empty inventory.", file
        )
    except json.JSONDecodeError:
        logging.error(
            "Error decoding the inventory file. Please check the file format."
        )


def save_data(file="inventory.json"):
    """
    Save inventory data to a JSON file.

    Args:
        file (str): Path to the JSON file

    Returns:
        None
    """
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(stock_data, f)
        logging.info("Data saved successfully.")
    except IOError as e:
        logging.error("Error saving data: %s", e)


def print_data():
    """
    Print the current inventory to console.

    Returns:
        None
    """
    print("Items Report:")
    for item, qty in stock_data.items():
        print(f"{item} -> {qty}")


def check_low_items(threshold=5):
    """
    Check for items below a specified threshold.

    Args:
        threshold (int): Minimum quantity threshold

    Returns:
        list: List of item names below the threshold
    """
    low_items = [item for item, qty in stock_data.items() if qty < threshold]
    return low_items


def main():
    """
    Main function to demonstrate inventory system usage.

    Returns:
        None
    """
    logs = []
    add_item("apple", 10, logs)
    add_item("banana", -2, logs)  # Invalid, will log warning
    add_item(123, "ten", logs)  # Invalid types, will log warning
    remove_item("apple", 3)
    remove_item("orange", 1)  # Item doesn't exist, will log warning
    print("Apple stock:", get_qty("apple"))
    print("Low items:", check_low_items())
    save_data()
    load_data()
    print_data()


if __name__ == "__main__":
    main()
