"""Initializes a new Quest staircase procedure"""

category = "Staircase"
controls = [
    {
        "type": "line_edit",
        "var": "t_guess",
        "label": "Estimated threshold (used for starting test value)",
        "tooltip": "Estimated threshold (used for starting test value)"
    },
    {
        "type": "line_edit",
        "var": "t_guess_sd",
        "label": "Std. dev. of estimated threshold",
        "tooltip": "Std. dev. of estimated threshold"
    },
    {
        "type": "line_edit",
        "var": "p_threshold",
        "label": "Desired proportion of correct responses",
        "tooltip": "Desired proportion of correct responses"
    },
    {
        "type": "line_edit",
        "var": "beta",
        "label": "Steepness of the Weibull psychometric function (\u03b2)",
        "tooltip": "Steepness of the Weibull psychometric function (\u03b2)"
    },
    {
        "type": "line_edit",
        "var": "delta",
        "label": "Proportion of random responses at maximum stimulus intensity (\u03b4)",
        "tooltip": "Proportion of random responses at maximum stimulus intensity (\u03b4)"
    },
    {
        "type": "line_edit",
        "var": "gamma",
        "label": "Chance level (\u03b3)",
        "tooltip": "Chance level (\u03b3)"
    },
    {
        "type": "combobox",
        "var": "test_value_method",
        "label": "Method to determine optimal test value",
        "options": [
            "quantile",
            "mean",
            "mode"
        ],
        "tooltip": "Method to determine optimal test value"
    },
    {
        "type": "line_edit",
        "var": "min_test_value",
        "label": "Minimum test value",
        "tooltip": "Minimum test value"
    },
    {
        "type": "line_edit",
        "var": "max_test_value",
        "label": "Maximum test value",
        "tooltip": "Maximum test value"
    },
    {
        "type": "line_edit",
        "var": "var_test_value",
        "label": "Experimental variable for test value",
        "tooltip": "Experimental variable for test value"
    }
]
