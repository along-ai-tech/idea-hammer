"""SM-2 算法单元测试

按 TDD 纪律：
- 测试名回答"什么 break 让它失败"
- 不 mirror assertion：每次预期值独立推导
- 边界用例：quality=0, 3, 5；EF 下限；due_at 调度
"""
from datetime import datetime, timedelta

from app.models.card import Card
from app.services.spaced_repetition import (
    EF_FLOOR,
    calculate_next_review,
)


def make_card(repetitions=0, interval=0, easiness_factor=2.5):
    """工厂：创建一张最小卡片用于算法测试"""
    return Card(
        id=1,
        front="Q",
        back="A",
        repetitions=repetitions,
        interval=interval,
        easiness_factor=easiness_factor,
    )


def test_quality_below_three_resets_repetitions_to_zero():
    """答错（quality=0）应该把 repetitions 重置为 0，证明算法重置语义"""
    card = make_card(repetitions=5, interval=30)
    next_card = calculate_next_review(card, quality=0)
    assert next_card.repetitions == 0


def test_quality_below_three_sets_interval_to_one_day():
    """答错应该把 interval 重置为 1 天（明天复习），而非保留原 30 天"""
    card = make_card(repetitions=5, interval=30)
    next_card = calculate_next_review(card, quality=2)
    assert next_card.interval == 1


def test_first_correct_answer_sets_interval_to_one():
    """第一次答对（repetitions 0→1）应该 interval=1 天"""
    card = make_card(repetitions=0, interval=0)
    next_card = calculate_next_review(card, quality=3)
    assert next_card.interval == 1
    assert next_card.repetitions == 1


def test_second_correct_answer_sets_interval_to_six():
    """第二次答对（repetitions 1→2）应该 interval=6 天"""
    card = make_card(repetitions=1, interval=1)
    next_card = calculate_next_review(card, quality=3)
    assert next_card.interval == 6
    assert next_card.repetitions == 2


def test_third_correct_answer_multiplies_interval_by_easiness_factor():
    """第三次答对（repetitions 2→3）应该 interval = 上次 × EF（默认 2.5 × 6 = 15）"""
    card = make_card(repetitions=2, interval=6, easiness_factor=2.5)
    next_card = calculate_next_review(card, quality=3)
    assert next_card.interval == 15
    assert next_card.repetitions == 3


def test_perfect_quality_five_increases_easiness_factor_by_one_tenth():
    """quality=5 完美回答应该让 EF 增加 0.1（2.5 → 2.6）"""
    card = make_card(repetitions=2, interval=6, easiness_factor=2.5)
    next_card = calculate_next_review(card, quality=5)
    # EF' = 2.5 + (0.1 - 0 * (0.08 + 0 * 0.02)) = 2.6
    assert abs(next_card.easiness_factor - 2.6) < 0.001


def test_zero_quality_lowers_easiness_factor_by_eight_tenths():
    """quality=0 完全答错应该让 EF 降低 0.8（2.5 → 1.7），证明 EF 与 quality 强相关"""
    card = make_card(repetitions=2, interval=6, easiness_factor=2.5)
    next_card = calculate_next_review(card, quality=0)
    # EF' = 2.5 + (0.1 - 5 * (0.08 + 5 * 0.02)) = 2.5 + (0.1 - 0.9) = 1.7
    assert abs(next_card.easiness_factor - 1.7) < 0.001


def test_easiness_factor_floor_is_one_point_three():
    """连续答错 EF 不应跌破 SM-2 下限 1.3"""
    card = make_card(repetitions=2, interval=6, easiness_factor=1.4)
    next_card = calculate_next_review(card, quality=0)
    assert next_card.easiness_factor >= EF_FLOOR
    assert next_card.easiness_factor == EF_FLOOR  # 1.4 - 0.4 = 1.0，但应被 floor 拉到 1.3


def test_due_at_is_now_plus_interval_days():
    """due_at 应该等于 now + interval 天，证明调度逻辑正确"""
    card = make_card(repetitions=0, interval=0)
    before = datetime.utcnow()
    next_card = calculate_next_review(card, quality=3)
    after = datetime.utcnow()
    expected_min = before + timedelta(days=1)
    expected_max = after + timedelta(days=1) + timedelta(seconds=1)
    assert expected_min <= next_card.due_at <= expected_max


def test_last_reviewed_at_is_set_to_now():
    """复习后 last_reviewed_at 应该被设置为现在"""
    card = make_card(repetitions=0, interval=0)
    before = datetime.utcnow()
    next_card = calculate_next_review(card, quality=3)
    after = datetime.utcnow()
    assert before <= next_card.last_reviewed_at <= after


def test_quality_out_of_range_raises_value_error():
    """quality 超出 0-5 范围应该抛 ValueError，避免静默错误数据"""
    card = make_card()
    try:
        calculate_next_review(card, quality=6)
    except ValueError:
        return
    except Exception:
        raise AssertionError("应该抛 ValueError，不是其他异常")
    raise AssertionError("quality=6 应该抛 ValueError")


def test_original_card_is_not_mutated():
    """算法应返回新 Card 实例，不修改入参（防止副作用）"""
    card = make_card(repetitions=2, interval=6, easiness_factor=2.5)
    original_id = card.id
    original_repetitions = card.repetitions
    original_interval = card.interval
    calculate_next_review(card, quality=5)
    assert card.id == original_id
    assert card.repetitions == original_repetitions
    assert card.interval == original_interval
