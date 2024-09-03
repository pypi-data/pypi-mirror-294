#pylint: disable=too-many-locals,too-many-arguments

''' Helper functions to run one measurement measurement with wke '''


import select
import sys
import os
import struct
import multiprocessing

from time import localtime, strftime, time
from threading import Thread, Condition, Lock

from ..run import run, run_background
from ..errors import MeasurementFailedError
from ..tasks import join_all, Task
from ..config import Configuration

from .data_collector import DataCollector

class MeasurementResult:
    ''' The output for MeasurementSession.measure '''

    def __init__(self, start_time, end_time, num_operations, target, options):
        self._start_time = start_time
        self._end_time = end_time
        self._num_operations = num_operations
        self._target = target
        self._options = options

    @property
    def target(self):
        ''' The name of the target that was run for this measurement '''
        return self._target

    @property
    def options(self) -> list[tuple[str, str]]:
        ''' The options that were set for target of this measurement '''
        return list(self._options.items())

    @property
    def start_time(self):
        ''' The (absolute) start time of the measurement '''
        return self._start_time

    @property
    def end_time(self):
        ''' The (absolute) end time of the measurement '''
        return self._end_time

    @property
    def elapsed_time(self):
        ''' The time that elapsed while running the measurement '''
        return self._end_time-self._start_time

    @property
    def throughput(self):
        ''' The calculated throughput (in ops/second) '''
        return float(self.num_operations) / self.elapsed_time

    @property
    def num_operations(self):
        '''
            The numer of operations executed during this measurement.
           
            Note, this is not computed/measured but corresponds to whatever `num_operations` is
            set to when calling MeasurementSession.measure().
        '''
        return self._num_operations

    def print_summary(self):
        ''' Print the summary of this measurement to stdout '''
        print("### Summary:")
        print("Options: " + ', '.join(f"{name}=`{value}`" for name,value in self.options))
        print(f"Elapsed: {self.elapsed_time}")
        print(f"Throughput: {self.throughput}")

class MeasurementSession:
    ''' Logic encapsulating a single measurement run '''

    def __init__(self, cluster, config, collect_statistics, verbose):
        assert isinstance(config, Configuration)

        self._cluster = cluster
        self._config = config
        self._collect_statistics = collect_statistics
        self._uid = strftime("%y%m%d-%H%M%S", localtime())
        self._log_dir = strftime(f"logs/measurement-{self._uid}")
        self._verbose = verbose
        self._background_tasks = []

        # Create the folder that will hold all log data
        os.mkdir(self.log_dir)

        #make the measurement folder easier to find
        try:
            os.remove('current-measurement')
        except OSError:
            pass #did not exist

        os.symlink(self.log_dir, 'current-measurement')

    @property
    def uid(self):
        ''' The unique identifier associated with this measurement '''
        return self._uid

    @property
    def cluster(self):
        ''' The cluster associated with this measurement '''
        return self._cluster

    @property
    def config(self):
        ''' The configuration associated with this measurement '''
        return self._config

    @property
    def log_dir(self):
        ''' The directory where all log files are stored '''
        return self._log_dir

    def __drop__(self):
        self.stop_background_tasks()

    def stop_background_tasks(self):
        ''' Stop any running background tasks that are part of this session '''
        for proc in self._background_tasks:
            proc.terminate()
            proc.join()

    def run(self, selector, target, options=None, prelude=None, timeout=None) -> bool:
        '''
            Run a target as part of this session, but do not measure.

            This is useful, for example, to prepare your measurement by setting up test data.
        '''
        return run(selector, self.config, target, prelude=prelude, options=options,
                verbose=self._verbose, log_dir=self.log_dir, timeout=timeout)

    def run_background(self, selector, target, options=None,
        prelude=None, timeout=None) -> multiprocessing.Process:
        '''
            Run a target in the background as part of this session.
            This is useful, for example, to start a server process that you will measure again.

            To stop the background task either kill the returned Process object,
            or call stop_background_tasks().
        '''
        proc = run_background(selector, self.config, target, prelude=prelude, options=options,
                verbose=self._verbose, log_dir=self.log_dir, timeout=timeout)

        self._background_tasks.append(proc)
        return proc

    def measure(self, selector, target, num_operations, options=None,
        prelude=None, timeout=None) -> MeasurementResult:
        ''' 
            Run the target and measure its performance/output.

            This must be called at most once per Session object and
            the Session object should not be used anymore after calling measure().
        '''

        if options is None:
            options = []

        if self._collect_statistics is None:
            print("Won't collect statistics")
            data_collector = None
        else:
            print("Will collect statistics")

            hostname = self._collect_statistics

            data_collector = DataCollector(self.cluster, self.config, hostname, self.log_dir)
            data_collector.start()

            try:
                data_collector.wait_ready()
            except RuntimeError as err:
                raise MeasurementFailedError("Failed to set up data collection") from err

        # Actually run the thing
        start = time()
        success = run(selector, self.config, target, prelude=prelude, options=options,
                verbose=self._verbose, log_dir=self.log_dir, timeout=timeout)
        end = time()

        if not success:
            raise MeasurementFailedError("Target did not execute successfully")

        result = MeasurementResult(start, end, num_operations, target, options)
        result.print_summary()

        if data_collector:
            data_collector.stop()

        # Move current-measurement to last-measurement
        try:
            os.remove('current-measurement')
        except OSError:
            pass #did not exist
        try:
            os.remove('last-measurement')
        except OSError:
            pass #did not exist

        os.symlink(self.log_dir, 'last-measurement')
        return result
