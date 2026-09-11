"""SM-2 间隔重复算法

经典 SM-2 算法实现（Wozniak 1985），Anki 早期默认。
每张卡片有：repetitions（连续答对次数）、interval（间隔天数）、easiness_factor（难度系数，默认 2.5）。
复习质量 quality: 0-5（< 3 答错，>= 3 答对）。
"""
from datetime import datetime, timedelta
from app.models.card import Card

EF_FLOOR = 1.3
EF_DEFAULT = 2.5
QUALITY_WRONG = 3  # quality < 3 即视为答错


def calculate_next_review(card: Card, quality: int) -> Card:
    """根据复习质量计算卡片的下次复习状态（不修改原 card，返回新实例）

    Args:
        card: 当前卡片
        quality: 复习质量 0-5

    Returns:
        新 Card 实例，含更新后的 repetitions / interval / easiness_factor / due_at / last_reviewed_at
    """
    if quality < 0 or quality > 5:
        raise ValueError(f"quality must be 0-5, got {quality}")

    now = datetime.utcnow()

    if quality < QUALITY_WRONG:
        # 答错：重置到 initial state
        repetitions = 0
        interval = 1
    else:
        # 答对：递增 repetitions，根据次数算 interval
        if card.repetitions == 0:
            interval = 1
        elif card.repetitions == 1:
            interval = 6
        else:
            interval = round(card.interval * card.easiness_factor)
        repetitions = card.repetitions + 1

    # 更新 EF：quality 越高涨越多，quality=0 跌但不下破 1.3
    new_ef = card.easiness_factor + (
        0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
    )
    new_ef = max(EF_FLOOR, new_ef)

    return Card(
        id=card.id,
        front=card.front,
        back=card.back,
        created_at=card.created_at,
        repetitions=repetitions,
        interval=interval,
        easiness_factor=new_ef,
        due_at=now + timedelta(days=interval),
        last_reviewed_at=now,
    )
