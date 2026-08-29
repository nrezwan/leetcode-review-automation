# 🚀 LeetCode Review Automation

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![GitHub](https://img.shields.io/badge/GitHub-Repo-black.svg)](https://github.com/nrezwan/leetcode-review-automation)

A powerful **spaced repetition system** that automatically tracks your LeetCode solutions and schedules smart review sessions to help you retain knowledge effectively.

---

## 🎯 Why This Project?

Solving LeetCode problems is great, but **retaining what you've learned** is the real challenge. This tool:

- 📥 **Auto-syncs** your solved problems from Git
- 📅 **Schedules reviews** at optimal intervals (spaced repetition)
- 📊 **Tracks progress** in Excel (no database needed!)
- 🧠 **Helps you remember** algorithms and patterns long-term

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **📥 Auto-Sync** | Detects new/updated problems from your Git repository |
| **📋 Review Sessions** | Interactive reviews with spaced repetition scheduling |
| **📊 Excel Tracking** | Simple, viewable progress tracking in Excel |
| **📈 Dashboard** | Quick overview of your progress and due reviews |
| **🔍 Search** | Find any problem quickly |
| **📖 View All** | Complete list of all tracked problems |

### Smart Scheduling
- **Success** → Next review interval **increases** (exponential backoff)
- **Failure** → Next review interval **resets** to 7 days
- **New problem** → First review after **7 days**

---

## 📂 Project Structure
leetcode-review-automation/
├── 📁 src/ # Core modules
│ ├── 📄 git_parser.py # Reads problems from Git
│ ├── 📄 excel_manager.py # Handles Excel file operations
│ ├── 📄 sync_manager.py # Syncs Git → Excel
│ └── 📄 review_manager.py # Interactive review sessions
├── 📁 data/ # Your review data (gitignored)
│ └── 📄 LeetCodeReviewSheet.xlsx
├── 📁 LeetCode_Solutions/ # Your LeetCode repository
├── 📄 main.py # Main entry point
├── 📄 requirements.txt # Dependencies
├── 📄 .gitignore # Git ignore rules
└── 📄 README.md # This file

text

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/nrezwan/leetcode-review-automation.git
cd leetcode-review-automation
2. Set Up Virtual Environment
bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows
3. Install Dependencies
bash
pip install -r requirements.txt
4. Clone Your LeetCode Solutions
bash
# Make sure you're in the project root
git clone https://github.com/nrezwan/LeetCode_Solutions.git
5. Run the Application
bash
python3 main.py
📋 Usage Guide
Main Menu
text
🚀 LEETCODE REVIEW AUTOMATOR
============================================================
1. 📥 Sync Problems from Git
2. 📋 Start Review Session
3. 📊 Show Dashboard
4. 📖 View All Problems
5. 🔍 Search Problem
6. ⚙️ Settings
7. ❌ Exit
1. Sync Problems
Reads all problem folders from ./LeetCode_Solutions

Adds new problems to Excel

Updates "Date Last Solved" for existing problems

2. Review Session
Shows problems due for review

For each problem, asks: "Did you solve it?"

Yes → Extends review interval, increments success count

No → Resets interval to 7 days

Skip → Leaves the problem as-is

3. Dashboard
Shows:

Total problems tracked

Problems due for review

Status breakdown (New/Success/Retry)

4. View All Problems
Complete list of all problems with their status and review count.

5. Search Problem
Find a specific problem by name.

📊 How the Review Schedule Works
Successful Reviews	Next Review Interval
0 → 1	14 days
1 → 2	21 days
2 → 3	28 days
3+	Increases by 7 days each time
Failed Review	Resets to 7 days
📁 Excel File Structure
Column	Description
LeetCode Problem	Problem name (e.g., 1-two-sum)
Date Last Solved	When you last solved it
Next Review Date	When to review next
Successful Reviews	Number of successful reviews
Status	📝 New / ✅ Success / 🔄 Retry
🛠️ Requirements
text
Python 3.8+
GitPython>=3.1.0
openpyxl>=3.1.0
🤝 Contributing
Contributions are welcome! Here's how:

Fork the repository

Create a feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request

📄 License
This project is open source and available under the MIT License.

📬 Connect
GitHub: nrezwan

LeetCode: nrezwan

🌟 Star the Project
If this project helps you, please ⭐ Star it on GitHub!

https://img.shields.io/github/stars/nrezwan/leetcode-review-automation?style=social

🙏 Acknowledgments
LeetSync for automatic GitHub sync

Spaced Repetition for the review algorithm
