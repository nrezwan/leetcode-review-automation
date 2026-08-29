# src/git_parser.py
"""
Git Parser Module - Handles reading commits from the LeetCode repository
"""

import re
from pathlib import Path
from datetime import datetime
import git

class GitParser:
    """Parse Git commits to extract LeetCode problem information"""
    
    def __init__(self, repo_path="./LeetCode_Solutions"):
        self.repo_path = Path(repo_path)
        self.repo = None
        self.problems = []
        
    def is_valid_repo(self):
        """Check if the repository exists and is valid"""
        if not self.repo_path.exists():
            return False
        try:
            self.repo = git.Repo(self.repo_path)
            return True
        except git.InvalidGitRepositoryError:
            return False

    def get_problems_from_folders(self):
        """Get problem names from folder structure with Git commit dates."""
        if not self.is_valid_repo():
            print(f"❌ Repository not found at: {self.repo_path}")
            return []
        
        problems = []
        print(f"🔍 Scanning folders in {self.repo_path}...")
        
        # Get a mapping of folder names to commit dates
        commit_dates = self._get_commit_dates_for_folders()
        
        for item in self.repo_path.iterdir():
            if item.is_dir() and re.match(r'^\d+-[\w-]+', item.name):
                # Try to get commit date from our mapping
                commit_date = commit_dates.get(item.name)
                
                if commit_date is None:
                    # Fallback to file modification time
                    commit_date = datetime.fromtimestamp(item.stat().st_mtime)
                
                problems.append({
                    'name': item.name,
                    'date': commit_date,
                    'folder_path': str(item),
                    'source': 'folder'
                })
                print(f"  ✅ Found: {item.name} ({commit_date.strftime('%Y-%m-%d')})")
        
        print(f"\n📊 Total problems found: {len(problems)}")
        return problems

    def _get_commit_dates_for_folders(self):
        """
        Get the last commit date for each problem folder by scanning Git history.
        This is more accurate than using file modification times.
        """
        if self.repo is None:
            self.repo = git.Repo(self.repo_path)
        
        commit_dates = {}
        
        print("  📅 Getting commit dates from Git history...")
        
        # Walk through commits and track which problem folders they affect
        for commit in self.repo.iter_commits():
            try:
                # Check stats to see which files were changed
                for file_path in commit.stats.files.keys():
                    # Look for folder names that match LeetCode problem pattern
                    parts = file_path.split('/')
                    for part in parts:
                        if re.match(r'^\d+-[\w-]+', part):
                            problem_name = part
                            if problem_name not in commit_dates:
                                commit_dates[problem_name] = commit.committed_datetime
                            elif commit.committed_datetime > commit_dates[problem_name]:
                                commit_dates[problem_name] = commit.committed_datetime
            except Exception:
                # Some commits might not have stats (e.g., merge commits)
                continue
        
        # Also check commit messages for folder names
        for commit in self.repo.iter_commits():
            try:
                message = commit.message
                for problem in self.repo_path.iterdir():
                    if problem.is_dir() and re.match(r'^\d+-[\w-]+', problem.name):
                        if problem.name in message:
                            if problem.name not in commit_dates:
                                commit_dates[problem.name] = commit.committed_datetime
            except Exception:
                continue
        
        # If still missing dates, use the first commit in the repo as fallback
        # (This ensures every problem gets at least a rough date)
        if not commit_dates:
            try:
                first_commit = next(self.repo.iter_commits())
                for problem in self.repo_path.iterdir():
                    if problem.is_dir() and re.match(r'^\d+-[\w-]+', problem.name):
                        if problem.name not in commit_dates:
                            commit_dates[problem.name] = first_commit.committed_datetime
            except StopIteration:
                pass
        
        return commit_dates

    def get_problems_from_commits(self):
        """
        Alternative method: Try to get problem names from commit messages.
        This is a backup method in case folder scanning fails.
        """
        if not self.is_valid_repo():
            return []
        
        try:
            if self.repo is None:
                self.repo = git.Repo(self.repo_path)
            problems = []
            print("🔍 Scanning commit messages...")
            
            for commit in self.repo.iter_commits():
                message = commit.message.strip()
                # Look for problem pattern in commit message
                match = re.search(r'(\d+-[\w-]+)', message)
                if match:
                    problem_name = match.group(1)
                    # Skip false positives like "Time"
                    if problem_name not in ["Time", "Memory"]:
                        problems.append({
                            'name': problem_name,
                            'date': commit.committed_datetime,
                            'source': 'commit'
                        })
                        print(f"  ✅ Found in commit: {problem_name}")
            
            return problems
        except Exception as e:
            print(f"⚠️ Could not read commits: {e}")
            return []
    
    def get_all_problems(self):
        """
        Get all problems with unique names and latest dates.
        Combines both methods and removes duplicates.
        """
        # Try folders first (most reliable)
        folder_problems = self.get_problems_from_folders()
        
        # If no folders found, try commits
        if not folder_problems:
            print("No folders found, trying commits...")
            folder_problems = self.get_problems_from_commits()
        
        # Remove duplicates (keep the latest date for each problem)
        unique_problems = {}
        for problem in folder_problems:
            name = problem['name']
            if name not in unique_problems or problem['date'] > unique_problems[name]['date']:
                unique_problems[name] = problem
        
        # Sort by date (newest first)
        result = sorted(unique_problems.values(), key=lambda x: x['date'], reverse=True)
        
        self.problems = result
        return result
    
    def get_problem_dates(self):
        """
        Get a dictionary of problem names and their latest solve dates.
        Useful for quick lookups.
        """
        problems = self.get_all_problems()
        return {p['name']: p['date'] for p in problems}

# Quick test
if __name__ == "__main__":
    parser = GitParser()
    if parser.is_valid_repo():
        problems = parser.get_all_problems()
        
        print("\n📋 Recent Problems:")
        for i, p in enumerate(problems[:10], 1):
            print(f"  {i}. {p['name']} - {p['date'].strftime('%Y-%m-%d')}")
        
        print(f"\n📊 Total: {len(problems)} problems")
    else:
        print("Please clone your repository first!")
        print("Run: git clone https://github.com/nrezwan/LeetCode_Solutions.git")