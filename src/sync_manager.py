# src/sync_manager.py - Add sorting

import re
from pathlib import Path
from datetime import datetime
from git_parser import GitParser
from excel_manager import ExcelManager

class SyncManager:
    def __init__(self, repo_path="./LeetCode_Solutions", excel_path="./data/LeetCodeReviewSheet.xlsx"):
        self.repo_path = Path(repo_path)
        self.excel_path = Path(excel_path)
        
        # Ensure data directory exists
        self.excel_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.git_parser = GitParser(str(self.repo_path))
        self.excel_manager = ExcelManager(str(self.excel_path))
        self.excel_manager.setup_excel()
    
    def _extract_number(self, problem_name):
        """Extract the number from a problem name for sorting."""
        # e.g., "1-two-sum" → 1, "141-linked-list-cycle" → 141
        match = re.match(r'^(\d+)', problem_name)
        return int(match.group(1)) if match else 999999
    
    def sync_all(self):
        """Sync all problems from Git to Excel."""
        print("\n" + "=" * 60)
        print("🔄 SYNCING PROBLEMS")
        print("=" * 60)
        
        # Get problems from Git
        problems = self.git_parser.get_all_problems()
        
        if not problems:
            print("❌ No problems found in repository!")
            return {'added': 0, 'updated': 0, 'total': 0}
        
        print(f"\n📊 Found {len(problems)} problems in repository")
        
        # ✅ Sort problems numerically by problem number
        problems.sort(key=lambda p: self._extract_number(p['name']))
        print(f"📊 Sorted {len(problems)} problems by number")
        
        # Load existing Excel data
        existing = self.excel_manager.load_problems()
        print(f"📊 Found {len(existing)} problems in Excel")
        
        added = 0
        updated = 0
        
        for problem in problems:
            name = problem['name']
            date = problem['date']
            
            if name in existing:
                updated += 1
                self.excel_manager.add_or_update_problem(name, date)
            else:
                added += 1
                self.excel_manager.add_or_update_problem(name, date)
        
        self.excel_manager.save()
        
        print("\n" + "=" * 60)
        print("📊 SYNC SUMMARY")
        print("=" * 60)
        print(f"✅ Added: {added} new problems")
        print(f"🔄 Updated: {updated} existing problems")
        print(f"📝 Total: {added + updated} problems synced")
        
        return {'added': added, 'updated': updated, 'total': added + updated}