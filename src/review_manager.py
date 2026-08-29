# src/review_manager.py
"""
Review Manager - Handles interactive review sessions
"""

from datetime import datetime, timedelta
from excel_manager import ExcelManager

class ReviewManager:
    """Manage interactive review sessions"""
    
    def __init__(self, excel_path="./data/LeetCodeReviewSheet.xlsx"):
        """
        Initialize the review manager.
        
        Args:
            excel_path (str): Path to the Excel file
        """
        self.excel_manager = ExcelManager(excel_path)
        self.excel_manager.setup_excel()
    
    def start_review_session(self):
        """
        Start an interactive review session.
        Shows all due problems and asks for updates.
        """
        print("\n" + "=" * 60)
        print("📋 REVIEW SESSION")
        print("=" * 60)
        
        # Get problems due for review
        due_problems = self.excel_manager.get_due_reviews()
        
        if not due_problems:
            print("\n🎉 No problems due for review today!")
            print("📅 Check back tomorrow or sync new problems.")
            return
        
        print(f"\n📌 {len(due_problems)} problem(s) due for review:\n")
        
        # Track updates for summary
        updated = {
            'success': 0,
            'retry': 0,
            'skipped': 0
        }
        
        for problem in due_problems:
            print("-" * 50)
            print(f"📝 {problem['name']}")
            print(f"   📅 Next Review: {problem['next_review']}")
            print(f"   ✅ Successful Reviews: {problem['successful_reviews']}")
            
            # Get user input
            while True:
                response = input("   Did you solve it? (y/n/skip): ").lower().strip()
                if response in ['y', 'n', 'skip']:
                    break
                print("   ❌ Invalid input. Please enter 'y', 'n', or 'skip'")
            
            if response == 'y':
                # Success!
                self.excel_manager.update_review_result(problem['name'], success=True)
                updated['success'] += 1
                
            elif response == 'n':
                # Failure - reset interval
                self.excel_manager.update_review_result(problem['name'], success=False)
                updated['retry'] += 1
                
            else:
                # Skipped
                print(f"   ⏭️ Skipped {problem['name']}")
                updated['skipped'] += 1
            
            print()  # Blank line after each problem
        
        # Show summary
        print("=" * 60)
        print("📊 REVIEW SESSION SUMMARY")
        print("=" * 60)
        print(f"✅ Successfully solved: {updated['success']}")
        print(f"🔄 Need to retry: {updated['retry']}")
        print(f"⏭️ Skipped: {updated['skipped']}")
        print(f"📝 Total reviewed: {updated['success'] + updated['retry']}")
        
        if updated['success'] > 0:
            print("\n💡 Great job! Keep up the good work!")
        elif updated['retry'] > 0:
            print("\n💪 Keep practicing! You'll get them next time.")
        
        # Save after all updates
        self.excel_manager.save()
    
    def show_dashboard(self):
        """
        Show a quick dashboard of the current state.
        """
        stats = self.excel_manager.get_statistics()
        due_problems = self.excel_manager.get_due_reviews()
        
        print("\n" + "=" * 60)
        print("📊 LEETCODE REVIEW DASHBOARD")
        print("=" * 60)
        print(f"📝 Total Problems: {stats['total']}")
        print(f"📅 Due for Review: {stats['due']}")
        
        # Show status breakdown
        print("\n📋 Status Breakdown:")
        for status, count in stats['status_counts'].items():
            emoji = status[0]  # Get the emoji from status
            print(f"   {status}: {count}")
        
        # Show next 5 due problems (if any)
        if due_problems:
            print("\n📋 Next Problems Due:")
            for i, p in enumerate(due_problems[:5], 1):
                days_until = (p['next_review'] - datetime.now().date()).days
                if days_until <= 0:
                    print(f"   {i}. {p['name']} - ⚠️ Overdue!")
                else:
                    print(f"   {i}. {p['name']} - In {days_until} days")
        else:
            print("\n🎉 No problems due for review!")

# Quick test
if __name__ == "__main__":
    print("🧪 Testing Review Manager")
    print("=" * 50)
    
    review = ReviewManager()
    
    # Show dashboard
    review.show_dashboard()
    
    # Start review session
    print("\n🚀 Starting review session...")
    review.start_review_session()