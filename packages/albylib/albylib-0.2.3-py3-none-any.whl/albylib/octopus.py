import ipyparallel as ipp


class Octopus:
    """
    A class for managing and interacting with an ipyparallel cluster.

    Attributes:
        num_engines (int): The number of worker engines to start.
        engine_args (dict): A dictionary of arguments to pass to the engines.
        cluster (ipp.Cluster): The ipyparallel cluster object.
        client (ipp.Client): The ipyparallel client object.
        view (ipp.LoadBalancedView): The load-balanced view of the engines.
    """

    def __init__(self, workers=10, cpus_per_worker=2, mem_per_worker="10G"):
        """
        Initializes the Octopus instance.

        Args:
            workers: The number of worker engines to start (default: 10).
            cpus_per_worker: The number of CPUs to allocate per worker (default: 2).
            mem_per_worker: The memory to allocate per worker (default: "10G").
        """
        self.num_engines = workers
        self.engine_args = {"mem": mem_per_worker, "cpus": cpus_per_worker, "controller_mem": f"{workers * 4}G"}
        self.cluster = None
        self.client = None
        self.view = None

    def start(self):
        """
        Starts the ipyparallel cluster and connects the client and load-balanced view.
        """
        if self.cluster is None:
            self.cluster = ipp.Cluster(profile="slurm", controller_ip="*", n=self.num_engines, engine_timeout=600)
            self.cluster.profile_config.SlurmLauncher.namespace.update(self.engine_args)
            self.cluster.profile_config.SlurmControllerLauncher.namespace.update(self.engine_args)
        self._start()

    def _start(self):
        """
        Starts the cluster and connects the client and load-balanced view.
        """
        self.cluster.start_cluster_sync()
        self.client = self.cluster.connect_client_sync()
        self.view = self.client.load_balanced_view()

    def map_sync(self, func, iterable):
        """
        Maps a function to an iterable using the load-balanced view synchronously.

        Args:
            func: The function to map.
            iterable: The iterable to map the function over.

        Returns:
            A list of results from mapping the function to the iterable.

        Raises:
            RuntimeError: If the Octopus has not been started.
        """
        if self.view is None:
            raise RuntimeError("Octopus has not been started. Call start() method first.")
        return self.view.map_sync(func, iterable)

    def map_async(self, func, iterable):
        """
        Maps a function to an iterable using the load-balanced view asynchronously.

        Args:
            func: The function to map.
            iterable: The iterable to map the function over.

        Returns:
            An AsyncResult object representing the asynchronous computation.

        Raises:
            RuntimeError: If the Octopus has not been started.
        """
        if self.view is None:
            raise RuntimeError("Octopus has not been started. Call start() method first.")
        return self.view.map_async(func, iterable)

    def stop(self):
        """
        Stops the ipyparallel cluster and resets the cluster, client, and view attributes.
        """
        if self.cluster is not None:
            self.cluster.stop_cluster_sync()
            self.cluster = None
            self.client = None
            self.view = None
