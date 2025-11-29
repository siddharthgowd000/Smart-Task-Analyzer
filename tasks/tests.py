from django.test import TestCase
from datetime import date, timedelta
from .scoring import analyze_tasks, STRATEGY_SMART, STRATEGY_IMPACT


class ScoringTests(TestCase):

    def test_overdue_task_has_higher_score(self):
        today = date.today()
        tasks = [
            {
                "id": 1,
                "title": "Overdue",
                "due_date": (today - timedelta(days=1)).isoformat(),
                "estimated_hours": 2,
                "importance": 5,
                "dependencies": [],
            },
            {
                "id": 2,
                "title": "Future",
                "due_date": (today + timedelta(days=5)).isoformat(),
                "estimated_hours": 2,
                "importance": 5,
                "dependencies": [],
            },
        ]
        result = analyze_tasks(tasks, strategy=STRATEGY_SMART)
        top_title = result["tasks"][0]["title"]
        self.assertEqual(top_title, "Overdue")

    def test_high_importance_wins_in_high_impact(self):
        today = date.today()
        tasks = [
            {
                "id": 1,
                "title": "Low importance",
                "due_date": (today + timedelta(days=1)).isoformat(),
                "estimated_hours": 1,
                "importance": 2,
                "dependencies": [],
            },
            {
                "id": 2,
                "title": "High importance",
                "due_date": (today + timedelta(days=1)).isoformat(),
                "estimated_hours": 3,
                "importance": 9,
                "dependencies": [],
            },
        ]
        result = analyze_tasks(tasks, strategy=STRATEGY_IMPACT)
        self.assertEqual(result["tasks"][0]["title"], "High importance")