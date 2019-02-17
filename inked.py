#!/usr/bin/env python

'''
Write text with external editor
'''

import os
import sys
import subprocess
import tempfile
import copy
import yaml
import inkex # pylint: disable=import-error


class Editor(inkex.Effect):
    '''
    Write text with external editor
    '''

    def __init__(self):
        '''
        Initialise
        '''

        inkex.Effect.__init__(self)

        with open(os.path.expanduser('~/.inked.yaml')) as fhl:
            self.cfg = yaml.load(fhl)


    def run(self, sel):
        '''
        Run extension
        '''

        # Open temporary file
        tmp = tempfile.NamedTemporaryFile()

        # Write to temporary file
        reftspan = None
        for tspan in sel:
            if reftspan is None:
                reftspan = copy.copy(tspan)
            print >> tmp, tspan.text
            sel.remove(tspan)
        tmp.flush()

        # Start editor
        subprocess.call(self.cfg['command'].strip() % tmp.name, shell=True)

        # Read temporary file
        with open(tmp.name) as fhl:
            for line in fhl:
                tspan = copy.copy(reftspan)
                tspan.text = line.strip('\n')
                sel.append(tspan)


    def effect(self):
        '''
        Check object
        '''

        try:
            sel = self.selected.values()[0]
            if sel.tag == '{http://www.w3.org/2000/svg}text':
                self.run(sel)
            else:
                print >> sys.stderr, "Expected non-flowed text object"
        except IndexError:
            pass


Editor().affect()
