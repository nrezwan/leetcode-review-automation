# test_parser.py - Test the git parser
import sys
from pathlib import Path

# Add current directory to path so Python can find our modules
sys.path.insert(0, str(Path(__file__).parent))

# Now import from the same directory
from git_parser import GitParser 

def main():
    print("🧪 Testing Git Parser")  
    print("=" * 50)
    
    parser = GitParser("./LeetCode_Solutions")
    
    if not parser.is_valid_repo():
        print("❌ Repository not found!")
        print("💡 Run: git clone https://github.com/nrezwan/LeetCode_Solutions.git")
        return
    
    # Test getting all problems
    problems = parser.get_all_problems()
    
    print(f"\n📊 Total problems found: {len(problems)}")
    
    if problems:
        print("\n📋 First 5 problems:")
        for i, p in enumerate(problems[:5], 1):
            date_str = p['date'].strftime('%Y-%m-%d %H:%M')
            print(f"  {i}. {p['name']} - {date_str}")
        
        print(f"\n📅 Latest problem: {problems[0]['name']} ({problems[0]['date'].strftime('%Y-%m-%d')})")
        print(f"📅 Oldest problem: {problems[-1]['name']} ({problems[-1]['date'].strftime('%Y-%m-%d')})")
        
        # Test problem dates lookup
        dates = parser.get_problem_dates()
        print(f"\n📋 Problem dates lookup ready ({len(dates)} entries)")
    
    print("\n✅ Test complete!")

if __name__ == "__main__":
    main()