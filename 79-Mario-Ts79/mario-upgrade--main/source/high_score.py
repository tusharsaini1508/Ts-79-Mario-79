import json
from pathlib import Path


DEFAULT_SCORE_PATH = Path.home() / '.mario-platformer' / 'high_score.json'


def load_high_score(path=DEFAULT_SCORE_PATH):
    try:
        with Path(path).open(encoding='utf-8') as score_file:
            data = json.load(score_file)
    except (OSError, json.JSONDecodeError):
        return 0

    if not isinstance(data, dict):
        return 0

    score = data.get('top_score', 0)
    if type(score) is not int or score < 0:
        return 0
    return score


def save_high_score(score, path=DEFAULT_SCORE_PATH):
    if type(score) is not int or score < 0:
        return False

    score_path = Path(path)
    temporary_path = score_path.with_suffix(score_path.suffix + '.tmp')
    try:
        score_path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path.write_text(
            json.dumps({'top_score': score}), encoding='utf-8')
        temporary_path.replace(score_path)
    except OSError:
        return False
    return True
