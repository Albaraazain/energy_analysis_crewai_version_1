# src/agents/data_analyst.py

from crewai import Agent
from typing import Dict, List
import statistics
from datetime import datetime

class DataAnalystAgent:
    """
    Agent responsible for analyzing energy consumption data and identifying patterns.
    """


    @staticmethod
    def create_agent(llm) -> Agent:
        """
        Create and configure the Data Analyst agent.

        Args:
            llm: Language model instance to be used by the agent

        Returns:
            Agent: Configured Data Analyst agent
        """
        return Agent(
            role='Energy Data Analyst',
            goal='Analyze energy consumption data and identify meaningful patterns',
            backstory="""You are an experienced energy data analyst with expertise in 
            residential energy consumption. You excel at interpreting usage patterns
            and identifying opportunities for optimization. Your analysis helps 
            homeowners understand their energy usage patterns.""",
            verbose=True,
            llm=llm,
            allow_delegation=False
        )

    @staticmethod
    def calculate_basic_statistics(data: Dict[str, float]) -> Dict:
        """
        Calculate basic statistical measures from consumption data.

        Args:
            data: Dictionary of monthly consumption data

        Returns:
            Dictionary containing statistical measures
        """
        values = list(data.values())
        return {
            "average": statistics.mean(values),
            "median": statistics.median(values),
            "min": min(values),
            "max": max(values),
            "std_dev": statistics.stdev(values) if len(values) > 1 else 0
        }

    @staticmethod
    def identify_patterns(data: Dict[str, float]) -> Dict:
        """
        Identify patterns and anomalies in consumption data.

        Args:
            data: Dictionary of monthly consumption data

        Returns:
            Dictionary containing identified patterns and anomalies
        """
        sorted_data = dict(sorted(data.items()))
        values = list(sorted_data.values())
        avg = statistics.mean(values)
        std_dev = statistics.stdev(values) if len(values) > 1 else 0

        # Identify months with unusual consumption
        anomalies = {}
        seasonal_patterns = {"summer": [], "winter": [], "spring_fall": []}

        for date, value in sorted_data.items():
            month = int(date.split('-')[1])

            # Check for anomalies (values more than 2 standard deviations from mean)
            if abs(value - avg) > (2 * std_dev):
                anomalies[date] = value

            # Group by season
            if month in [12, 1, 2]:
                seasonal_patterns["winter"].append(value)
            elif month in [6, 7, 8]:
                seasonal_patterns["summer"].append(value)
            else:
                seasonal_patterns["spring_fall"].append(value)

        # Calculate seasonal averages
        seasonal_averages = {
            season: statistics.mean(values) if values else 0
            for season, values in seasonal_patterns.items()
        }

        return {
            "anomalies": anomalies,
            "seasonal_averages": seasonal_averages,
            "trend": "increasing" if len(values) > 1 and values[-1] > values[0] else "decreasing"
        }