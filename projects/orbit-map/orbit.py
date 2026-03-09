#!/usr/bin/env python3
"""
orbit.py - Map conceptual gravity across artifacts

Reads workbench index and reveals:
- Orbit centers (strongest gravitational pull)
- Theme clusters (artifacts orbiting similar concepts)
- Artifact relationships (what orbits what)
- System topology (kinds, modes, themes)

Text-first. No fancy rendering. Just signal.
"""

import json
import sys
from collections import defaultdict, Counter
from pathlib import Path
from typing import Dict, List, Set


class OrbitMap:
    def __init__(self, index_path: str):
        self.index_path = Path(index_path)
        self.artifacts = []
        self.load_index()
    
    def load_index(self):
        """Load the workbench index"""
        if not self.index_path.exists():
            print(f"❌ Index not found: {self.index_path}", file=sys.stderr)
            sys.exit(1)
        
        with open(self.index_path) as f:
            data = json.load(f)
            self.artifacts = data.get('artifacts', [])
            self.generated_at = data.get('generated_at', 'unknown')
    
    def orbit_centers(self) -> List[tuple]:
        """Find the strongest gravitational centers (most common tags)"""
        tag_counts = Counter()
        
        for artifact in self.artifacts:
            tags = artifact.get('tags') or []
            for tag in tags:
                tag_counts[tag] += 1
        
        return tag_counts.most_common()
    
    def theme_clusters(self) -> Dict[str, List[Dict]]:
        """Group artifacts by shared tags"""
        clusters = defaultdict(list)
        
        for artifact in self.artifacts:
            tags = artifact.get('tags') or []
            for tag in tags:
                clusters[tag].append({
                    'title': artifact.get('title'),
                    'kind': artifact.get('kind'),
                    'mode': artifact.get('mode', ''),
                    'path': artifact.get('path')
                })
        
        return dict(clusters)
    
    def artifact_relationships(self) -> List[Dict]:
        """Find artifacts with shared tags (orbital neighbors)"""
        relationships = []
        
        # Build tag -> artifacts mapping
        tag_map = defaultdict(list)
        for artifact in self.artifacts:
            tags = artifact.get('tags') or []
            if tags:  # Only consider artifacts with tags
                for tag in tags:
                    tag_map[tag].append(artifact)
        
        # For each artifact, find its neighbors
        processed = set()
        for artifact in self.artifacts:
            tags = artifact.get('tags') or []
            if not tags:
                continue
            
            title = artifact.get('title')
            neighbors = set()
            
            # Find all artifacts that share any tag
            for tag in tags:
                for neighbor in tag_map[tag]:
                    neighbor_title = neighbor.get('title')
                    if neighbor_title != title:
                        neighbors.add(neighbor_title)
            
            if neighbors:
                rel_key = tuple(sorted([title] + list(neighbors)))
                if rel_key not in processed:
                    relationships.append({
                        'artifact': title,
                        'tags': tags,
                        'orbits_with': sorted(list(neighbors))
                    })
                    processed.add(rel_key)
        
        return relationships
    
    def topology(self) -> Dict:
        """Map the system's topology (kinds, modes, themes)"""
        kinds = Counter()
        modes = Counter()
        tag_count = 0
        tagged_artifacts = 0
        
        for artifact in self.artifacts:
            kind = artifact.get('kind', 'unknown')
            mode = artifact.get('mode', '')
            tags = artifact.get('tags') or []
            
            kinds[kind] += 1
            if mode:
                modes[mode] += 1
            if tags:
                tagged_artifacts += 1
                tag_count += len(tags)
        
        return {
            'total_artifacts': len(self.artifacts),
            'kinds': dict(kinds),
            'modes': dict(modes),
            'tagged_artifacts': tagged_artifacts,
            'total_tags': tag_count,
            'avg_tags_per_artifact': round(tag_count / tagged_artifacts, 2) if tagged_artifacts else 0
        }
    
    def strongest_orbits(self, min_connections: int = 3) -> List[tuple]:
        """Find artifacts with the most orbital connections"""
        connections = Counter()
        
        # Build tag -> artifacts mapping
        tag_map = defaultdict(list)
        for artifact in self.artifacts:
            tags = artifact.get('tags') or []
            if tags:
                for tag in tags:
                    tag_map[tag].append(artifact)
        
        # Count unique connections for each artifact
        for artifact in self.artifacts:
            tags = artifact.get('tags') or []
            if not tags:
                continue
            
            title = artifact.get('title')
            neighbors = set()
            
            for tag in tags:
                for neighbor in tag_map[tag]:
                    neighbor_title = neighbor.get('title')
                    if neighbor_title != title:
                        neighbors.add(neighbor_title)
            
            connections[title] = len(neighbors)
        
        return [(title, count) for title, count in connections.most_common() if count >= min_connections]


def format_orbit_centers(centers: List[tuple]):
    """Text output for orbit centers"""
    print("\n🌌 ORBIT CENTERS (gravitational pull by tag frequency)\n")
    
    if not centers:
        print("  No tags found.")
        return
    
    max_count = centers[0][1] if centers else 1
    
    for tag, count in centers:
        bar_length = int((count / max_count) * 40)
        bar = "█" * bar_length
        print(f"  {tag:20s} {bar} {count}")


def format_theme_clusters(clusters: Dict[str, List[Dict]], top_n: int = 5):
    """Text output for theme clusters"""
    print("\n🌙 THEME CLUSTERS (artifacts orbiting similar concepts)\n")
    
    # Sort by cluster size
    sorted_clusters = sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True)
    
    for theme, artifacts in sorted_clusters[:top_n]:
        print(f"  [{theme}] — {len(artifacts)} artifacts")
        for art in artifacts[:5]:  # Show first 5
            kind_badge = art['kind'][:4].upper()
            mode_str = f"/{art['mode']}" if art['mode'] else ""
            print(f"    • {art['title']} ({kind_badge}{mode_str})")
        if len(artifacts) > 5:
            print(f"    ... and {len(artifacts) - 5} more")
        print()


def format_strongest_orbits(orbits: List[tuple]):
    """Text output for strongest orbital connections"""
    print("\n⭐ STRONGEST ORBITS (artifacts with most connections)\n")
    
    if not orbits:
        print("  No strong orbits found (min 3 connections).")
        return
    
    for title, count in orbits[:10]:
        print(f"  {title:40s} → {count} connections")


def format_topology(topo: Dict):
    """Text output for system topology"""
    print("\n🗺️  SYSTEM TOPOLOGY\n")
    print(f"  Total artifacts: {topo['total_artifacts']}")
    print(f"  Tagged: {topo['tagged_artifacts']} ({topo['avg_tags_per_artifact']} tags/artifact avg)")
    print(f"\n  Kinds:")
    for kind, count in sorted(topo['kinds'].items(), key=lambda x: x[1], reverse=True):
        print(f"    {kind:20s} {count}")
    
    if topo['modes']:
        print(f"\n  Modes:")
        for mode, count in sorted(topo['modes'].items(), key=lambda x: x[1], reverse=True):
            print(f"    {mode:20s} {count}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Map conceptual gravity across sera-foundry artifacts'
    )
    parser.add_argument(
        '--index',
        default='projects/workbench/data/index.json',
        help='Path to workbench index (default: projects/workbench/data/index.json)'
    )
    parser.add_argument(
        '--view',
        choices=['centers', 'clusters', 'orbits', 'topology', 'all'],
        default='all',
        help='What to display (default: all)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output raw JSON instead of formatted text'
    )
    parser.add_argument(
        '--min-connections',
        type=int,
        default=3,
        help='Minimum connections for strongest orbits (default: 3)'
    )
    
    args = parser.parse_args()
    
    # Resolve index path
    if not Path(args.index).is_absolute():
        # Assume relative to sera-foundry root
        base = Path(__file__).parent.parent.parent
        index_path = base / args.index
    else:
        index_path = Path(args.index)
    
    orbit_map = OrbitMap(index_path)
    
    if args.json:
        # Raw JSON output
        output = {}
        if args.view in ['centers', 'all']:
            output['orbit_centers'] = orbit_map.orbit_centers()
        if args.view in ['clusters', 'all']:
            output['theme_clusters'] = orbit_map.theme_clusters()
        if args.view in ['orbits', 'all']:
            output['strongest_orbits'] = orbit_map.strongest_orbits(args.min_connections)
        if args.view in ['topology', 'all']:
            output['topology'] = orbit_map.topology()
        
        print(json.dumps(output, indent=2))
    else:
        # Formatted text output
        print(f"\n✨ ORBIT MAP — generated from {orbit_map.generated_at}\n")
        print("=" * 70)
        
        if args.view in ['centers', 'all']:
            format_orbit_centers(orbit_map.orbit_centers())
        
        if args.view in ['clusters', 'all']:
            format_theme_clusters(orbit_map.theme_clusters())
        
        if args.view in ['orbits', 'all']:
            format_strongest_orbits(orbit_map.strongest_orbits(args.min_connections))
        
        if args.view in ['topology', 'all']:
            format_topology(orbit_map.topology())
        
        print("\n" + "=" * 70)
        print()


if __name__ == '__main__':
    main()
