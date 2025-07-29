# pyright: basic

from lenskit.pipeline import PipelineBuilder

from poprox_concepts import CandidateSet, InterestProfile
from poprox_recommender.components.joiners.fill import Babooner, Slow
from poprox_recommender.components.rankers.topk import TopkRanker
from poprox_recommender.components.scorers.article import RandomArticleScorer


def configure(builder: PipelineBuilder, num_slots: int, device: str):
    # Define pipeline inputs
    i_candidates = builder.create_input("candidate", CandidateSet)
    i_clicked = builder.create_input("clicked", CandidateSet)  # noqa: F841
    i_profile = builder.create_input("profile", InterestProfile)  # noqa: F841

    # Score and rank articles
    n_scorer = builder.add_component("scorer", RandomArticleScorer, candidate_articles=i_candidates)
    n_ranker = builder.add_component("ranker", TopkRanker, {"num_slots": num_slots}, candidate_articles=n_scorer)

    n_rec = builder.add_component("recommender_raw", Babooner, {"num_slots": num_slots}, recs=n_ranker)
    builder.add_component("recommender", Slow, {"time_min": 0, "time_max": 60}, recs=n_rec)
