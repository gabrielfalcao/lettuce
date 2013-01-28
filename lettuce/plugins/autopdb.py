#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from lettuce.terrain import after


def enable(runner):
    @after.each_step
    def failfast_or_pdb(step):
        has_traceback = step.why

        if not has_traceback:
            return

        sys.stdout.write(step.why.traceback + '\n')

        try:
            from IPython.core.debugger import Pdb
            pdb = Pdb()
        except ImportError:
            try:
                from IPython.Debugger import Pdb
                from IPython.Shell import IPShell
                IPShell(argv=[''])
                pdb = Pdb()
            except ImportError:
                import pdb

        matched, defined = step.pre_run(False)
        if matched:
            args = matched.groups()
            kwargs = matched.groupdict()
            pdb.runcall(defined.function, step, *args, **kwargs)
