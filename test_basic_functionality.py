#!/usr/bin/env python3
"""
Test basic SWE-smith functionality
"""
import os
import shutil
from pathlib import Path

def test_entity_extraction():
    """Test entity extraction from Python code"""
    print("🔍 Testing entity extraction...")
    
    # Create test repository structure
    test_repo = Path("test_repo")
    test_repo.mkdir(exist_ok=True)
    
    # Create sample Python files
    sample_code = {
        "calculator.py": '''
def add(a, b):
    """Add two numbers."""
    return a + b

def subtract(a, b):
    """Subtract b from a."""
    if a < b:
        print("Warning: result will be negative")
    return a - b

class Calculator:
    """A simple calculator class."""
    
    def __init__(self):
        self.history = []
    
    def calculate(self, op, x, y):
        """Perform calculation and store in history."""
        if op == "add":
            result = add(x, y)
        elif op == "sub":
            result = subtract(x, y)
        else:
            result = 0
        
        self.history.append((op, x, y, result))
        return result
''',
        "utils.py": '''
def is_even(n):
    """Check if number is even."""
    return n % 2 == 0

def factorial(n):
    """Calculate factorial."""
    if n <= 1:
        return 1
    return n * factorial(n - 1)
'''
    }
    
    # Write test files
    for filename, content in sample_code.items():
        (test_repo / filename).write_text(content)
    
    # Test entity extraction
    from swesmith.bug_gen.utils import extract_entities_from_directory
    
    entities = extract_entities_from_directory(str(test_repo))
    
    print(f"   Found {len(entities)} entities:")
    for entity in entities:
        print(f"   - {entity.name} ({type(entity).__name__}) in {entity.file_path}")
        print(f"     Lines {entity.line_start}-{entity.line_end}, Complexity: {entity.complexity}")
    
    # Clean up
    shutil.rmtree(test_repo)
    
    if len(entities) > 0:
        print("   ✅ Entity extraction working!")
        return True
    else:
        print("   ❌ No entities found")
        return False

def test_procedural_modifications():
    """Test procedural modification techniques"""
    print("\n🛠️  Testing procedural modification techniques...")
    
    try:
        from swesmith.bug_gen.procedural.generate import PM_TECHNIQUES
        
        print(f"   Found {len(PM_TECHNIQUES)} procedural modification techniques:")
        for i, technique in enumerate(PM_TECHNIQUES[:5]):  # Show first 5
            print(f"   {i+1}. {technique.name}")
            print(f"      {technique.explanation[:60]}...")
        
        if len(PM_TECHNIQUES) > 5:
            print(f"   ... and {len(PM_TECHNIQUES) - 5} more")
        
        print("   ✅ Procedural modifications loaded!")
        return True
    except Exception as e:
        print(f"   ❌ Error loading procedural modifications: {e}")
        return False

def test_repository_profiles():
    """Test repository profile system"""
    print("\n📁 Testing repository profiles...")
    
    try:
        from swesmith.profiles import global_registry
        
        # Get a sample of repositories
        all_repos = [k for k in global_registry.keys() if '/' in k]
        sample_repos = all_repos[:5]
        
        print(f"   Found {len(all_repos)} repositories. Sample:")
        for repo in sample_repos:
            try:
                profile = global_registry.get(repo)
                print(f"   - {repo}")
                print(f"     Owner: {profile.owner}, Repo: {profile.repo}")
                print(f"     Test command: {profile.test_cmd[:50]}...")
            except Exception as e:
                print(f"   - {repo}: Error loading profile - {e}")
        
        print("   ✅ Repository profiles working!")
        return True
    except Exception as e:
        print(f"   ❌ Error with repository profiles: {e}")
        return False

def test_bug_generation_setup():
    """Test if bug generation components are ready"""
    print("\n🐛 Testing bug generation setup...")
    
    try:
        # Test LLM utils
        from swesmith.bug_gen.llm.utils import extract_code_block
        test_text = "Here's some code:\n```python\nprint('hello')\n```"
        extracted = extract_code_block(test_text)
        
        if extracted == "print('hello')":
            print("   ✅ LLM code extraction working!")
        else:
            print("   ⚠️  LLM code extraction might have issues")
        
        # Test procedural modification imports
        from swesmith.bug_gen.procedural.control_flow import ControlIfElseInvertModifier
        from swesmith.bug_gen.procedural.operations import OperationChangeModifier
        
        print("   ✅ Bug generation components imported successfully!")
        return True
    except Exception as e:
        print(f"   ❌ Error with bug generation setup: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing SWE-smith Basic Functionality")
    print("=" * 50)
    
    tests = [
        test_entity_extraction,
        test_procedural_modifications,
        test_repository_profiles,
        test_bug_generation_setup,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"   ❌ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 All {total} tests passed! SWE-smith is ready to use.")
        print("\n🚀 You can now try:")
        print("   • Generate procedural bugs for a repository")
        print("   • Create LLM-generated bugs") 
        print("   • Set up execution environments")
    else:
        print(f"⚠️  {passed}/{total} tests passed. Some functionality may not work correctly.")
    
    print(f"\n💡 Next steps:")
    print("   1. Try running procedural bug generation on a test repository")
    print("   2. Set up Docker environments for validation")
    print("   3. Generate your first task instances!")