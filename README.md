# 📱 Social Media Content Analyzer

A clean, compact, and easy-to-understand Python data project that examines social media performance across different content formats (**Reels, Videos, Images, Text**) on 5 major platforms (**Instagram, YouTube, Facebook, LinkedIn, Twitter**).

---

## 🌟 What This Project Does

- **Simple & Intuitive Dataset:** A clean 30-post sample dataset with clear metrics: Likes, Comments, Shares, and Views.
- **Straightforward Analytics:**
  - $\text{Total Engagement} = \text{Likes} + \text{Comments} + \text{Shares}$
  - $\text{Engagement Rate (\%)} = (\text{Total Engagement} / \text{Views}) \times 100$
- **High-Quality Visualizations:** Generates clean bar charts comparing average engagement and views.
- **Modern Interactive Web Dashboard:** Built with Streamlit and Plotly, featuring real-time filters, interactive charts, and a **Quick Post Simulator**.

---

## 📁 Project Structure

```text
Tiny-Project/
│
├── dataset/
│   └── social_media_data.csv       # Small, clean 30-row sample dataset
│
├── output/
│   ├── engagement_by_content.png   # Bar chart: Engagement by Content Type
│   ├── platform_performance.png   # Bar chart: Average Views by Platform
│   └── summary.csv                 # Exported performance summary table
│
├── analysis.py                     # Easy-to-read Python analysis script
├── app.py                          # Beautiful interactive Streamlit web UI
├── main.py                         # Single-line launcher
├── requirements.txt                # Minimal Python dependencies
└── README.md                       # Project documentation
```

---

## 🚀 Quick Start Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Analysis Script (Console + Charts)
```bash
python analysis.py
```
*or*
```bash
python main.py
```

This will:
1. Load the 30-post dataset.
2. Calculate total engagement and engagement rates.
3. Print a clean summary table to your terminal.
4. Save clean visualization charts and a summary CSV into the `output/` folder.

---

### 3. Launch the Interactive Web Dashboard (UI)
```bash
streamlit run app.py
```

This opens a beautiful dashboard in your browser (`http://localhost:8501`) where you can:
- Filter data by Platform and Content Type.
- View interactive Plotly charts with hover stats.
- Use the **Post Simulator** to estimate engagement for future posts.
- Download the filtered data as CSV.

---

## 📊 Summary of Findings

- **Reels** achieve the highest average engagement ($\approx 1,317$) and reach.
- **Videos** perform second best with strong watch time and steady engagement.
- **Images** provide consistent, quick-view engagement.
- **Text posts** are great for direct discussion and community conversations.
