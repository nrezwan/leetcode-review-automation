# main.py - The main entry point for LeetCode Review Automation
"""
LeetCode Review Automation Tool
A complete system to track and review LeetCode problems.

Modules:
- Git Parser: Reads problems from your repository
- Excel Manager: Stores problem data
- Sync Manager: Syncs Git → Excel
- Review Manager: Interactive review sessions
"""

import sys
import os
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import our modules
from git_parser import GitParser
from excel_manager import ExcelManager
from sync_manager import SyncManager
from review_manager import ReviewManager

class LeetCodeReviewApp:
    """Main application class for LeetCode Review Automation"""
    
    def __init__(self):
        """Initialize the application"""
        self.repo_path = "./LeetCode_Solutions"
        self.excel_path = "./data/LeetCodeReviewSheet.xlsx"
        self.sync_manager = None
        self.review_manager = None
        
        # Check if repository exists
        if not Path(self.repo_path).exists():
            print("⚠️ Warning: LeetCode repository not found!")
            print(f"   Looking for: {self.repo_path}")
            print("   Please clone your repository first.")
            print("   git clone https://github.com/nrezwan/LeetCode_Solutions.git")
    
    def setup_managers(self):
        """Initialize the managers"""
        self.sync_manager = SyncManager(self.repo_path, self.excel_path)
        self.review_manager = ReviewManager(self.excel_path)
    
    def show_menu(self):
        """Display the main menu"""
        print("\n" + "=" * 60)
        print("🚀 LEETCODE REVIEW AUTOMATOR")
        print("=" * 60)
        print("1. 📥 Sync Problems from Git")
        print("2. 📋 Start Review Session")
        print("3. 📊 Show Dashboard")
        print("4. 📖 View All Problems")
        print("5. 🔍 Search Problem")
        print("6. ⚙️ Settings")
        print("7. ❌ Exit")
        print("=" * 60)
    
    def sync_problems(self):
        """Sync problems from Git to Excel"""
        print("\n" + "=" * 60)
        print("📥 SYNCING PROBLEMS")
        print("=" * 60)
        
        if not self.sync_manager:
            self.setup_managers()
        
        self.sync_manager.sync_all()
        print("\n✅ Sync complete! Press Enter to continue...")
        input()
    
    def start_review(self):
        """Start an interactive review session"""
        print("\n" + "=" * 60)
        print("📋 REVIEW SESSION")
        print("=" * 60)
        
        if not self.review_manager:
            self.setup_managers()
        
        self.review_manager.start_review_session()
        print("\n✅ Review complete! Press Enter to continue...")
        input()
    
    def show_dashboard(self):
        """Display the dashboard"""
        if not self.review_manager:
            self.setup_managers()
        
        self.review_manager.show_dashboard()
        print("\nPress Enter to continue...")
        input()
    
    def view_all_problems(self):
        """Display all problems"""
        print("\n" + "=" * 60)
        print("📖 ALL PROBLEMS")
        print("=" * 60)
        
        if not self.excel_manager:
            self.setup_managers()
        
        problems = self.excel_manager.load_problems()
        
        if not problems:
            print("❌ No problems found in Excel.")
            print("💡 Run 'Sync Problems' first!")
            input()
            return
        
        print(f"\n📊 Total problems: {len(problems)}\n")
        
        # Sort by problem name
        sorted_problems = sorted(problems.items())
        
        # Show in columns
        for i, (name, data) in enumerate(sorted_problems, 1):
            status = data.get('status', '📝 New')
            reviews = data.get('successful_reviews', 0)
            print(f"{i:3}. {name:35} | {status:10} | Reviews: {reviews}")
        
        print(f"\n📊 Showing {len(sorted_problems)} problems")
        print("\nPress Enter to continue...")
        input()
    
    def search_problem(self):
        """Search for a specific problem"""
        print("\n" + "=" * 60)
        print("🔍 SEARCH PROBLEM")
        print("=" * 60)
        
        if not self.excel_manager:
            self.setup_managers()
        
        search_term = input("Enter problem name (or part of it): ").strip()
        
        if not search_term:
            print("❌ No search term provided.")
            input()
            return
        
        problems = self.excel_manager.load_problems()
        
        matches = []
        search_lower = search_term.lower()
        for name, data in problems.items():
            if search_lower in name.lower():
                matches.append((name, data))
        
        if not matches:
            print(f"❌ No problems found containing '{search_term}'")
        else:
            print(f"\n🔍 Found {len(matches)} match(es):\n")
            for name, data in matches:
                status = data.get('status', '📝 New')
                reviews = data.get('successful_reviews', 0)
                next_review = data.get('next_review_date', 'Unknown')
                print(f"  📝 {name}")
                print(f"     Status: {status}")
                print(f"     Reviews: {reviews}")
                print(f"     Next Review: {next_review}")
                print()
        
        print("Press Enter to continue...")
        input()
    
    def show_settings(self):
        """Show and update settings"""
        print("\n" + "=" * 60)
        print("⚙️ SETTINGS")
        print("=" * 60)
        
        print("1. Review Interval: 7 days")
        print("2. Repository Path: ./LeetCode_Solutions")
        print("3. Excel Path: ./data/LeetCodeReviewSheet.xlsx")
        print("\n💡 To change settings, edit the config.py file.")
        print("\n📊 Stats:")
        
        # ✅ Fixed: Use review_manager instead of excel_manager
        if self.review_manager:
            stats = self.review_manager.excel_manager.get_statistics()
            print(f"   Total Problems: {stats['total']}")
            print(f"   Due for Review: {stats['due']}")
        else:
            print("   ⚠️ Review manager not initialized. Please sync first.")
        
        print("\nPress Enter to continue...")
        input()
    
    def run(self):
        """Main application loop"""
        print("🚀 Initializing LeetCode Review Automator...")
        
        # Initialize managers
        self.setup_managers()
        
        while True:
            self.show_menu()
            choice = input("👉 Choose an option (1-7): ").strip()
            
            if choice == '1':
                self.sync_problems()
            elif choice == '2':
                self.start_review()
            elif choice == '3':
                self.show_dashboard()
            elif choice == '4':
                self.view_all_problems()
            elif choice == '5':
                self.search_problem()
            elif choice == '6':
                self.show_settings()
            elif choice == '7':
                print("\n👋 Goodbye! Happy coding!")
                break
            else:
                print("\n❌ Invalid choice. Please enter 1-7.")
                input("Press Enter to continue...")

def check_requirements():
    """Check if required packages are installed"""
    try:
        import git
        import openpyxl
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e.name}")
        print("\n💡 Install required packages:")
        print("   pip install -r requirements.txt")
        return False

def check_structure():
    """Check if the project structure is set up correctly"""
    issues = []
    
    if not Path("./LeetCode_Solutions").exists():
        issues.append("LeetCode_Solutions folder not found")
    
    if not Path("./src").exists():
        issues.append("src folder not found")
    
    if not Path("./data").exists():
        issues.append("data folder not found")
        print("📁 Creating data folder...")
        Path("./data").mkdir(exist_ok=True)
    
    if issues:
        print("⚠️ Project structure issues:")
        for issue in issues:
            print(f"   • {issue}")
        print("\n💡 Please make sure you have:")
        print("   1. Cloned your LeetCode repository as ./LeetCode_Solutions")
        print("   2. Created the src and data folders")
        print("   3. Installed all requirements")
        return False
    
    return True

def main():
    """Main entry point"""
    print("=" * 60)
    print("🚀 LEETCODE REVIEW AUTOMATOR")
    print("=" * 60)
    
    # Check requirements
    if not check_requirements():
        return
    
    # Check project structure
    if not check_structure():
        return
    
    # Run the application
    app = LeetCodeReviewApp()
    app.run()

if __name__ == "__main__":
    main()