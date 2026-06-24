from excel_analysis.analytics import abc_analysis, cohort_retention, market_basket_analysis, rfm_segmentation
from excel_analysis.data import generate_retail_data


def test_rfm_segmentation_outputs_segments():
    rfm = rfm_segmentation(generate_retail_data())

    assert {"recency", "frequency", "monetary", "rfm_score", "segment"} <= set(rfm.columns)
    assert rfm["segment"].notna().any()


def test_cohort_retention_matrix_starts_at_one():
    cohort = cohort_retention(generate_retail_data())

    assert 0 in cohort.columns
    assert (cohort[0] == 1).all()


def test_abc_analysis_assigns_classes():
    abc = abc_analysis(generate_retail_data())

    assert {"revenue_pct", "cum_pct", "abc_class"} <= set(abc.columns)
    assert set(abc["abc_class"].dropna()) <= {"A", "B", "C"}


def test_market_basket_outputs_rule_metrics():
    rules = market_basket_analysis(generate_retail_data())

    assert {"antecedent", "consequent", "support", "confidence", "lift"} <= set(rules.columns)
    assert (rules["support"] > 0).all()

