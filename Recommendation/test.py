import unittest
from Recommendation import get_next_activity, Activity, Location
from .yelp import YelpCategory, YelpResult
from datetime import datetime

class TestGetNextActivity(unittest.TestCase):
    def test_get_next_activity_after_moma(self):

        preferences = [
            YelpCategory.ArtMuseums,
            YelpCategory.Museums,
            YelpCategory.Coffee,
            YelpCategory.ArtGalleries,
            YelpCategory.Bars
        ]

        business = YelpResult(
            id=None,
            name="MoMA",
            image_url=None,
            is_closed=False,
            categories=[YelpCategory.Museums, YelpCategory.ArtMuseums],
            city_name="New York",
            latitude=40.7614,
            longitude=-73.9776,
            price=2,
            rating=4.6,
            review_count=42507,
            url=None
        )

        moma_visit = Activity(
            business=business,
            time=None,
            duration=None,
        )

        result = get_next_activity(
            activity_preferences=preferences,
            price_preference="1,2,3,4",
            previous_activity=moma_visit
        )

        result = get_next_activity(
            activity_preferences=preferences,
            price_preference="1",
            previous_activity=result
        )

        result = get_next_activity(
            activity_preferences=preferences,
            price_preference="1",
            previous_activity=result
        )

        print(result)