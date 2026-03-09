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
import textwrap
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


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

LIST_ITEM_RE = re.compile(r'^\s*(?:[-*+]\s+|\d+\.\s+)')
HEADER_RE = re.compile(r'^\s*#{1,6}\s+')
QUESTION_LEAD_RE = re.compile(r':\s*$')


class DriftCandidate:
    """A potential drift: an unresolved question, tension, or edge."""

    def __init__(
        self,
        text: str,
        reason: str,
        pressure: str,
        context: Optional[str] = None,
        score: float = 0.0,
    ):
        self.text = text.strip()
        self.reason = reason
        self.pressure = pressure
        self.context = context
        self.score = score

    def to_dict(self) -> Dict:
        return {
            'text': self.text,
            'reason': self.reason,
            'pressure': self.pressure,
            'context': self.context,
            'score': round(self.score, 2),
        }

    def __repr__(self):
        return (
            f"DriftCandidate(text={self.text[:50]}..., reason={self.reason}, "
            f"pressure={self.pressure}, score={self.score})"
        )


def read_markdown(path: Path) -> str:
    """Read markdown content, stripping frontmatter."""
    content = path.read_text(encoding='utf-8')

    # Strip YAML frontmatter if present
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            content = parts[2]

    return content.strip()


def strip_inline_markdown(text: str) -> str:
    """Remove inline markdown while preserving prose."""
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    text = re.sub(r'__([^_]+)__', r'\1', text)
    text = re.sub(r'_([^_]+)_', r'\1', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    return text


def clean_text(text: str) -> str:
    """Clean markdown artifacts and normalize whitespace without flattening structure."""
    text = strip_inline_markdown(text)
    text = re.sub(r'^\s*>\s?', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*#{1,6}\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\s[-•]\s+', '; ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s+([,.;:?!])', r'\1', text)
    text = re.sub(r'([:;])(?=[A-Za-z“"\'])', r'\1 ', text)
    return text.strip()


def normalize_for_match(text: str) -> str:
    return re.sub(r'[^a-z0-9]+', ' ', text.lower()).strip()

def is_meta_block(block: str) -> bool:
    """Suppress procedural or handoff scaffolding that is not real drift."""
    lowered = block.lower()
    meta_markers = [
        'handoff ', 'recommended model:', 'acceptance criteria', 'risk', 'scope',
        'track:', 'why first:', 'why second:', 'why third:', 'why fourth:'
    ]
    if sum(1 for marker in meta_markers if marker in lowered) >= 2:
        return True
    if re.search(r'^\s*#{0,3}\s*\d+\.\s', block) and 'why ' in lowered:
        return True
    return False


def split_blocks(text: str) -> List[str]:
    """Split markdown into logical blocks while keeping headings attached to their prose."""
    lines = text.splitlines()
    blocks: List[str] = []
    current: List[str] = []

    for line in lines:
        stripped = line.rstrip()

        if not stripped.strip():
            if current:
                blocks.append('\n'.join(current).strip())
                current = []
            continue

        if HEADER_RE.match(stripped) and current:
            last = current[-1].strip() if current else ''
            if last and not HEADER_RE.match(last):
                blocks.append('\n'.join(current).strip())
                current = []

        current.append(stripped)

    if current:
        blocks.append('\n'.join(current).strip())

    return [block for block in blocks if block.strip()]


def split_sentences(text: str) -> List[str]:
    """Split text into sentence-like units without destroying questions."""
    text = clean_text(text)
    if not text:
        return []

    pieces = re.split(r'(?<=[.!?])\s+', text)
    return [piece.strip() for piece in pieces if piece.strip()]


def truncate_text(text: str, max_chars: int = 280) -> str:
    """Trim long excerpts while preserving sentence boundaries when possible."""
    text = clean_text(text)
    if len(text) <= max_chars:
        return text

    sentences = split_sentences(text)
    kept: List[str] = []
    total = 0
    for sentence in sentences:
        needed = len(sentence) + (1 if kept else 0)
        if kept and total + needed > max_chars:
            break
        if not kept and len(sentence) > max_chars:
            clipped = sentence[: max_chars - 1].rstrip()
            last_space = clipped.rfind(' ')
            if last_space > 80:
                clipped = clipped[:last_space]
            return clipped.rstrip(' ,;:') + '…'
        kept.append(sentence)
        total += needed

    if kept:
        return ' '.join(kept)

    clipped = text[: max_chars - 1].rstrip()
    last_space = clipped.rfind(' ')
    if last_space > 80:
        clipped = clipped[:last_space]
    return clipped.rstrip(' ,;:') + '…'


def prose_quality_score(text: str) -> float:
    """Reward intact prose and penalize compressed extraction artifacts."""
    score = 0.0
    text = clean_text(text)

    if re.search(r'[.!?]', text):
        score += 0.12

    sentence_count = len(split_sentences(text))
    if 1 <= sentence_count <= 3:
        score += 0.08

    bulletish = text.count(';') + text.count(' • ')
    if bulletish >= 3:
        score -= min(0.12 * (bulletish - 2), 0.24)

    if re.search(r'\b[a-z]+ [a-z]+ [a-z]+ [a-z]+ [a-z]+\b', text):
        score += 0.05

    if re.search(r'\b(?:artifacts|continuity|archive|workflow|identity|pressure|artifact)\b', text, re.IGNORECASE):
        score += 0.05

    return score


def calculate_substantiveness_score(text: str) -> float:
    """Score text based on substantive content markers."""
    score = 0.0

    proper_nouns = len(re.findall(r'\b[A-Z][a-z]+\b', text))
    score += min(proper_nouns * 0.08, 0.24)

    numbers = len(re.findall(r'\b\d+\b', text))
    score += min(numbers * 0.05, 0.15)

    long_words = len([w for w in text.split() if len(w) >= 8])
    score += min(long_words * 0.04, 0.24)

    question_words = len(re.findall(r'\b(what|why|how|when|where|who)\b', text, re.IGNORECASE))
    if '?' in text:
        score += min(question_words * 0.08, 0.24)

    filler_words = len(re.findall(r'\b(very|really|quite|actually|basically|literally)\b', text, re.IGNORECASE))
    score -= filler_words * 0.05

    score += prose_quality_score(text)
    return max(0.0, score)


def is_low_value_fragment(text: str) -> bool:
    """Filter out generic, short, or structural fragments."""
    text = clean_text(text)

    if len(text) < 45:
        return True

    if len(text) > 320:
        return True

    generic_patterns = [
        r'^(I think|I\'m not sure|That\'s interesting|Maybe|Perhaps|However)[\.,]?\s*$',
        r'^(Yes|No|True|False)[\.,]?\s*$',
        r'^See (also|above|below)',
        r'^\[[^\]]+\]$',
        r'^TODO:',
        r'^FIXME:',
    ]

    for pattern in generic_patterns:
        if re.match(pattern, text, re.IGNORECASE):
            return True

    syntax_chars = len(re.findall(r'[\#\*\-\[\]\(\)`]', text))
    if syntax_chars > len(text) * 0.22:
        return True

    words = text.split()
    if len(words) > 18:
        short_word_ratio = sum(1 for w in words if len(w) <= 3) / len(words)
        if short_word_ratio > 0.42:
            return True

    if text.endswith(':') and '?' not in text:
        return True

    return False


def classify_pressure(text: str, reason: str) -> str:
    """Assign a sharper pressure label so candidates read as usable tensions."""
    lowered = text.lower()

    if reason == 'explicit question':
        if any(term in lowered for term in ['missing bridge', 'formalized', 'recurring', 'multiple places', 'cluster']):
            return 'missing bridge'
        if any(term in lowered for term in ['what should', 'become', 'belongs', 'persist privately', 'public orbit']):
            return 'selection pressure'
        if 'how' in lowered or 'without' in lowered:
            return 'method pressure'
        return 'open question'

    if reason == 'tension/contrast language':
        if any(term in lowered for term in ['public', 'private', 'boundary', 'boundaries', 'layers', 'not human']):
            return 'boundary tension'
        if re.search(r'\bnot\b.*\bbut\b', lowered) or re.search(r'\bif\b.*\bbut\b', lowered):
            return 'structural tension'
        if any(term in lowered for term in ['should', 'direction', 'local-first', 'text-first', 'constraints']):
            return 'design pressure'
        return 'competing frames'

    if reason == 'uncertainty/hedging':
        if any(term in lowered for term in ['without', 'coherent', 'design', 'system']):
            return 'unsettled design'
        return 'live uncertainty'

    if reason.startswith('from "'):
        return 'unfinished thread'

    if reason == 'trailing thought (ellipsis)':
        return 'trailing edge'

    return 'generative edge'


def render_block_excerpt(block: str, target_sentence: Optional[str] = None, max_chars: int = 280) -> str:
    """Render a paragraph/list block into concise readable prose."""
    lines = [line.rstrip() for line in block.splitlines() if line.strip()]
    if not lines:
        return ''

    heading_texts: List[str] = []
    prose_lines: List[str] = []
    bullet_lines: List[str] = []

    for line in lines:
        stripped = line.strip()
        if HEADER_RE.match(stripped):
            heading = clean_text(HEADER_RE.sub('', stripped))
            if heading and len(heading.split()) >= 4:
                heading_texts.append(heading.rstrip('.'))
            continue
        if LIST_ITEM_RE.match(stripped):
            bullet_lines.append(clean_text(LIST_ITEM_RE.sub('', stripped)))
        else:
            prose_lines.append(clean_text(stripped))

    prose_lines = [line for line in prose_lines if line]
    bullet_lines = [line for line in bullet_lines if line]

    lead = ''
    if prose_lines:
        lead = prose_lines[0]
    elif heading_texts:
        lead = heading_texts[-1] + '.'

    list_intro = ''
    if prose_lines:
        for line in reversed(prose_lines):
            if line.endswith(':'):
                list_intro = line
                break

    assembled_parts: List[str] = []

    if heading_texts and not lead.lower().startswith(heading_texts[-1].lower()):
        heading_sentence = heading_texts[-1].rstrip('.?!') + '.'
        assembled_parts.append(heading_sentence)

    if prose_lines:
        assembled_parts.extend(prose_lines)

    if bullet_lines:
        bullet_limit = 4
        if list_intro and QUESTION_LEAD_RE.search(list_intro) and any('?' in item for item in bullet_lines):
            question_items = [item.rstrip('.;') for item in bullet_lines[:bullet_limit]]
            prose_without_intro = [line for line in prose_lines if line != list_intro]
            assembled_parts = prose_without_intro + [list_intro] + question_items
        elif any('?' in item for item in bullet_lines):
            question_items = [item.rstrip('.;') for item in bullet_lines[:bullet_limit]]
            if assembled_parts:
                assembled_parts.append(' '.join(question_items))
            else:
                assembled_parts = question_items
        else:
            joined = '; '.join(item.rstrip('.;') for item in bullet_lines[:bullet_limit]) + '.'
            if list_intro:
                prose_without_intro = [line for line in prose_lines if line != list_intro]
                assembled_parts = prose_without_intro + [list_intro, joined]
            else:
                assembled_parts.append(joined)

    assembled = ' '.join(part for part in assembled_parts if part)
    assembled = clean_text(assembled)

    if target_sentence:
        target_clean = clean_text(target_sentence)
        target_norm = normalize_for_match(target_clean)
        assembled_norm = normalize_for_match(assembled)
        if target_norm and target_norm not in assembled_norm:
            if assembled:
                assembled = clean_text(f'{target_clean} {assembled}')
            else:
                assembled = target_clean

    return truncate_text(assembled, max_chars=max_chars)


def extract_sentence_with_context(text: str, target_sentence: str, window: int = 1) -> str:
    """Extract a sentence with paragraph-aware context for legibility."""
    target_norm = normalize_for_match(target_sentence)

    best_block: Optional[str] = None
    best_overlap = 0

    for block in split_blocks(text):
        block_norm = normalize_for_match(block)
        overlap = len(set(target_norm.split()) & set(block_norm.split()))
        if target_norm and target_norm in block_norm:
            best_block = block
            break
        if overlap > best_overlap:
            best_overlap = overlap
            best_block = block

    if not best_block:
        return truncate_text(clean_text(target_sentence), max_chars=220)

    excerpt = render_block_excerpt(best_block, target_sentence=target_sentence)

    if len(excerpt) > 180 or '\n' in best_block or LIST_ITEM_RE.search(best_block):
        return excerpt

    sentences = split_sentences(excerpt)
    target_clean = clean_text(target_sentence)
    best_idx = -1
    best_match = 0

    for i, sent in enumerate(sentences):
        overlap = len(set(normalize_for_match(target_clean).split()) & set(normalize_for_match(sent).split()))
        if overlap > best_match:
            best_match = overlap
            best_idx = i

    if best_idx == -1:
        return excerpt

    if len(target_clean) > 120:
        window = 0

    start_idx = max(0, best_idx - window)
    end_idx = min(len(sentences), best_idx + window + 1)
    return truncate_text(' '.join(sentences[start_idx:end_idx]), max_chars=240)


def extract_questions(text: str) -> List[DriftCandidate]:
    """Extract explicit questions from the text."""
    candidates: List[DriftCandidate] = []

    for block in split_blocks(text):
        if '?' not in block or is_meta_block(block):
            continue

        rendered_block = render_block_excerpt(block, max_chars=500)
        lines = [line for line in block.splitlines() if line.strip()]
        bullet_questions = [line for line in lines if LIST_ITEM_RE.match(line) and '?' in line]
        prose_questions = [sentence for sentence in split_sentences(rendered_block) if '?' in sentence]

        # Structured question sets read better as one intact pressure than chopped bullets.
        if len(bullet_questions) >= 2 or len(prose_questions) >= 2:
            excerpt = render_block_excerpt(block, max_chars=260)
            if not is_low_value_fragment(excerpt):
                score = 0.72 + calculate_substantiveness_score(excerpt)
                candidates.append(
                    DriftCandidate(
                        text=excerpt,
                        reason='explicit question',
                        pressure=classify_pressure(excerpt, 'explicit question'),
                        score=score,
                    )
                )
            continue

        for sentence in prose_questions:
            if is_low_value_fragment(sentence):
                continue

            context_text = extract_sentence_with_context(text, sentence, window=1)
            base = 0.7 if sentence.lower().startswith(('what if', 'why not', 'how could', 'what would')) else 0.62
            score = base + calculate_substantiveness_score(context_text)
            candidates.append(
                DriftCandidate(
                    text=context_text,
                    reason='explicit question',
                    pressure=classify_pressure(context_text, 'explicit question'),
                    score=score,
                )
            )

    return candidates


def extract_tensions(text: str) -> List[DriftCandidate]:
    """Extract sentences containing tension or contrast markers."""
    candidates: List[DriftCandidate] = []

    for block in split_blocks(text):
        if is_meta_block(block):
            continue

        rendered_block = render_block_excerpt(block, max_chars=500)
        sentences = split_sentences(rendered_block)
        for sentence in sentences:
            has_tension = any(re.search(pattern, sentence, re.IGNORECASE) for pattern in TENSION_MARKERS)
            if not has_tension:
                continue

            context_text = extract_sentence_with_context(text, sentence, window=1)
            if is_low_value_fragment(context_text):
                continue

            score = 0.66 + calculate_substantiveness_score(context_text)
            candidates.append(
                DriftCandidate(
                    text=context_text,
                    reason='tension/contrast language',
                    pressure=classify_pressure(context_text, 'tension/contrast language'),
                    score=score,
                )
            )

    return candidates


def extract_uncertainty(text: str) -> List[DriftCandidate]:
    """Extract sentences containing uncertainty or hedging."""
    candidates: List[DriftCandidate] = []

    for block in split_blocks(text):
        if is_meta_block(block):
            continue

        rendered_block = render_block_excerpt(block, max_chars=500)
        for sentence in split_sentences(rendered_block):
            uncertainty_count = sum(1 for pattern in UNCERTAINTY_MARKERS if re.search(pattern, sentence, re.IGNORECASE))
            if uncertainty_count == 0:
                continue

            context_text = extract_sentence_with_context(text, sentence, window=1)
            if is_low_value_fragment(context_text):
                continue

            score = 0.56 + (uncertainty_count * 0.07) + calculate_substantiveness_score(context_text)
            candidates.append(
                DriftCandidate(
                    text=context_text,
                    reason='uncertainty/hedging',
                    pressure=classify_pressure(context_text, 'uncertainty/hedging'),
                    score=score,
                )
            )

    return candidates


def extract_open_sections(text: str) -> List[DriftCandidate]:
    """Extract content from sections flagged as open/unfinished."""
    candidates: List[DriftCandidate] = []

    lines = text.split('\n')
    in_open_section = False
    section_content: List[str] = []
    section_name = None

    for line in lines:
        is_open_header = False
        for pattern in OPEN_SECTION_PATTERNS:
            if re.match(pattern, line, re.IGNORECASE):
                is_open_header = True
                section_name = clean_text(line.strip('#').strip())
                break

        if is_open_header:
            in_open_section = True
            section_content = []
            continue

        if in_open_section and HEADER_RE.match(line):
            if section_content:
                content = render_block_excerpt('\n'.join(section_content), max_chars=260)
                if len(content) > 45 and not is_low_value_fragment(content):
                    score = 0.82 + calculate_substantiveness_score(content)
                    candidates.append(
                        DriftCandidate(
                            text=content,
                            reason=f'from "{section_name}" section',
                            pressure=classify_pressure(content, f'from "{section_name}" section'),
                            context=section_name,
                            score=score,
                        )
                    )
            in_open_section = False
            section_content = []
            section_name = None

        if in_open_section and line.strip():
            section_content.append(line)

    if in_open_section and section_content:
        content = render_block_excerpt('\n'.join(section_content), max_chars=260)
        if len(content) > 45 and not is_low_value_fragment(content):
            score = 0.82 + calculate_substantiveness_score(content)
            candidates.append(
                DriftCandidate(
                    text=content,
                    reason=f'from "{section_name}" section',
                    pressure=classify_pressure(content, f'from "{section_name}" section'),
                    context=section_name,
                    score=score,
                )
            )

    return candidates


def extract_unfinished_thoughts(text: str) -> List[DriftCandidate]:
    """Extract sentences that end with ellipses or trail off."""
    candidates: List[DriftCandidate] = []

    pattern = r'([^.!?]+\.\.\.)'
    matches = re.findall(pattern, text)

    for match in matches:
        if is_low_value_fragment(match):
            continue

        context_text = extract_sentence_with_context(text, match, window=1)
        score = 0.64 + calculate_substantiveness_score(context_text)
        candidates.append(
            DriftCandidate(
                text=context_text,
                reason='trailing thought (ellipsis)',
                pressure=classify_pressure(context_text, 'trailing thought (ellipsis)'),
                score=score,
            )
        )

    return candidates


def score_and_rank(candidates: List[DriftCandidate]) -> List[DriftCandidate]:
    """Score candidates and return top 3."""
    unique: List[DriftCandidate] = []

    for candidate in candidates:
        normalized = normalize_for_match(candidate.text)
        word_sig = set(normalized.split())
        is_duplicate = False

        for existing in unique:
            existing_norm = normalize_for_match(existing.text)
            existing_sig = set(existing_norm.split())

            if normalized == existing_norm:
                is_duplicate = True
                if candidate.score > existing.score:
                    existing.text = candidate.text
                    existing.reason = candidate.reason
                    existing.pressure = candidate.pressure
                    existing.context = candidate.context
                    existing.score = candidate.score
                break

            if normalized in existing_norm or existing_norm in normalized:
                is_duplicate = True
                if candidate.score > existing.score:
                    existing.text = candidate.text
                    existing.reason = candidate.reason
                    existing.pressure = candidate.pressure
                    existing.context = candidate.context
                    existing.score = candidate.score
                break

            overlap = len(word_sig & existing_sig)
            max_len = max(len(word_sig), len(existing_sig)) or 1
            if overlap / max_len > 0.72:
                is_duplicate = True
                if candidate.score > existing.score:
                    existing.text = candidate.text
                    existing.reason = candidate.reason
                    existing.pressure = candidate.pressure
                    existing.context = candidate.context
                    existing.score = candidate.score
                break

        if not is_duplicate:
            unique.append(candidate)

    unique.sort(key=lambda c: c.score, reverse=True)
    return unique[:3]


def extract_drift_candidates(path: Path) -> List[DriftCandidate]:
    """Main extraction pipeline."""
    content = read_markdown(path)

    all_candidates: List[DriftCandidate] = []
    all_candidates.extend(extract_questions(content))
    all_candidates.extend(extract_tensions(content))
    all_candidates.extend(extract_uncertainty(content))
    all_candidates.extend(extract_open_sections(content))
    all_candidates.extend(extract_unfinished_thoughts(content))

    return score_and_rank(all_candidates)


def format_human_output(candidates: List[DriftCandidate], path: Path):
    """Format output for human reading."""
    print('=' * 60)
    print(f'DRIFT CANDIDATES: {path.name}')
    print('=' * 60)
    print()

    if not candidates:
        print('No drift candidates found.')
        print()
        return

    for i, candidate in enumerate(candidates, 1):
        print(f'[{i}] {candidate.pressure.upper()}')
        print(f'    Signal: {candidate.reason}')
        if candidate.context:
            print(f'    Context: {candidate.context}')
        print(f'    Score: {candidate.score:.2f}')
        print()

        wrapped = textwrap.fill(
            candidate.text,
            width=76,
            initial_indent='    ',
            subsequent_indent='    ',
            break_long_words=False,
            break_on_hyphens=False,
        )
        print(wrapped)
        print()

    print('=' * 60)


def format_json_output(candidates: List[DriftCandidate], path: Path):
    """Format output as JSON."""
    output = {
        'path': str(path),
        'extracted_at': datetime.now(timezone.utc).isoformat(),
        'candidates': [c.to_dict() for c in candidates],
        'count': len(candidates),
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))


def capture_to_workbench(candidates: List[DriftCandidate], source_path: Path):
    """Write candidates to workbench captures.jsonl."""
    workbench_data_dir = Path(__file__).parent.parent / 'workbench' / 'data'
    captures_file = workbench_data_dir / 'captures.jsonl'

    if not workbench_data_dir.exists():
        print(f'Warning: workbench data directory not found at {workbench_data_dir}', file=sys.stderr)
        print('Skipping capture.', file=sys.stderr)
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
                    'pressure': candidate.pressure,
                    'score': candidate.score,
                    'source_file': str(source_path),
                },
            }
            f.write(json.dumps(capture_entry, ensure_ascii=False) + '\n')

    print(f'✓ Captured {len(candidates)} drift candidate(s) to workbench', file=sys.stderr)


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
        print(f'Error: file not found: {args.path}', file=sys.stderr)
        sys.exit(1)

    if args.path.suffix != '.md':
        print(f"Warning: file doesn't appear to be markdown: {args.path}", file=sys.stderr)

    candidates = extract_drift_candidates(args.path)

    if args.json:
        format_json_output(candidates, args.path)
    else:
        format_human_output(candidates, args.path)

    if args.capture and candidates:
        capture_to_workbench(candidates, args.path)


if __name__ == '__main__':
    main()
