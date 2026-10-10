"""
Clean, straightforward data analysis workflow.
"""

import os
import sys

# Add parent directory to path so analysis can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from analysis import load_data, calculate_metrics, generate_summary, create_charts, run

if __name__ == "__main__":
    run()
