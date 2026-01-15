#!/usr/bin/env python3
"""
Generate nodes.json from dora-hub node-hub directory.

This script scans all nodes in the dora-hub repository and generates
a JSON file with metadata for each node.

Usage:
    # Using GitHub API (no clone needed):
    python generate_nodes_json.py --github

    # Using local clone:
    git clone https://github.com/dora-rs/dora-hub.git
    python generate_nodes_json.py --local ./dora-hub/node-hub

    # Specify output file:
    python generate_nodes_json.py --github --output nodes.json
"""

import json
import os
import sys
import argparse
import re
from pathlib import Path
from typing import Dict, List, Optional, Union
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.parse import quote


class NodeScanner:
    """Scanner for dora-hub nodes to extract metadata."""

    def __init__(self, github_token: Optional[str] = None):
        self.github_token = github_token or os.environ.get("GITHUB_TOKEN")
        self.base_api_url = "https://api.github.com/repos/dora-rs/dora-hub"
        self.base_raw_url = "https://raw.githubusercontent.com/dora-rs/dora-hub/main"

    def _make_github_request(self, url: str) -> Union[Dict, List]:
        """Make a request to GitHub API with optional authentication."""
        headers = {"Accept": "application/vnd.github.v3+json"}
        if self.github_token:
            headers["Authorization"] = f"token {self.github_token}"

        req = Request(url, headers=headers)
        try:
            with urlopen(req) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            print(f"Error fetching {url}: {e}", file=sys.stderr)
            return [] if "contents" in url else {}

    def _extract_metadata_from_readme(self, readme_content: str) -> Dict[str, str]:
        """Extract metadata from README.md content."""
        metadata = {
            "title": "",
            "description": "",
            "install": "",
            "category": "",
        }

        lines = readme_content.split("\n")

        # Extract title (first # heading)
        for line in lines:
            if line.startswith("# "):
                metadata["title"] = line[2:].strip()
                break

        # Extract description (first paragraph after title)
        description_lines = []
        in_description = False
        for line in lines:
            if metadata["title"] and line.strip() and not line.startswith("#"):
                in_description = True
            if in_description:
                if line.startswith("#") or line.startswith("```"):
                    break
                if line.strip():
                    description_lines.append(line.strip())
                elif description_lines:
                    break
        metadata["description"] = " ".join(description_lines[:3])  # First 3 lines

        # Extract install instructions
        install_pattern = re.search(
            r"(?:##\s*Install|##\s*Installation|```bash\s*)(pip install [^\n]+|cargo install [^\n]+)",
            readme_content,
            re.IGNORECASE
        )
        if install_pattern:
            metadata["install"] = install_pattern.group(1).strip()

        return metadata

    def _extract_metadata_from_cargo_toml(self, content: str) -> Dict[str, str]:
        """Extract metadata from Cargo.toml."""
        metadata = {}

        # Extract package name
        name_match = re.search(r'name\s*=\s*"([^"]+)"', content)
        if name_match:
            metadata["title"] = name_match.group(1)

        # Extract description
        desc_match = re.search(r'description\s*=\s*"([^"]+)"', content)
        if desc_match:
            metadata["description"] = desc_match.group(1)

        # Extract license
        license_match = re.search(r'license\s*=\s*"([^"]+)"', content)
        if license_match:
            metadata["license"] = license_match.group(1)

        # Extract authors
        authors_match = re.search(r'authors\s*=\s*\[([^\]]+)\]', content)
        if authors_match:
            authors = authors_match.group(1).strip()
            # Extract first author
            author_match = re.search(r'"([^"]+)"', authors)
            if author_match:
                metadata["author"] = author_match.group(1)

        return metadata

    def _extract_metadata_from_package_json(self, content: str) -> Dict[str, str]:
        """Extract metadata from package.json."""
        try:
            data = json.loads(content)
            metadata = {}

            if "name" in data:
                metadata["title"] = data["name"]
            if "description" in data:
                metadata["description"] = data["description"]
            if "license" in data:
                metadata["license"] = data["license"]
            if "author" in data:
                metadata["author"] = data["author"] if isinstance(data["author"], str) else data["author"].get("name", "")

            return metadata
        except json.JSONDecodeError:
            return {}

    def _extract_metadata_from_pyproject_toml(self, content: str) -> Dict[str, str]:
        """Extract metadata from pyproject.toml."""
        metadata = {}

        # Extract name
        name_match = re.search(r'name\s*=\s*"([^"]+)"', content)
        if name_match:
            metadata["title"] = name_match.group(1)

        # Extract description
        desc_match = re.search(r'description\s*=\s*"([^"]+)"', content)
        if desc_match:
            metadata["description"] = desc_match.group(1)

        # Extract license
        license_match = re.search(r'license\s*=\s*"([^"]+)"', content)
        if license_match:
            metadata["license"] = license_match.group(1)

        # Extract authors
        authors_match = re.search(r'authors\s*=\s*\[([^\]]+)\]', content)
        if authors_match:
            authors = authors_match.group(1).strip()
            author_match = re.search(r'"([^"]+)"', authors)
            if author_match:
                metadata["author"] = author_match.group(1)

        return metadata

    def _infer_tags(self, node_name: str, readme_content: str, metadata: Dict) -> List[str]:
        """Infer tags based on node name and content."""
        tags = []

        node_lower = node_name.lower()
        readme_lower = readme_content.lower()

        # Language tags
        if "python" in readme_lower or ".py" in readme_lower:
            tags.append("python")
        if "rust" in readme_lower or "cargo" in readme_lower:
            tags.append("rust")

        # Media type tags
        if any(word in node_lower or word in readme_lower
               for word in ["camera", "image", "vision", "yolo", "detection", "segment"]):
            tags.append("image")
        if any(word in node_lower or word in readme_lower
               for word in ["video", "stream", "opencv"]):
            tags.append("video")
        if any(word in node_lower or word in readme_lower
               for word in ["audio", "microphone", "speaker", "sound", "whisper", "tts"]):
            tags.append("audio")
        if any(word in node_lower or word in readme_lower
               for word in ["depth", "realsense", "3d", "point cloud"]):
            tags.append("depth")
        if any(word in node_lower or word in readme_lower
               for word in ["control", "robot", "servo", "motor", "arm"]):
            tags.append("control")

        return list(set(tags))  # Remove duplicates

    def _get_node_metadata_github(self, node_name: str) -> Optional[Dict]:
        """Get metadata for a single node using GitHub API."""
        node_path = f"node-hub/{node_name}"

        # Get file list in node directory
        contents_url = f"{self.base_api_url}/contents/{node_path}"
        files = self._make_github_request(contents_url)

        if not files:
            return None

        # Initialize node data
        node_data = {
            "title": node_name,
            "description": "",
            "preview": None,
            "author": None,
            "github": "https://github.com/dora-rs/dora-hub",
            "downloads": None,
            "last_commit": None,
            "last_release": None,
            "license": None,
            "install": None,
            "category": None,
            "website": node_name,
            "source": f"https://github.com/dora-rs/dora-hub/tree/main/{node_path}",
            "tags": []
        }

        # Read available files
        readme_content = ""
        for file in files:
            if not isinstance(file, dict):
                continue

            file_name = file.get("name", "")
            download_url = file.get("download_url", "")

            if not download_url:
                continue

            try:
                with urlopen(download_url) as response:
                    content = response.read().decode("utf-8", errors="ignore")

                    if file_name.upper() == "README.MD":
                        readme_content = content
                        metadata = self._extract_metadata_from_readme(content)
                        node_data.update(metadata)

                    elif file_name == "Cargo.toml":
                        metadata = self._extract_metadata_from_cargo_toml(content)
                        # Only update if not already set from README
                        for key, value in metadata.items():
                            if not node_data.get(key):
                                node_data[key] = value

                    elif file_name == "package.json":
                        metadata = self._extract_metadata_from_package_json(content)
                        for key, value in metadata.items():
                            if not node_data.get(key):
                                node_data[key] = value

                    elif file_name == "pyproject.toml":
                        metadata = self._extract_metadata_from_pyproject_toml(content)
                        for key, value in metadata.items():
                            if not node_data.get(key):
                                node_data[key] = value

            except Exception as e:
                print(f"Error reading {file_name} in {node_name}: {e}", file=sys.stderr)

        # Infer tags
        node_data["tags"] = self._infer_tags(node_name, readme_content, node_data)

        # Get last commit date
        try:
            commits_url = f"{self.base_api_url}/commits?path={node_path}&per_page=1"
            commits = self._make_github_request(commits_url)
            if commits and len(commits) > 0:
                commit_date = commits[0].get("commit", {}).get("committer", {}).get("date")
                if commit_date:
                    node_data["last_commit"] = commit_date
        except Exception as e:
            print(f"Error getting commit info for {node_name}: {e}", file=sys.stderr)

        return node_data

    def _get_node_metadata_local(self, node_path: Path) -> Optional[Dict]:
        """Get metadata for a single node from local filesystem."""
        if not node_path.is_dir():
            return None

        node_name = node_path.name

        # Initialize node data
        node_data = {
            "title": node_name,
            "description": "",
            "preview": None,
            "author": None,
            "github": "https://github.com/dora-rs/dora-hub",
            "downloads": None,
            "last_commit": None,
            "last_release": None,
            "license": None,
            "install": None,
            "category": None,
            "website": node_name,
            "source": f"https://github.com/dora-rs/dora-hub/tree/main/node-hub/{node_name}",
            "tags": []
        }

        readme_content = ""

        # Read README.md
        readme_path = node_path / "README.md"
        if readme_path.exists():
            try:
                with open(readme_path, "r", encoding="utf-8") as f:
                    readme_content = f.read()
                    metadata = self._extract_metadata_from_readme(readme_content)
                    node_data.update(metadata)
            except Exception as e:
                print(f"Error reading README for {node_name}: {e}", file=sys.stderr)

        # Read Cargo.toml
        cargo_path = node_path / "Cargo.toml"
        if cargo_path.exists():
            try:
                with open(cargo_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    metadata = self._extract_metadata_from_cargo_toml(content)
                    for key, value in metadata.items():
                        if not node_data.get(key):
                            node_data[key] = value
            except Exception as e:
                print(f"Error reading Cargo.toml for {node_name}: {e}", file=sys.stderr)

        # Read package.json
        package_path = node_path / "package.json"
        if package_path.exists():
            try:
                with open(package_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    metadata = self._extract_metadata_from_package_json(content)
                    for key, value in metadata.items():
                        if not node_data.get(key):
                            node_data[key] = value
            except Exception as e:
                print(f"Error reading package.json for {node_name}: {e}", file=sys.stderr)

        # Read pyproject.toml
        pyproject_path = node_path / "pyproject.toml"
        if pyproject_path.exists():
            try:
                with open(pyproject_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    metadata = self._extract_metadata_from_pyproject_toml(content)
                    for key, value in metadata.items():
                        if not node_data.get(key):
                            node_data[key] = value
            except Exception as e:
                print(f"Error reading pyproject.toml for {node_name}: {e}", file=sys.stderr)

        # Infer tags
        node_data["tags"] = self._infer_tags(node_name, readme_content, node_data)

        return node_data

    def scan_nodes_github(self) -> List[Dict]:
        """Scan all nodes using GitHub API."""
        print("Fetching node list from GitHub...", file=sys.stderr)
        contents_url = f"{self.base_api_url}/contents/node-hub"
        contents = self._make_github_request(contents_url)

        if not contents:
            print("Error: Could not fetch node-hub contents", file=sys.stderr)
            return []

        nodes = []
        node_dirs = [item for item in contents if isinstance(item, dict) and item.get("type") == "dir"]

        print(f"Found {len(node_dirs)} nodes. Scanning...", file=sys.stderr)

        for i, item in enumerate(node_dirs, 1):
            node_name = item.get("name")
            if node_name:
                print(f"[{i}/{len(node_dirs)}] Scanning {node_name}...", file=sys.stderr)
                node_data = self._get_node_metadata_github(node_name)
                if node_data:
                    nodes.append(node_data)

        return nodes

    def scan_nodes_local(self, node_hub_path: str) -> List[Dict]:
        """Scan all nodes from local filesystem."""
        node_hub = Path(node_hub_path)

        if not node_hub.exists() or not node_hub.is_dir():
            print(f"Error: {node_hub_path} does not exist or is not a directory", file=sys.stderr)
            return []

        print(f"Scanning local directory: {node_hub_path}", file=sys.stderr)

        nodes = []
        node_dirs = [d for d in node_hub.iterdir() if d.is_dir() and not d.name.startswith(".")]

        print(f"Found {len(node_dirs)} nodes. Scanning...", file=sys.stderr)

        for i, node_dir in enumerate(sorted(node_dirs), 1):
            print(f"[{i}/{len(node_dirs)}] Scanning {node_dir.name}...", file=sys.stderr)
            node_data = self._get_node_metadata_local(node_dir)
            if node_data:
                nodes.append(node_data)

        return nodes


def main():
    parser = argparse.ArgumentParser(
        description="Generate nodes.json from dora-hub node-hub directory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--github", action="store_true", help="Fetch from GitHub API")
    group.add_argument("--local", type=str, help="Path to local node-hub directory")

    parser.add_argument("--output", "-o", type=str, default="nodes.json",
                        help="Output JSON file (default: nodes.json)")
    parser.add_argument("--token", type=str, help="GitHub API token (or use GITHUB_TOKEN env var)")

    args = parser.parse_args()

    scanner = NodeScanner(github_token=args.token)

    if args.github:
        nodes = scanner.scan_nodes_github()
    else:
        nodes = scanner.scan_nodes_local(args.local)

    if not nodes:
        print("Error: No nodes found", file=sys.stderr)
        return 1

    # Sort by title
    nodes.sort(key=lambda x: x["title"])

    # Write to file
    output_path = Path(args.output)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(nodes, f, indent=2, ensure_ascii=False)

    print(f"\nSuccess! Generated {output_path} with {len(nodes)} nodes.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
