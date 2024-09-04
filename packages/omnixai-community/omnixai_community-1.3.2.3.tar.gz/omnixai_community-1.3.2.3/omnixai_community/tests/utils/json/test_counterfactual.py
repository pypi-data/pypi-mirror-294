#
# Copyright (c) 2023 salesforce.com, inc.
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# For full license text, see the LICENSE file in the repo root or https://opensource.org/licenses/BSD-3-Clause
#
import unittest
import pandas as pd
from omnixai_community.explanations.tabular.counterfactual import CFExplanation, ExplanationBase


class TestCF(unittest.TestCase):

    def test(self):
        exp = CFExplanation()
        exp.add(
            query=pd.DataFrame([["a", "b"]], columns=["col 1", "col 2"]),
            cfs=pd.DataFrame([["a", "b"], ["c", "d"], ["e", "f"]], columns=["col 1", "col 2"]),
        )
        s = exp.to_json()
        e = ExplanationBase.from_json(s)

        a, b = exp.get_explanations(0), e.get_explanations(0)
        for name in ["query", "counterfactual"]:
            self.assertListEqual(list(a[name].columns), list(b[name].columns))
            self.assertListEqual(a[name].values.tolist(), b[name].values.tolist())


if __name__ == "__main__":
    unittest.main()
