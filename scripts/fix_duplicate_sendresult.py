#!/usr/bin/env python3
"""
Script to fix duplicate code in sendResult function in quiz HTML files.
Removes:
1. Trailing comma after function closing brace (line with "},")
2. Duplicate body/JSON.stringify blocks
3. Orphaned query string code at function end
"""

import os
import re
from pathlib import Path

WEB_DIR = Path(__file__).parent.parent / "Web"

def fix_file(file_path):
    """Fix duplicate code in a single HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern 1: Find the sendResult function and remove everything after the proper closing
        # We need to find: async function sendResult(...) { ... } followed by "}," and duplicate code
        
        # Strategy: Find the function start, then find the first proper closing "}" 
        # and remove everything after until we hit the restart-btn handler
        
        lines = content.split('\n')
        new_lines = []
        i = 0
        in_sendResult = False
        brace_count = 0
        function_start = -1
        
        while i < len(lines):
            line = lines[i]
            
            # Detect start of sendResult function
            if 'async function sendResult' in line:
                in_sendResult = True
                function_start = i
                brace_count = 0
                new_lines.append(line)
                # Count opening brace
                brace_count += line.count('{') - line.count('}')
                i += 1
                continue
            
            if in_sendResult:
                # Count braces
                brace_count += line.count('{') - line.count('}')
                new_lines.append(line)
                
                # Check if function should end (brace_count == 0)
                if brace_count == 0:
                    # Check if next line is problematic
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        
                        # Pattern 1: Line is just "},"
                        if next_line == '},':
                            # Skip the comma line and all duplicate code until we find restart-btn
                            i += 1
                            while i + 1 < len(lines):
                                line_check = lines[i + 1]
                                # Stop when we hit restart-btn handler or proper function end
                                if 'restart-btn' in line_check or 'showQuestion()' in line_check:
                                    break
                                # Stop if we see a clean closing brace on its own line
                                if line_check.strip() == '}' and 'function' not in lines[i]:
                                    i += 1
                                    break
                                i += 1
                            in_sendResult = False
                            continue
                        
                        # Pattern 2: Next line starts with "body:" (duplicate)
                        elif next_line.startswith('body:') or next_line.startswith('body :'):
                            # Skip duplicate code
                            i += 1
                            while i < len(lines):
                                line_check = lines[i]
                                # Stop when we see restart-btn or showQuestion
                                if 'restart-btn' in line_check or 'showQuestion()' in line_check:
                                    break
                                # Stop at clean closing brace
                                if line_check.strip() == '}' and brace_count == 0:
                                    break
                                # Stop at query string pattern
                                if '}?student_name=' in line_check:
                                    i += 1
                                    # Skip the fetch line too
                                    while i < len(lines) and ('await fetch' in lines[i] or 'send-status' in lines[i] or '}catch' in lines[i]):
                                        i += 1
                                    break
                                i += 1
                            in_sendResult = False
                            continue
                    
                    in_sendResult = False
            else:
                new_lines.append(line)
            
            i += 1
        
        content = '\n'.join(new_lines)
        
        # Second pass: Remove orphaned query string patterns
        # Pattern: }?student_name=... followed by fetch/await code
        content = re.sub(
            r'\s*\}\?student_name=[^`]*`;\s*(?:await fetch\([^)]+\)[^;]*;)?\s*(?:document\.getElementById\([^)]+\)[^;]*;)?\s*(?:\}catch\([^)]+\)\{[^}]*\})?\s*\}?\s*',
            '\n',
            content,
            flags=re.MULTILINE
        )
        
        # Third pass: Fix any remaining "}," that should be "}"
        # But only if it's at the end of sendResult function context
        lines = content.split('\n')
        fixed_lines = []
        for i, line in enumerate(lines):
            # If line is just "}," check if it's part of sendResult function
            if line.strip() == '},':
                # Check previous lines for sendResult context
                prev_context = '\n'.join(lines[max(0, i-20):i])
                if 'async function sendResult' in prev_context and 'getElementById(\'send-status\')' in prev_context:
                    # Replace with just "}"
                    fixed_lines.append('    }')
                    continue
            fixed_lines.append(line)
        
        content = '\n'.join(fixed_lines)
        
        # Only write if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function to fix all HTML files."""
    html_files = sorted(list(WEB_DIR.glob("*.html")))
    
    print(f"Found {len(html_files)} HTML files to check...")
    
    fixed_files = []
    for html_file in html_files:
        if fix_file(html_file):
            print(f"✅ Fixed: {html_file.name}")
            fixed_files.append(html_file.name)
    
    print(f"\n✅ Fixed {len(fixed_files)} files out of {len(html_files)} total files.")
    
    if fixed_files:
        print("\nFixed files:")
        for f in fixed_files:
            print(f"  - {f}")

if __name__ == "__main__":
    main()
