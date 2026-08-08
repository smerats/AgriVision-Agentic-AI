"""
explainable_ai/explanation.py
Generates natural language explanations and calculates feature contributions for predictions.
"""

def explain_prediction(feature_dict, feature_means, feature_importances, target_type="regression", target_name="Target"):
    """
    Generate local explanations and feature contributions.
    
    Parameters:
        feature_dict (dict): The input values for features, e.g. {"temperature": 25.0, ...}
        feature_means (dict): Average training value for each feature.
        feature_importances (dict): Relative importance weights of the features.
        target_type (str): "regression" or "classification".
        target_name (str): The label of the prediction target.
        
    Returns:
        dict: A dictionary containing:
            - "feature_influence": Map of each feature to its influence description.
            - "summary": A high-level natural language summary.
            - "feature_contributions": Map of each feature to its numerical contribution score.
    """
    explanations = {}
    contributions = {}
    
    for feature, value in feature_dict.items():
        mean = feature_means.get(feature, 0.0)
        importance = feature_importances.get(feature, 0.0)
        
        # Deviation from the typical training mean
        deviation = value - mean
        # A simple local contribution proxy: deviation * importance weight
        contribution = deviation * importance
        contributions[feature] = float(contribution)
        
        direction = "above" if deviation >= 0 else "below"
        diff_pct = (abs(deviation) / mean * 100) if mean != 0 else 0.0
        
        if target_type == "regression":
            impact = "increased" if contribution >= 0 else "decreased"
            explanations[feature] = (
                f"{feature.replace('_', ' ').capitalize()} is {value:.2f}, which is {direction} the "
                f"average of {mean:.2f} ({diff_pct:.1f}% deviation). This {impact} the predicted {target_name}."
            )
        else:
            # Classification
            impact = "increased" if contribution >= 0 else "decreased"
            explanations[feature] = (
                f"{feature.replace('_', ' ').capitalize()} is {value:.2f}, which is {direction} the "
                f"average of {mean:.2f} ({diff_pct:.1f}% deviation). This {impact} the likelihood/risk of {target_name}."
            )
            
    # Find key factors
    sorted_contribs = sorted(contributions.items(), key=lambda x: x[1], reverse=True)
    top_positive = sorted_contribs[0][0] if sorted_contribs and sorted_contribs[0][1] > 0 else None
    top_negative = sorted_contribs[-1][0] if sorted_contribs and sorted_contribs[-1][1] < 0 else None
    
    summary = []
    if top_positive:
        summary.append(f"The primary factor driving the prediction up was {top_positive.replace('_', ' ')}.")
    if top_negative:
        summary.append(f"The primary factor pulling the prediction down was {top_negative.replace('_', ' ')}.")
        
    if not summary:
        summary.append("All inputs are near their typical average values.")
        
    return {
        "feature_influence": explanations,
        "summary": " ".join(summary),
        "feature_contributions": contributions
    }
