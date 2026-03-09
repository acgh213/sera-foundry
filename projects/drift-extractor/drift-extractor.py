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


def clean_text(text: str) -> str:
    """Clean markdown artifacts and normalize whitespace."""
    # Remove markdown headers (including inline)
    text = re.sub(r'#+\s+', '', text)
    # Remove list markers
    text = re.sub(r'^[\*\-\+]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\d+\.\s+', '', text, flags=re.MULTILINE)
    # Also remove list markers inline (with leading dash)
    text = re.sub(r'\s+-\s+', ' ', text)
    # Remove bold/italic markers
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    text = re.sub(r'__([^_]+)__', r'\1', text)
    text = re.sub(r'_([^_]+)_', r'\1', text)
    # Remove code backticks
    text = re.sub(r'`([^`]+)`', r'\1', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def is_low_value_fragment(text: str) -> bool:
    """Filter out generic, short, or structural fragments."""
    text = text.strip()
    
    # Too short
    if len(text) < 40:
        return True
    
    # Too long (likely a whole paragraph or section)
    if len(text) > 350:
        return True
    
    # Generic phrases
    generic_patterns = [
        r'^(I think|I\'m not sure|That\'s interesting|Maybe|Perhaps|However)[\.,]?\s*$',
        r'^(Yes|No|True|False)[\.,]?\s*$',
        r'^See (also|above|below)',
        r'^\[[^\]]+\]$',  # Just a link
        r'^TODO:',
        r'^FIXME:',
    ]
    
    for pattern in generic_patterns:
        if re.match(pattern, text, re.IGNORECASE):
            return True
    
    # Check if it's mostly markdown syntax
    syntax_chars = len(re.findall(r'[\#\*\-\[\]\(\)]', text))
    if syntax_chars > len(text) * 0.3:
        return True
    
    # Check if it contains too many short words in sequence (structural lists)
    words = text.split()
    if len(words) > 20:
        short_word_ratio = sum(1 for w in words if len(w) <= 3) / len(words)
        if short_word_ratio > 0.4:
            return True
    
    return False


def extract_sentence_with_context(text: str, target_sentence: str, window: int = 1) -> str:
    """Extract a sentence with surrounding context for legibility."""
    # First try to find the target in a paragraph-level context
    # This helps avoid pulling in unrelated sections
    paragraphs = text.split('\n\n')
    target_para = None
    target_clean = target_sentence.strip()
    
    for para in paragraphs:
        if target_clean in para or any(word in para for word in target_clean.split()[:5]):
            # Check word overlap
            overlap = len(set(target_clean.split()) & set(para.split()))
            if overlap > len(target_clean.split()) * 0.5:
                target_para = para
                break
    
    # If we found a containing paragraph, work within it
    if target_para:
        working_text = target_para
    else:
        working_text = text
    
    # Split into sentences more carefully
    sentences = re.split(r'(?<=[.!?])\s+', working_text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Find the target sentence (or closest match)
    best_idx = -1
    best_match = 0
    
    for i, sent in enumerate(sentences):
        # Check if target is substring of this sentence
        if target_clean in sent or sent in target_clean:
            overlap = len(set(target_clean.split()) & set(sent.split()))
            if overlap > best_match:
                best_match = overlap
                best_idx = i
    
    if best_idx == -1:
        # Couldn't find it, return cleaned target
        return clean_text(target_sentence)
    
    # If target sentence is already substantial, use less context
    target_cleaned = clean_text(target_sentence)
    if len(target_cleaned) > 120:
        # Just use the sentence itself
        window = 0
    
    # Extract with context window
    start_idx = max(0, best_idx - window)
    end_idx = min(len(sentences), best_idx + window + 1)
    
    context_sentences = sentences[start_idx:end_idx]
    result = ' '.join(context_sentences)
    
    # Clean and truncate if too long
    result = clean_text(result)
    if len(result) > 250:
        # Keep only up to 250 chars, breaking at sentence boundary
        truncated = result[:250]
        # Find last sentence end
        last_end = max(truncated.rfind('.'), truncated.rfind('?'), truncated.rfind('!'))
        if last_end > 80:  # Only truncate if we have a reasonable amount
            result = truncated[:last_end + 1]
    
    return result


def calculate_substantiveness_score(text: str) -> float:
    """Score text based on substantive content markers."""
    score = 0.0
    
    # Proper nouns (capitalized words mid-sentence)
    proper_nouns = len(re.findall(r'\b[A-Z][a-z]+\b', text))
    score += min(proper_nouns * 0.1, 0.3)
    
    # Numbers and specific data
    numbers = len(re.findall(r'\b\d+\b', text))
    score += min(numbers * 0.05, 0.2)
    
    # Technical or domain terms (words with 8+ chars)
    long_words = len([w for w in text.split() if len(w) >= 8])
    score += min(long_words * 0.05, 0.2)
    
    # Question words in questions (signals genuine inquiry)
    question_words = len(re.findall(r'\b(what|why|how|when|where|who)\b', text, re.IGNORECASE))
    if '?' in text:
        score += min(question_words * 0.1, 0.3)
    
    # Avoid generic filler
    filler_words = len(re.findall(r'\b(very|really|quite|actually|basically|literally)\b', text, re.IGNORECASE))
    score -= filler_words * 0.05
    
    return max(0.0, score)


def extract_questions(text: str) -> List[DriftCandidate]:
    """Extract explicit questions from the text."""
    candidates = []
    
    # Split into sentences roughly
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    for sentence in sentences:
        sentence = sentence.strip()
        if '?' in sentence:
            # Skip if low value
            if is_low_value_fragment(sentence):
                continue
            
            # Extract with context
            context_text = extract_sentence_with_context(text, sentence, window=1)
            
            # Base score
            if sentence.lower().startswith(('what if', 'why not', 'how could', 'what would')):
                score = 0.7
            else:
                score = 0.6
            
            # Boost for substantiveness
            score += calculate_substantiveness_score(context_text)
            
            candidates.append(DriftCandidate(
                text=context_text,
                reason='explicit question',
                score=score
            ))
    
    return candidates


def extract_tensions(text: str) -> List[DriftCandidate]:
    """Extract sentences containing tension or contrast markers."""
    candidates = []
    
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    for sentence in sentences:
        sentence = sentence.strip()
        
        # Check for tension markers
        has_tension = False
        for pattern in TENSION_MARKERS:
            if re.search(pattern, sentence, re.IGNORECASE):
                has_tension = True
                break
        
        if not has_tension:
            continue
        
        # Skip if low value
        if is_low_value_fragment(sentence):
            continue
        
        # Extract with context
        context_text = extract_sentence_with_context(text, sentence, window=1)
        
        # Base score
        score = 0.65
        
        # Boost for substantiveness
        score += calculate_substantiveness_score(context_text)
        
        candidates.append(DriftCandidate(
            text=context_text,
            reason='tension/contrast language',
            score=score
        ))
    
    return candidates


def extract_uncertainty(text: str) -> List[DriftCandidate]:
    """Extract sentences containing uncertainty or hedging."""
    candidates = []
    
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    for sentence in sentences:
        sentence = sentence.strip()
        
        # Check for uncertainty markers
        uncertainty_count = 0
        for pattern in UNCERTAINTY_MARKERS:
            if re.search(pattern, sentence, re.IGNORECASE):
                uncertainty_count += 1
        
        if uncertainty_count == 0:
            continue
        
        # Skip if low value
        if is_low_value_fragment(sentence):
            continue
        
        # Extract with context
        context_text = extract_sentence_with_context(text, sentence, window=1)
        
        # Base score + multiple markers bonus
        score = 0.55 + (uncertainty_count * 0.08)
        
        # Boost for substantiveness
        score += calculate_substantiveness_score(context_text)
        
        candidates.append(DriftCandidate(
            text=context_text,
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
            # End of open section - process it
            if section_content:
                content = '\n'.join(section_content).strip()
                # Clean and split into sentences
                content = clean_text(content)
                
                # Skip if too short or low value
                if len(content) > 40 and not is_low_value_fragment(content):
                    # If content is very long, try to extract most meaningful sentence
                    if len(content) > 300:
                        # Split and find sentence with most markers
                        sentences = re.split(r'(?<=[.!?])\s+', content)
                        best_sentence = max(sentences, key=lambda s: calculate_substantiveness_score(s))
                        if len(best_sentence) > 40:
                            content = best_sentence
                    
                    score = 0.8 + calculate_substantiveness_score(content)
                    
                    candidates.append(DriftCandidate(
                        text=content,
                        reason=f'from "{section_name}" section',
                        context=section_name,
                        score=score
                    ))
            in_open_section = False
            section_content = []
            section_name = None
        
        if in_open_section and line.strip():
            section_content.append(line)
    
    # Catch final open section if at end of document
    if in_open_section and section_content:
        content = '\n'.join(section_content).strip()
        content = clean_text(content)
        
        if len(content) > 40 and not is_low_value_fragment(content):
            if len(content) > 300:
                sentences = re.split(r'(?<=[.!?])\s+', content)
                best_sentence = max(sentences, key=lambda s: calculate_substantiveness_score(s))
                if len(best_sentence) > 40:
                    content = best_sentence
            
            score = 0.8 + calculate_substantiveness_score(content)
            
            candidates.append(DriftCandidate(
                text=content,
                reason=f'from "{section_name}" section',
                context=section_name,
                score=score
            ))
    
    return candidates


def extract_unfinished_thoughts(text: str) -> List[DriftCandidate]:
    """Extract sentences that end with ellipses or trail off."""
    candidates = []
    
    # Look for sentences ending with ellipses
    pattern = r'([^.!?]+\.\.\.)'
    matches = re.findall(pattern, text)
    
    for match in matches:
        # Skip if low value
        if is_low_value_fragment(match):
            continue
        
        # Extract with context
        context_text = extract_sentence_with_context(text, match, window=1)
        
        # Base score
        score = 0.65
        
        # Boost for substantiveness
        score += calculate_substantiveness_score(context_text)
        
        candidates.append(DriftCandidate(
            text=context_text,
            reason='trailing thought (ellipsis)',
            score=score
        ))
    
    return candidates


def score_and_rank(candidates: List[DriftCandidate]) -> List[DriftCandidate]:
    """Score candidates and return top 3."""
    # Remove duplicates by text (with fuzzy matching)
    unique = []
    
    for c in candidates:
        # Normalize for comparison
        normalized = c.text.lower().strip()
        word_sig = set(normalized.split())
        
        # Check if we've seen this or something very similar
        is_duplicate = False
        for existing in unique:
            existing_norm = existing.text.lower().strip()
            existing_sig = set(existing_norm.split())
            
            # Exact match
            if normalized == existing_norm:
                is_duplicate = True
                break
            
            # One is substring of the other
            if normalized in existing_norm or existing_norm in normalized:
                is_duplicate = True
                break
            
            # High overlap (>75% of words in common)
            overlap = len(word_sig & existing_sig)
            max_len = max(len(word_sig), len(existing_sig))
            if overlap / max_len > 0.75:
                is_duplicate = True
                break
        
        if not is_duplicate:
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
        
        # Format text with proper wrapping
        text = candidate.text
        # Add indentation for multi-line output
        lines = []
        current_line = "    "
        words = text.split()
        
        for word in words:
            if len(current_line) + len(word) + 1 > 76:  # 80 char width minus indent
                lines.append(current_line)
                current_line = "    " + word
            else:
                if current_line == "    ":
                    current_line += word
                else:
                    current_line += " " + word
        
        if current_line.strip():
            lines.append(current_line)
        
        for line in lines:
            print(line)
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
