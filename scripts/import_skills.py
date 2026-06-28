import os
import re
import sys
import shutil
import urllib.request
import urllib.parse
import subprocess
import tempfile
import hashlib
import json

# Setup logger-like output
def log_info(msg):
    print(f"[INFO] {msg}", flush=True)

def log_warn(msg):
    print(f"[WARN] {msg}", flush=True)

def log_error(msg):
    print(f"[ERROR] {msg}", flush=True)

# Malware / Safety checks
BLOCKED_EXTENSIONS = {
    '.exe', '.dll', '.bat', '.cmd', '.sh', '.bin', '.msi', '.com', '.vbs', '.js', '.py'
}

SUSPICIOUS_PATTERNS = [
    re.compile(rb'eval\s*\('),
    re.compile(rb'exec\s*\('),
    re.compile(rb'subprocess\s*\.'),
    re.compile(rb'os\s*\.\s*system'),
    re.compile(rb'__import__'),
    re.compile(rb'powershell'),
    re.compile(rb'base64\.b64decode'),
    re.compile(rb'shutil\s*\.'),
    re.compile(rb'urllib\s*\.\s*request'),
    re.compile(rb'requests\s*\.\s*get'),
]

def scan_file_for_safety(file_path):
    """Scans a file for binary extensions or suspicious script patterns.
    
    Returns: (is_safe, reason)
    """
    _, ext = os.path.splitext(file_path.lower())
    if ext in BLOCKED_EXTENSIONS:
        # We allow .js and .py ONLY if they are inside component directories and clean,
        # but for knowledge input, we generally block code scripts unless they are TSX/JSX components.
        if ext in ['.js', '.py']:
            log_warn(f"Script file detected: {file_path}. Scanning contents...")
        else:
            return False, f"Blocked extension: {ext}"

    # Read binary or text to check for malicious patterns
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
    except Exception as e:
        return False, f"Could not read file: {e}"

    # Simple binary/text heuristic: check for null bytes
    if b'\x00' in content:
        # Check if it's an allowed binary format (none expected for skill texts)
        if ext not in ['.png', '.jpg', '.jpeg', '.gif', '.glb', '.gltf']:
            return False, "Suspicious binary file structure"

    # Check for executable code injection patterns
    for pattern in SUSPICIOUS_PATTERNS:
        match = pattern.search(content)
        if match:
            # We flag it, but allow markdown files to explain commands as text code blocks
            # If it's a script (.py, .js) with execution patterns, we block it.
            if ext in ['.py', '.js', '.sh', '.bat']:
                return False, f"Suspicious script pattern found: {match.group(0)}"
            else:
                log_warn(f"Pattern {match.group(0)} found in text file {file_path} (likely in code block). Proceeding with caution.")

    return True, "Safe"


def convert_github_to_raw(url):
    """Converts a standard GitHub file URL to raw.githubusercontent.com URL."""
    # Example: https://github.com/user/repo/blob/main/path/to/file.md
    # Raw: https://raw.githubusercontent.com/user/repo/main/path/to/file.md
    m = re.match(r'https?://(?:www\.)?github\.com/([^/]+)/([^/]+)/blob/([^/]+)/(.+)', url)
    if m:
        user, repo, branch, path = m.groups()
        # Clean any trailing query parameters like ?plain=1
        path = path.split('?')[0]
        return f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/{path}"
    return url


def process_url(url, base_dir, temp_dir):
    """Processes a single URL by downloading files or cloning repositories,
    scanning them, and placing them in knowledge_input/ folders.
    """
    log_info(f"Processing URL: {url}")
    
    # Check if GitHub URL
    if 'github.com' in url or 'githubusercontent.com' in url:
        # Case A: GitHub blob (specific file)
        if '/blob/' in url:
            raw_url = convert_github_to_raw(url)
            try:
                log_info(f"Downloading file from: {raw_url}")
                # Parse filename
                parsed_url = urllib.parse.urlparse(raw_url)
                file_name = os.path.basename(parsed_url.path)
                
                # Make name unique based on repo and path
                parts = parsed_url.path.strip('/').split('/')
                # parts example: ['user', 'repo', 'branch', 'path', 'to', 'file.md']
                if len(parts) >= 4:
                    unique_name = f"{parts[0]}-{parts[1]}-{'-'.join(parts[3:])}"
                else:
                    unique_name = f"downloaded-{file_name}"
                
                temp_file_path = os.path.join(temp_dir, unique_name)
                urllib.request.urlretrieve(raw_url, temp_file_path)
                
                # Safety scan
                is_safe, reason = scan_file_for_safety(temp_file_path)
                if not is_safe:
                    log_error(f"Security hazard! Skipped file {unique_name}: {reason}")
                    return
                
                # Copy to appropriate folder
                dest_folder = "references"
                if unique_name.lower().endswith('skill.md'):
                    dest_folder = "skills"
                elif 'design' in unique_name.lower() or 'theme' in unique_name.lower():
                    dest_folder = "design_systems"
                
                dest_path = os.path.join(base_dir, "knowledge_input", dest_folder, unique_name)
                shutil.copy2(temp_file_path, dest_path)
                log_info(f"Saved: {dest_folder}/{unique_name}")
                
            except Exception as e:
                log_error(f"Failed to download specific file {url}: {e}")
        
        # Case B: General GitHub Repository
        else:
            # Clean repository URL
            # Example: https://github.com/user/repo/tree/main or https://github.com/user/repo
            m = re.match(r'https?://(?:www\.)?github\.com/([^/]+)/([^/]+)', url)
            if m:
                user, repo = m.groups()
                repo = repo.split('/')[0].replace('.git', '')
                repo_url = f"https://github.com/{user}/{repo}"
                repo_dir = os.path.join(temp_dir, f"{user}-{repo}")
                
                log_info(f"Cloning repo: {repo_url}...")
                try:
                    # Clone repository using shallow clone
                    result = subprocess.run(
                        ["git", "clone", "--depth", "1", repo_url, repo_dir],
                        capture_output=True, text=True, check=True
                    )
                    
                    # Scan for skills or markdown files
                    count = 0
                    for root, _, files in os.walk(repo_dir):
                        # Skip git directory
                        if '.git' in root.split(os.sep):
                            continue
                            
                        for f in files:
                            # We search for SKILL.md, *.md, *.yaml, *.json
                            f_lower = f.lower()
                            if f_lower == 'skill.md' or f_lower.endswith('.skill') or f_lower.endswith('.md') or f_lower.endswith('.yaml') or f_lower.endswith('.yml') or f_lower.endswith('.json'):
                                file_path = os.path.join(root, f)
                                
                                # Safety scan
                                is_safe, reason = scan_file_for_safety(file_path)
                                if not is_safe:
                                    log_error(f"Security hazard! Skipped repo file {f} in {user}/{repo}: {reason}")
                                    continue
                                
                                # Make name unique
                                rel_path = os.path.relpath(file_path, repo_dir)
                                unique_name = f"{user}-{repo}-{rel_path.replace(os.sep, '-')}"
                                
                                # Determine category
                                dest_folder = "references"
                                if f_lower == 'skill.md' or 'skills' in rel_path.lower():
                                    dest_folder = "skills"
                                elif 'design' in f_lower or 'theme' in f_lower or 'design_systems' in rel_path.lower():
                                    dest_folder = "design_systems"
                                
                                dest_path = os.path.join(base_dir, "knowledge_input", dest_folder, unique_name)
                                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                                shutil.copy2(file_path, dest_path)
                                count += 1
                    
                    log_info(f"Repo {user}/{repo} processed. Integrated {count} files.")
                    
                except Exception as e:
                    log_error(f"Failed to clone/process repository {repo_url}: {e}")
            else:
                log_warn(f"GitHub URL could not be parsed: {url}")
                
    # Case C: External non-GitHub website (Aura build, Skills sh, etc.)
    else:
        # Create external link reference file
        log_info(f"Logging external link: {url}")
        ref_file = os.path.join(base_dir, "knowledge_input", "references", "external-links.txt")
        try:
            with open(ref_file, "a", encoding="utf-8") as f:
                f.write(f"{url}\n")
        except Exception as e:
            log_error(f"Failed to log external reference link: {e}")


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    txt_path = os.path.join(base_dir, "Banco_Aprendizado", "Skills & Inspiration.txt")
    
    if not os.path.exists(txt_path):
        log_error(f"File not found: {txt_path}")
        sys.exit(1)
        
    log_info("Starting Import Skills Script...")
    
    # 1. Parse text file and extract unique URLs
    urls = []
    url_pattern = re.compile(r'https?://[^\s]+')
    
    with open(txt_path, 'r', encoding='utf-8') as f:
        for line in f:
            found = url_pattern.findall(line)
            if found:
                urls.extend(found)
                
    unique_urls = sorted(list(set(urls)))
    log_info(f"Found {len(unique_urls)} unique URLs to process.")
    
    # 2. Setup temporary directory for downloads and clones
    temp_dir = os.path.join(base_dir, "scratch", "temp_repos")
    os.makedirs(temp_dir, exist_ok=True)
    
    # 3. Ensure knowledge_input subfolders exist
    for folder in ["skills", "design_systems", "references"]:
        os.makedirs(os.path.join(base_dir, "knowledge_input", folder), exist_ok=True)
        
    # 4. Process each URL
    for url in unique_urls:
        try:
            process_url(url, base_dir, temp_dir)
        except Exception as err:
            log_error(f"Unhandled error processing {url}: {err}")
            
    # 5. Clean up temp folder
    try:
        shutil.rmtree(temp_dir)
        log_info("Temporary repository clones deleted.")
    except Exception as cleanup_err:
        log_warn(f"Failed to delete temp dir {temp_dir}: {cleanup_err}")
        
    log_info("Import script completed successfully!")

if __name__ == "__main__":
    main()
