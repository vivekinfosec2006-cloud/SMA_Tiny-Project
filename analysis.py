"""
A simple, easy-to-understand Python script to analyze social media engagement
across different content types (Reel, Video, Image, Text) and platforms.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set visual style for clean, modern plots
sns.set_theme(style="whitegrid")
plt.rcParams.update({"font.sans-serif": "Arial", "figure.autolayout": True})


def load_data(file_path="dataset/social_media_data.csv"):
    """Load the dataset from CSV file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset not found at: {file_path}")
    df = pd.read_csv(file_path)
    return df


def calculate_metrics(df):
    """
    Calculate essential engagement metrics:
    1. Engagement = Likes + Comments + Shares
    2. Engagement Rate (%) = (Engagement / Views) * 100
    """
    df_calc = df.copy()
    df_calc["Engagement"] = df_calc["Likes"] + df_calc["Comments"] + df_calc["Shares"]
    df_calc["Engagement_Rate"] = ((df_calc["Engagement"] / df_calc["Views"]) * 100).round(2)
    return df_calc


def generate_summary(df):
    """Group data by content type to calculate average performance."""
    summary = df.groupby("Content_Type").agg({
        "Post_ID": "count",
        "Views": "mean",
        "Likes": "mean",
        "Comments": "mean",
        "Shares": "mean",
        "Engagement": "mean",
        "Engagement_Rate": "mean"
    }).rename(columns={"Post_ID": "Total_Posts"}).round(1)

    # Sort from highest to lowest engagement
    summary = summary.sort_values(by="Engagement", ascending=False)
    return summary


def create_charts(df, summary, output_dir="output"):
    """Generate and save simple, beautiful charts."""
    os.makedirs(output_dir, exist_ok=True)

    # 1. Bar Chart: Average Engagement by Content Type
    plt.figure(figsize=(8, 5))
    palette = ["#4F46E5", "#06B6D4", "#10B981", "#F59E0B"]
    ax1 = sns.barplot(
        x=summary.index,
        y="Engagement",
        data=summary,
        hue=summary.index,
        palette=palette,
        legend=False
    )
    plt.title("Average Engagement by Content Type", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Content Type", fontsize=11, fontweight="bold")
    plt.ylabel("Average Engagement (Likes + Comments + Shares)", fontsize=11)
    
    for p in ax1.patches:
        val = int(p.get_height())
        ax1.annotate(f"{val}", (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha="center", va="bottom", fontsize=10, fontweight="bold", xytext=(0, 4),
                     textcoords="offset points")

    chart1_path = os.path.join(output_dir, "engagement_by_content.png")
    plt.savefig(chart1_path, dpi=300)
    plt.close()
    print(f"[+] Saved chart: {chart1_path}")

    # 2. Bar Chart: Average Views by Platform
    plt.figure(figsize=(8, 5))
    platform_avg = df.groupby("Platform")["Views"].mean().sort_values(ascending=False).round(1)
    ax2 = sns.barplot(
        x=platform_avg.index,
        y=platform_avg.values,
        hue=platform_avg.index,
        palette="viridis",
        legend=False
    )
    plt.title("Average Views by Platform", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Platform", fontsize=11, fontweight="bold")
    plt.ylabel("Average Views", fontsize=11)

    for p in ax2.patches:
        val = int(p.get_height())
        ax2.annotate(f"{val:,}", (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha="center", va="bottom", fontsize=10, fontweight="bold", xytext=(0, 4),
                     textcoords="offset points")

    chart2_path = os.path.join(output_dir, "platform_performance.png")
    plt.savefig(chart2_path, dpi=300)
    plt.close()
    print(f"[+] Saved chart: {chart2_path}")


def run():
    """Main execution function."""
    print("=" * 55)
    print("   SOCIAL MEDIA CONTENT ANALYZER (QUICK PIPELINE)")
    print("=" * 55)

    # Step 1: Load data
    df = load_data()
    print(f"[✓] Loaded dataset with {len(df)} posts.")

    # Step 2: Calculate metrics
    df_metrics = calculate_metrics(df)
    print("[✓] Calculated Engagement and Engagement Rate.")

    # Step 3: Performance summary
    summary = generate_summary(df_metrics)
    print("\n--- Content Performance Summary ---")
    print(summary[["Total_Posts", "Views", "Likes", "Engagement", "Engagement_Rate"]])

    # Step 4: Export charts and summary CSV
    create_charts(df_metrics, summary)
    
    summary_csv = "output/summary.csv"
    summary.to_csv(summary_csv)
    print(f"[✓] Exported summary table to: {summary_csv}")

    # Step 5: Highlight findings
    top_content = summary.index[0]
    top_eng = summary.loc[top_content, "Engagement"]
    print("\n" + "-" * 55)
    print(f"KEY RESULT: '{top_content}' performs best with {top_eng} avg engagement!")
    print("-" * 55)
    print("[Done] Analysis completed successfully.\n")


if __name__ == "__main__":
    run()
