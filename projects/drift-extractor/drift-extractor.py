#!/usr/bin/env python3
"""
drift-extractor

Extract drift candidates from markdown artifacts:
unresolved questions, tensions, unfinished edges, observations.

Heuristic-first extraction designed to surface 1-3 generative edges
that could become fragments or field notes.
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Optional


# Tension and contrast markers
TENSION_MARKERS = [
    r'\bbut\b', r'\byet\b', r'\bhowever\b', r'\balthough\b',
    r'\binstead\b', r'\brather\b', r'\bnevertheless\b',
    r'\bstill\b', r'\beven so\b', r'\bon the other hand\b',
    r'\bnot.*but\b', r'\bneither.*nor\b',
]

# Uncertainty/hedging language
UNCERTAINTY_MARKERS = [
    r'\bmaybe\b', r'\bperhaps\b', r'\bmight\b', r'\bcould\b',
    r'\bunsure\b', r'\bunclear\b', r'\bunknown\b', r'\bpuzzle\b',
    r'\bcurious\b', r'\bwonder\b', r'\bquestion\b', r'\btentative\b',
]

# Section headers that signal open edges
OPEN_SECTION_PATTERNS = [
    r'^#+\s*(open questions?|future work|to do|unfinished|next steps?|ideas?|thoughts?)\s*$'
]


class DriftCandidate:
    """A potential drift: an unresolved question, tension, or edge."""
    
    def __init__(self, text: str, reason: str, context: Optional[str] = None, score: float = 0.0):
        self.text = text.strip()
        self.reason = reason
        self.context = context
        self.score = score
    
    def to_dict(self) -> Dict:
        return {
            'text': self.text,
            'reason': self.reason,
            'context': self.context,
            'score': round(self.score, 2),
        }
    
    def __repr__(self):
        return f"DriftCandidate(text={self.text[:50]}..., reason={self.reason}, score={self.score})"


def read_markdown(path: Path) -> str:
    """Read markdown content, stripping frontmatter."""
    content = path.read_text(encoding='utf-8')
    
    # Strip YAML frontmatter if present
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            content = parts[2]
    
    return content.strip()


def extract_questions(text: str) -> List[DriftCandidate]:
    """Extract explicit questions from the text."""
    candidates = []
    
    # Split into sentences roughly
    sentences = re.split(r'[.!]\s+|\n\n+', text)
    
    for sentence in sentences:
        sentence = sentence.strip()
        if '?' in sentence:
            # Clean up the sentence
            clean = sentence.strip()
            
            # Skip very short questions (likely rhetorical or trivial)
            if len(clean) < 20:
                continue
            
            # Skip questions that are purely rhetorical markers
            if clean.lower().startswith(('what if', 'why not', 'how could')):
                score = 0.7
            else:
                score = 0.5
            
            candidates.append(DriftCandidate(
                text=clean,
                reason='explicit question',
                score=score
            ))
    
    return candidates


def extract_tensions(text: str) -> List[DriftCandidate]:
    """Extract sentences containing tension or contrast markers."""
    candidates = []
    
    # Split into sentences
    sentences = re.split(r'[.!?]\s+|\n\n+', text)
    
    for sentence in sentences:
        sentence = sentence.strip()
        
        # Check for tension markers
        for pattern in TENSION_MARKERS:
            if re.search(pattern, sentence, re.IGNORECASE):
                # Skip very short sentences
                if len(sentence) < 30:
                    continue
                
                candidates.append(DriftCandidate(
                    text=sentence,
                    reason='tension/contrast language',
                    score=0.6
                ))
                break  # Only count once per sentence
    
    return candidates


def extract_uncertainty(text: str) -> List[DriftCandidate]:
    """Extract sentences containing uncertainty or hedging."""
    candidates = []
    
    sentences = re.split(r'[.!?]\s+|\n\n+', text)
    
    for sentence in sentences:
        sentence = sentence.strip()
        
        # Check for uncertainty markers
        uncertainty_count = 0
        for pattern in UNCERTAINTY_MARKERS:
            if re.search(pattern, sentence, re.IGNORECASE):
                uncertainty_count += 1
        
        if uncertainty_count > 0:
            # Skip very short sentences
            if len(sentence) < 25:
                continue
            
            # Higher score for multiple uncertainty markers
            score = 0.5 + (uncertainty_count * 0.1)
            
            candidates.append(DriftCandidate(
                text=sentence,
                reason='uncertainty/hedging',
                score=score
            ))
    
    return candidates


def extract_open_sections(text: str) -> List[DriftCandidate]:
    """Extract content from sections flagged as open/unfinished."""
    candidates = []
    
    lines = text.split('\n')
    in_open_section = False
    section_content = []
    section_name = None
    
    for line in lines:
        # Check if this is an open section header
        is_open_header = False
        for pattern in OPEN_SECTION_PATTERNS:
            if re.match(pattern, line, re.IGNORECASE):
                is_open_header = True
                section_name = line.strip('#').strip()
                break
        
        if is_open_header:
            in_open_section = True
            section_content = []
            continue
        
        # Check if we've hit a new section header
        if in_open_section and re.match(r'^#+\s+', line):
            # End of open section
            if section_content:
                content = '\n'.join(section_content).strip()
                if len(content) > 20:
                    candidates.append(DriftCandidate(
                        text=content,
                        reason=f'from "{section_name}" section',
                        context=section_name,
                        score=0.8
                    ))
            in_open_section = False
            section_content = []
            section_name = None
        
        if in_open_section and line.strip():
            section_content.append(line)
    
    # Catch final open section if at end of document
    if in_open_section and section_content:
        content = '\n'.join(section_content).strip()
        if len(content) > 20:
            candidates.append(DriftCandidate(
                text=content,
                reason=f'from "{section_name}" section',
                context=section_name,
                score=0.8
            ))
    
    return candidates


def extract_unfinished_thoughts(text: str) -> List[DriftCandidate]:
    """Extract sentences that end with ellipses or trail off."""
    candidates = []
    
    # Look for sentences ending with ellipses
    pattern = r'([^.!?]+\.\.\.)'
    matches = re.findall(pattern, text)
    
    for match in matches:
        clean = match.strip()
        if len(clean) > 20:
            candidates.append(DriftCandidate(
                text=clean,
                reason='trailing thought (ellipsis)',
                score=0.6
            ))
    
    return candidates


def score_and_rank(candidates: List[DriftCandidate]) -> List[DriftCandidate]:
    """Score candidates and return top 3."""
    # Remove duplicates by text
    seen = set()
    unique = []
    for c in candidates:
        normalized = c.text.lower().strip()
        if normalized not in seen:
            seen.add(normalized)
            unique.append(c)
    
    # Sort by score descending
    unique.sort(key=lambda c: c.score, reverse=True)
    
    # Return top 3
    return unique[:3]


def extract_drift_candidates(path: Path) -> List[DriftCandidate]:
    """Main extraction pipeline."""
    content = read_markdown(path)
    
    all_candidates = []
    
    # Run all extractors
    all_candidates.extend(extract_questions(content))
    all_candidates.extend(extract_tensions(content))
    all_candidates.extend(extract_uncertainty(content))
    all_candidates.extend(extract_open_sections(content))
    all_candidates.extend(extract_unfinished_thoughts(content))
    
    # Score and rank
    return score_and_rank(all_candidates)


def format_human_output(candidates: List[DriftCandidate], path: Path):
    """Format output for human reading."""
    print("=" * 60)
    print(f"DRIFT CANDIDATES: {path.name}")
    print("=" * 60)
    print()
    
    if not candidates:
        print("No drift candidates found.")
        print()
        return
    
    for i, candidate in enumerate(candidates, 1):
        print(f"[{i}] {candidate.reason.upper()}")
        if candidate.context:
            print(f"    Context: {candidate.context}")
        print(f"    Score: {candidate.score:.2f}")
        print()
        # Wrap text nicely
        text = candidate.text
        if len(text) > 200:
            text = text[:197] + "..."
        print(f"    {text}")
        print()
    
    print("=" * 60)


def format_json_output(candidates: List[DriftCandidate], path: Path):
    """Format output as JSON."""
    output = {
        'path': str(path),
        'extracted_at': datetime.now(timezone.utc).isoformat(),
        'candidates': [c.to_dict() for c in candidates],
        'count': len(candidates)
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))


def capture_to_workbench(candidates: List[DriftCandidate], source_path: Path):
    """Write candidates to workbench captures.jsonl."""
    workbench_data_dir = Path(__file__).parent.parent / 'workbench' / 'data'
    captures_file = workbench_data_dir / 'captures.jsonl'
    
    if not workbench_data_dir.exists():
        print(f"Warning: workbench data directory not found at {workbench_data_dir}", file=sys.stderr)
        print("Skipping capture.", file=sys.stderr)
        return
    
    timestamp = datetime.now(timezone.utc).isoformat()
    
    with captures_file.open('a', encoding='utf-8') as f:
        for candidate in candidates:
            capture_entry = {
                'timestamp': timestamp,
                'text': candidate.text,
                'source': f'drift-extractor:{source_path.name}',
                'layer': 'internal',
                'tags': ['drift', 'extracted'],
                'metadata': {
                    'reason': candidate.reason,
                    'score': candidate.score,
                    'source_file': str(source_path),
                }
            }
            f.write(json.dumps(capture_entry, ensure_ascii=False) + '\n')
    
    print(f"✓ Captured {len(candidates)} drift candidate(s) to workbench", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description='Extract drift candidates from markdown artifacts'
    )
    parser.add_argument(
        '--path',
        type=Path,
        required=True,
        help='Path to markdown artifact'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON instead of human-readable format'
    )
    parser.add_argument(
        '--capture',
        action='store_true',
        help='Write candidates to workbench captures.jsonl'
    )
    
    args = parser.parse_args()
    
    if not args.path.exists():
        print(f"Error: file not found: {args.path}", file=sys.stderr)
        sys.exit(1)
    
    if not args.path.suffix == '.md':
        print(f"Warning: file doesn't appear to be markdown: {args.path}", file=sys.stderr)
    
    # Extract candidates
    candidates = extract_drift_candidates(args.path)
    
    # Output
    if args.json:
        format_json_output(candidates, args.path)
    else:
        format_human_output(candidates, args.path)
    
    # Optional capture to workbench
    if args.capture and candidates:
        capture_to_workbench(candidates, args.path)


if __name__ == '__main__':
    main()
