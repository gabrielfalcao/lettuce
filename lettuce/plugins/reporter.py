import sys


class Reporter(object):
    def __init__(self):
        self.failed_scenarios = []
        self.scenarios_and_its_fails = {}

    def wrt(self, what):
        if isinstance(what, unicode):
            what = what.encode('utf-8')
        sys.stdout.write(what)

    def store_failed_step(self, step):
        if step.failed and step.scenario not in self.failed_scenarios:
            self.scenarios_and_its_fails[step.scenario] = step.why
            self.failed_scenarios.append(step.scenario)

    def print_scenario_running(self, scenario):
        pass

    def print_scenario_ran(self, scenario):
        pass

    def print_end(self, total):
        if total.scenarios_passed < total.scenarios_ran:
            self.wrt("\n")
            self.wrt("\n")
            for scenario in self.failed_scenarios:
                reason = self.scenarios_and_its_fails[scenario]
                self.wrt(unicode(reason.step))
                self.wrt("\n")
                self.wrt(reason.traceback)

        self.wrt("\n")
        word = total.features_ran > 1 and "features" or "feature"
        self.wrt("%d %s (%d passed)\n" % (
            total.features_ran,
            word,
            total.features_passed))

        word = total.scenarios_ran > 1 and "scenarios" or "scenario"
        self.wrt("%d %s (%d passed)\n" % (
            total.scenarios_ran,
            word,
            total.scenarios_passed))

        steps_details = []
        for kind in "failed", "skipped", "undefined":
            attr = 'steps_%s' % kind
            stotal = getattr(total, attr)
            if stotal:
                steps_details.append("%d %s" % (stotal, kind))

        steps_details.append("%d passed" % total.steps_passed)
        word = total.steps > 1 and "steps" or "step"
        self.wrt("%d %s (%s)\n" % (
            total.steps,
            word,
            ", ".join(steps_details)))

        if total.failed_scenario_locations:
            self.wrt("\n")
            self.wrt("List of failed scenarios:\n")
            for scenario in total.failed_scenario_locations:
                self.wrt(scenario)
            self.wrt("\n")
