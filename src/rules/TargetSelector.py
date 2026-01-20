"""
This file is part of HuskyBot CV.
Copyright (C) 2025 Advanced Robotics at the University of Washington <robomstr@uw.edu>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from detector import Target


class TargetSelector:
    """
    A class used to select the best target from a list of targets based on a set of scoring rules.

    The TargetSelector uses a list of rules and applies the computed score to each target.
    The target with the lowest cumulative score is considered the best target.
    """

    def __init__(self, rules):
        self.rules = rules

    def getBestTarget(self, targets) -> Target:
        """
        Evaluate each target based on the rules and return the target with the lowest score.
        """
        bestTarget = None
        bestScore = float("inf")

        for target in targets:
            score = self.getTargetScore(target)
            if score < bestScore:
                bestScore = score
                bestTarget = target

        return bestTarget

    def getTargetScore(self, target: Target) -> float:
        """
        Computes the score for a single target
        """
        score = 0
        for rule in self.rules:
            score += rule.getScore(target)
        return score
