import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import Formula, FloatVector
import rpy2.robjects.packages as rpackages

import re


def install_rpackage(pkg_name: str):
    if not rpackages.isinstalled(pkg_name):
        # Import the utils package to use for installation
        utils = rpackages.importr('utils')
        # Set a CRAN mirror
        utils.chooseCRANmirror(ind=1)
        # Install the package
        utils.install_packages(pkg_name)
        print(f"Package '{pkg_name}' installed successfully.")


def r_wilcoxsign_test(GroupA, GroupB, print_result=False):
    # Install and import R packages
    install_rpackage('coin')

    coin = importr('coin')
    base = importr('base')

    GroupA = FloatVector(GroupA)
    GroupB = FloatVector(GroupB)

    # Test1 using base R's wilcox.test
    test_result1 = ro.r['wilcox.test'](GroupA, GroupB, paired=True)
    test_result1_str = str(test_result1)

    if print_result:
        print("Test1 Result:")
        print(test_result1_str)

    # Regex pattern for Test1 to extract V (W) statistic
    pattern_test1 = r"V\s*=\s*(\d+\.?\d*),\s*p-value\s*=\s*(\d+(\.\d+)?([eE][+-]?\d+)?)"
    match_test1 = re.search(pattern_test1, test_result1_str)

    if match_test1:
        w_value = float(match_test1.group(1))
        p_value1 = float(match_test1.group(2))
    else:
        w_value = None

    # Test2 using coin package
    # Combine the two groups into an R data frame
    data = base.data_frame(GroupA=GroupA, GroupB=GroupB)

    # Define the formula for the test
    formula = Formula('GroupA ~ GroupB')

    # Perform the Wilcoxon signed-rank test using the wilcoxsign_test function
    test_result2 = coin.wilcoxsign_test(formula, data=data, distribution="exact", alternative="two.sided")
    test_result2_str = str(test_result2)

    if print_result:
        print("Test2 Result:")
        print(test_result2_str)

    # Regex pattern for Test2 to extract Z and p-value
    pattern_test2 = r"Z\s*=\s*(-?\d+\.\d+),\s*p-value\s*=\s*(\d+(\.\d+)?([eE][+-]?\d+)?)"
    match_test2 = re.search(pattern_test2, test_result2_str)

    if match_test2:
        z_value = float(match_test2.group(1))
        p_value2 = float(match_test2.group(2))
    else:
        z_value, p_value2 = None, None

    r_value = abs(z_value / (len(GroupA) + len(GroupB)) ** .5) if z_value is not None else None

    effect_size = ""

    p_value = max([p_value1, p_value2])

    if p_value < .05:
        effect_size = f", r = {r_value}"
    report = f"$W = {w_value}, Z = {z_value}, p = {p_value}{effect_size}$"

    return {'w_statistics': w_value, 'z_statistics': z_value, 'p_value': p_value,
            'r_value': round(r_value, 5) if r_value is not None else None,
            'report': report}


def r_art_anova(df, indep_vars: list, response_var: str, subject_id_var: str, formula=None, print_results=False):
    """Rpy2 binding for ART ANOVA in PYTHON. Version 1. Written by Jonathan Liebers on 2023-08-31."""

    def significance_level(p):
        if p < 0.001:
            return '***'
        elif p < 0.01:
            return '**'
        elif p < 0.05:
            return '*'
        elif p < 0.1:
            return '.'
        else:
            return ''

    # general imports
    from rpy2.robjects import r, pandas2ri, Formula
    import rpy2.robjects as ro
    import rpy2.robjects.conversion as conversion
    from rpy2.robjects.packages import importr
    from itertools import combinations
    import string
    import rpy2.ipython.html
    rpy2.ipython.html.init_printing()

    # Import necessary R packages
    artool = importr('ARTool')
    rcpp = importr('Rcpp')
    dplyr = importr('dplyr')

    # Activate pandas-to-R dataframe conversion
    pandas2ri.activate()

    rdf = conversion.py2rpy(df)

    # Prepare data for R dataframe
    data_dict = {factor: r['as.factor'](rdf.rx2[factor]) for factor in indep_vars}
    data_dict[response_var] = rdf.rx2[response_var]
    data_dict[subject_id_var] = rdf.rx2[subject_id_var]

    rdf = r['data.frame'](**data_dict)

    # If formula is not provided, construct a default one
    if formula is None:
        independent_vars = " * ".join(indep_vars)
        formula = f"{response_var} ~ {independent_vars} + (1|{subject_id_var})"

    m = r.art(Formula(formula), data=rdf)
    anova_result = r.anova(m)

    r.assign("m", m)

    # convert anova
    with (ro.default_converter + pandas2ri.converter).context():
        anova_result = ro.conversion.get_conversion().rpy2py(anova_result)

    # add sig column
    anova_result['sig.'] = anova_result['Pr(>F)'].apply(lambda x: significance_level(x))

    # determine posthocs for significant rows
    run_posthoc = anova_result.loc[anova_result['sig.'].str.startswith('*')]["Term"].tolist()

    if len(run_posthoc) > 0:
        posthocs = {}

        for combo, letter in zip(run_posthoc, string.ascii_lowercase):
            if ":" not in combo:
                continue
            r("""posthoc.LETTER <- art.con(m, "COMBO", adjust="holm") %>%  # run ART-C for X1
                                      summary() %>%  # add significance stars to the output
                                      mutate(sig. = symnum(p.value, corr=FALSE, na=FALSE,
                                      cutpoints = c(0, 0.001, 0.01, 0.05, 0.1, 1),
                                      symbols = c("***", "**", "*", ".", " ")))

                                      posthoc.LETTER""".replace("COMBO", combo).replace("LETTER", letter))
            with (ro.default_converter + pandas2ri.converter).context():
                posthocs.update({combo: ro.conversion.get_conversion().rpy2py(r[f"posthoc.{letter}"])})

    if print_results:
        print("ANOVA")
        display(anova_result)

        for key in posthocs.keys():
            print("\nPosthoc test for", key)
            display(posthocs[key])

    return anova_result, posthocs