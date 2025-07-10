"""
Humanitix tools for LLMgine integration.
These are wrapper functions that expose the existing Humanitix functionality
as tools that can be called by the LLM.
"""

from typing import List, Dict, Any
from chico.tools.humanitix import Humanitix


# Initialize the Humanitix client
humanitix_client = Humanitix()


def list_events() -> str:
    """List all available events from Humanitix.
    
    Returns:
        A formatted string containing all events with their details.
    """
    return humanitix_client.list_events()


def get_event_details(event_name: str) -> str:
    """Get detailed information about a specific event by name.
    
    Args:
        event_name: The name of the event to get details for.
        
    Returns:
        A formatted string containing the event details.
    """
    return humanitix_client.show_event_details_by_name(event_name)


def get_ticket_status(event_name: str) -> str:
    """Get ticket status and availability for a specific event.
    
    Args:
        event_name: The name of the event to check ticket status for.
        
    Returns:
        A formatted string containing ticket status and availability information.
    """
    return humanitix_client.get_ticket_status(event_name)


def search_events(query: str) -> str:
    """Search for events that match the given query.
    
    Args:
        query: The search query to find matching events.
        
    Returns:
        A formatted string containing matching events.
    """
    # This would need to be implemented in the Humanitix class
    # For now, we'll use the existing list_events and filter
    all_events = humanitix_client.list_events()
    # Simple text-based search - could be enhanced
    if query.lower() in all_events.lower():
        return f"Found events matching '{query}':\n{all_events}"
    else:
        return f"No events found matching '{query}'"


def get_upcoming_events() -> str:
    """Get a list of upcoming events.
    
    Returns:
        A formatted string containing upcoming events.
    """
    # This would need to be implemented in the Humanitix class
    # For now, return all events
    return humanitix_client.list_events() 