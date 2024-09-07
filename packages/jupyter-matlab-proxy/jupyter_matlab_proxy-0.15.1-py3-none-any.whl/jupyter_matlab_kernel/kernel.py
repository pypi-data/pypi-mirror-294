# Copyright 2023-2024 The MathWorks, Inc.
# Implementation of MATLAB Kernel

# Import Python Standard Library
import asyncio
import http
import os
import sys
import time

# Import Dependencies
import aiohttp
import aiohttp.client_exceptions
import ipykernel.kernelbase
import psutil
import requests
from matlab_proxy import settings as mwi_settings
from matlab_proxy import util as mwi_util

from jupyter_matlab_kernel import mwi_logger
from jupyter_matlab_kernel.magic_execution_engine import (
    MagicExecutionEngine,
    get_completion_result_for_magics,
)
from jupyter_matlab_kernel.mwi_comm_helpers import MWICommHelper
from jupyter_matlab_kernel.mwi_exceptions import MATLABConnectionError

_MATLAB_STARTUP_TIMEOUT = mwi_settings.get_process_startup_timeout()
_logger = mwi_logger.get()


def is_jupyter_testing_enabled():
    """
    Checks if testing mode is enabled

    Returns:
        bool: True if MWI_JUPYTER_TEST environment variable is set to 'true'
        else False
    """

    return os.environ.get("MWI_JUPYTER_TEST", "false").lower() == "true"


def start_matlab_proxy_for_testing(logger=_logger):
    """
    Only used for testing purposes. Gets the matlab-proxy server configuration
    from environment variables and mocks the 'start_matlab_proxy' function

    Returns:
        Tuple (string, string, dict):
            url (string): Complete URL to send HTTP requests to matlab-proxy
            base_url (string): Complete base url for matlab-proxy obtained from tests
            headers (dict): Empty dictionary
    """

    import matlab_proxy.util.mwi.environment_variables as mwi_env

    # These environment variables are being set by tests, using dictionary lookup
    # instead of '.getenv' to make sure that the following line fails with the
    # Exception 'KeyError' in case the environment variables are not set
    matlab_proxy_base_url = os.environ[mwi_env.get_env_name_base_url()]
    matlab_proxy_app_port = os.environ[mwi_env.get_env_name_app_port()]

    logger.debug("Creating matlab-proxy URL for MATLABKernel testing.")

    # '127.0.0.1' is used instead 'localhost' for testing since Windows machines consume
    # some time to resolve 'localhost' hostname
    url = "{protocol}://127.0.0.1:{port}{base_url}".format(
        protocol="http",
        port=matlab_proxy_app_port,
        base_url=matlab_proxy_base_url,
    )
    headers = {}

    logger.debug(f"matlab-proxy URL: {url}")
    logger.debug(f"headers: {headers}")

    return url, matlab_proxy_base_url, headers


def _start_matlab_proxy_using_jupyter(url, headers, logger=_logger):
    """
    Start matlab-proxy using jupyter server which started the current kernel
    process by sending HTTP request to the endpoint registered through
    jupyter-matlab-proxy.

    Args:
        url (string): URL to send HTTP request
        headers (dict): HTTP headers required for the request

    Returns:
        bool: True if jupyter server has successfully started matlab-proxy else False.
    """
    # This is content that is present in the matlab-proxy index.html page which
    # can be used to validate a proper response.
    matlab_proxy_index_page_identifier = "MWI_MATLAB_PROXY_IDENTIFIER"

    logger.debug(
        f"Sending request to jupyter to start matlab-proxy at {url} with headers: {headers}"
    )
    # send request to the matlab-proxy endpoint to make sure it is available.
    # If matlab-proxy is not started, jupyter-server starts it at this point.
    resp = requests.get(url, headers=headers, verify=False)
    logger.debug(f"Received status code: {resp.status_code}")

    return (
        resp.status_code == http.HTTPStatus.OK
        and matlab_proxy_index_page_identifier in resp.text
    )


def start_matlab_proxy(logger=_logger):
    """
    Start matlab-proxy registered with the jupyter server which started the
    current kernel process.

    Raises:
        MATLABConnectionError: Occurs when kernel is not started by jupyter server.

    Returns:
        Tuple (string, string, dict):
            url (string): Complete URL to send HTTP requests to matlab-proxy
            base_url (string): Complete base url for matlab-proxy provided by jupyter server
            headers (dict): HTTP headers required while sending HTTP requests to matlab-proxy
    """

    # If jupyter testing is enabled, then a standalone matlab-proxy server would be
    # launched by the tests and kernel would expect the configurations of this matlab-proxy
    # server which is provided through environment variables to 'start_matlab_proxy_for_testing'
    if is_jupyter_testing_enabled():
        return start_matlab_proxy_for_testing(logger)

    nb_server_list = []

    # The matlab-proxy server, if running, could have been started by either
    # "jupyter_server" or "notebook" package.
    try:
        from jupyter_server import serverapp

        nb_server_list += list(serverapp.list_running_servers())

        from notebook import notebookapp

        nb_server_list += list(notebookapp.list_running_servers())
    except ImportError:
        pass

    # Use parent process id of the kernel to filter Jupyter Server from the list.
    jupyter_server_pid = os.getppid()

    # On Windows platforms using venv/virtualenv an intermediate python process spaws the kernel.
    # jupyter_server ---spawns---> intermediate_process ---spawns---> jupyter_matlab_kernel
    # Thus we need to go one level higher to acquire the process id of the jupyter server.
    # Note: conda environments do not require this, and for these environments sys.prefix == sys.base_prefix
    is_virtual_env = sys.prefix != sys.base_prefix
    if mwi_util.system.is_windows() and is_virtual_env:
        jupyter_server_pid = psutil.Process(jupyter_server_pid).ppid()

    logger.debug(f"Resolved jupyter server pid: {jupyter_server_pid}")

    nb_server = dict()
    found_nb_server = False
    for server in nb_server_list:
        if server["pid"] == jupyter_server_pid:
            logger.debug("Jupyter server associated with this MATLAB Kernel found.")
            found_nb_server = True
            nb_server = server
            # Stop iterating over the server list
            break

    # Error out if the server is not found!
    if not found_nb_server:
        logger.error("Jupyter server associated with this MATLABKernel not found.")
        raise MATLABConnectionError(
            """
            Error: MATLAB Kernel for Jupyter was unable to find the notebook server from which it was spawned!\n
            Resolution: Please relaunch kernel from JupyterLab or Classic Jupyter Notebook.
            """
        )

    # Verify that Password is disabled
    if nb_server["password"] is True:
        logger.error("Jupyter server uses password for authentication.")
        # TODO: To support passwords, we either need to acquire it from Jupyter or ask the user?
        raise MATLABConnectionError(
            """
            Error: MATLAB Kernel could not communicate with MATLAB.\n
            Reason: There is a password set to access the Jupyter server.\n
            Resolution: Delete the cached Notebook password file, and restart the kernel.\n
            See https://jupyter-notebook.readthedocs.io/en/stable/public_server.html#securing-a-notebook-server for more information.
            """
        )

    # Using nb_server["url"] to construct matlab-proxy URL as it handles the following cases
    # 1. For normal usage of Jupyter, the URL returned by nb_server uses localhost
    # 2. For explicitly specified IP with Jupyter, the URL returned by nb_server
    #       a. uses FQDN hostname when specified IP is 0.0.0.0
    #       b. uses specified IP for all other cases
    matlab_proxy_url = "{jupyter_server_url}matlab".format(
        jupyter_server_url=nb_server["url"]
    )

    available_tokens = {
        "jupyter_server": nb_server.get("token"),
        "jupyterhub": os.getenv("JUPYTERHUB_API_TOKEN"),
        "default": None,
    }

    for token in available_tokens.values():
        if token:
            headers = {"Authorization": f"token {token}"}
        else:
            headers = None

        if _start_matlab_proxy_using_jupyter(matlab_proxy_url, headers, logger):
            logger.debug(
                f"Started matlab-proxy using jupyter at {matlab_proxy_url} with headers: {headers}"
            )
            return matlab_proxy_url, nb_server["base_url"], headers

    logger.error(
        "MATLABKernel could not communicate with matlab-proxy through Jupyter server"
    )
    logger.error(f"Jupyter server:\n{nb_server}")
    raise MATLABConnectionError(
        """
                Error: MATLAB Kernel could not communicate with MATLAB.
                Reason: Possibly due to invalid jupyter security tokens.
        """
    )


class MATLABKernel(ipykernel.kernelbase.Kernel):
    # Required variables for Jupyter Kernel to function
    # banner is shown only for Jupyter Console.
    banner = "MATLAB"
    implementation = "jupyter_matlab_kernel"
    implementation_version: str = "0.0.1"

    # Values should be same as Codemirror mode
    language_info = {
        "name": "matlab",
        "mimetype": "text/x-matlab",
        "file_extension": ".m",
    }

    # MATLAB Kernel state
    kernel_id = ""
    server_base_url = ""
    startup_error = None
    startup_checks_completed: bool = False

    def __init__(self, *args, **kwargs):
        # Call superclass constructor to initialize ipykernel infrastructure
        super(MATLABKernel, self).__init__(*args, **kwargs)

        # Update log instance with kernel id. This helps in identifying logs from
        # multiple kernels which are running simultaneously
        self.kernel_id = self.ident
        self.log.debug(f"Initializing kernel with id: {self.kernel_id}")
        self.log = self.log.getChild(f"{self.kernel_id}")

        # Initialize the Magic Execution Engine.
        self.magic_engine = MagicExecutionEngine(self.log)

        try:
            # Start matlab-proxy using the jupyter-matlab-proxy registered endpoint.
            murl, self.server_base_url, headers = start_matlab_proxy(self.log)

            # Using asyncio.get_event_loop for shell_loop as io_loop variable is
            # not yet initialized because start() is called after the __init__
            # is completed.
            shell_loop = asyncio.get_event_loop()
            control_loop = self.control_thread.io_loop.asyncio_loop
            self.mwi_comm_helper = MWICommHelper(
                self.kernel_id, murl, shell_loop, control_loop, headers, self.log
            )
            shell_loop.run_until_complete(self.mwi_comm_helper.connect())
        except MATLABConnectionError as err:
            self.startup_error = err

    # ipykernel Interface API
    # https://ipython.readthedocs.io/en/stable/development/wrapperkernels.html

    async def interrupt_request(self, stream, ident, parent):
        """
        Custom handling of interrupt request sent by Jupyter. For more info, look at
        https://jupyter-client.readthedocs.io/en/stable/messaging.html#kernel-interrupt
        """
        self.log.debug("Received interrupt request from Jupyter")
        try:
            # Send interrupt request to MATLAB
            await self.mwi_comm_helper.send_interrupt_request_to_matlab()

            # Set the response to interrupt request.
            content = {"status": "ok"}
        except Exception as e:
            # Set the exception information as response to interrupt request
            self.log.error(
                f"Exception occurred while sending interrupt request to MATLAB: {e}"
            )
            content = {
                "status": "error",
                "ename": str(type(e).__name__),
                "evalue": str(e),
                "traceback": [],
            }

        self.session.send(stream, "interrupt_reply", content, parent, ident=ident)

    def modify_kernel(self, states_to_modify):
        """
        Used to modify MATLAB Kernel state
        Args:
            states_to_modify (dict): A key value pair of all the states to be modified.

        """
        self.log.debug(f"Modifying the kernel with {states_to_modify}")
        for key, value in states_to_modify.items():
            if hasattr(self, key):
                self.log.debug(f"set the value of {key} to {value}")
                setattr(self, key, value)

    def handle_magic_output(self, output, outputs=None):
        if output["type"] == "modify_kernel":
            self.modify_kernel(output)
        else:
            self.display_output(output)
            if outputs is not None and not self.startup_checks_completed:
                # Outputs are cleared after startup_check.
                # Storing the magic outputs to display them after startup_check completes.
                outputs.append(output)

    async def do_execute(
        self,
        code,
        silent,
        store_history=True,
        user_expressions=None,
        allow_stdin=False,
        *,
        cell_id=None,
    ):
        """
        Used by ipykernel infrastructure for execution. For more info, look at
        https://jupyter-client.readthedocs.io/en/stable/messaging.html#execute
        """
        self.log.debug(f"Received execution request from Jupyter with code:\n{code}")
        try:
            accumulated_magic_outputs = []
            performed_startup_checks = False

            for output in self.magic_engine.process_before_cell_execution(
                code, self.execution_count
            ):
                self.handle_magic_output(output, accumulated_magic_outputs)

            skip_cell_execution = self.magic_engine.skip_cell_execution()
            self.log.debug(f"Skipping cell execution is set to {skip_cell_execution}")

            # Complete one-time startup checks before sending request to MATLAB.
            # Blocking call, returns after MATLAB is started.
            if not skip_cell_execution:
                if not self.startup_checks_completed:
                    await self.perform_startup_checks()
                    self.display_output(
                        {
                            "type": "stream",
                            "content": {
                                "name": "stdout",
                                "text": "Executing ...",
                            },
                        }
                    )
                    if accumulated_magic_outputs:
                        self.display_output(
                            {"type": "clear_output", "content": {"wait": False}}
                        )
                    performed_startup_checks = True
                    self.startup_checks_completed = True

                if performed_startup_checks and accumulated_magic_outputs:
                    for output in accumulated_magic_outputs:
                        self.display_output(output)

                # Perform execution and categorization of outputs in MATLAB. Blocks
                # until execution results are received from MATLAB.
                outputs = await self.mwi_comm_helper.send_execution_request_to_matlab(
                    code
                )

                if performed_startup_checks and not accumulated_magic_outputs:
                    self.display_output(
                        {"type": "clear_output", "content": {"wait": False}}
                    )

                self.log.debug(
                    "Received outputs after execution in MATLAB. Clearing output area"
                )

                # Display all the outputs produced during the execution of code.
                for idx in range(len(outputs)):
                    data = outputs[idx]
                    self.log.debug(f"Displaying output {idx+1}:\n{data}")

                    # Ignore empty values returned from MATLAB.
                    if not data:
                        continue
                    self.display_output(data)

            # Execute post execution of MAGICs
            for output in self.magic_engine.process_after_cell_execution():
                self.handle_magic_output(output)

        except Exception as e:
            self.log.error(
                f"Exception occurred while processing execution request:\n{e}"
            )
            if isinstance(e, aiohttp.client_exceptions.ClientError):
                # Log the ClientError for debugging
                self.log.error(e)

                # If exception is an ClientError, it means MATLAB is unavailable.
                # Replace the ClientError with MATLABConnectionError to give
                # meaningful error message to the user
                e = MATLABConnectionError()

                # Since MATLAB is not available, we need to perform the startup
                # checks for subsequent execution requests
                self.startup_checks_completed = False

            # Clearing lingering message "Executing..." before displaying the error message
            if performed_startup_checks and not accumulated_magic_outputs:
                self.display_output(
                    {"type": "clear_output", "content": {"wait": False}}
                )
            # Send the exception message to the user.
            self.display_output(
                {
                    "type": "stream",
                    "content": {
                        "name": "stderr",
                        "text": str(e),
                    },
                }
            )
        return {
            "status": "ok",
            "execution_count": self.execution_count,
            "payload": [],
            "user_expressions": {},
        }

    async def do_complete(self, code, cursor_pos):
        """
        Used by ipykernel infrastructure for tab completion. For more info, look
        at https://jupyter-client.readthedocs.io/en/stable/messaging.html#completion

        Note: Apart from completion results, no other data can be presented to
              user. For example, if matlab-proxy is not licensed, we cannot show
              the licensing window.
        """
        self.log.debug(
            f"Received completion request from Jupyter with cursor position {cursor_pos} and code:\n{code}"
        )
        # Default completion results. It is modelled after ipkernel.py#do_complete
        # implementation to provide metadata for JupyterLab.
        completion_results = {
            "matches": [],
            "start": cursor_pos,
            "end": cursor_pos,
            "completions": [],
        }

        # Fetch tab completion results. Blocks untils either tab completion
        # results are received from MATLAB or communication with MATLAB fails.

        magic_completion_results = get_completion_result_for_magics(
            code, cursor_pos, self.log
        )

        self.log.debug(
            f"Received Completion results from MAGIC:\n{magic_completion_results}"
        )

        if magic_completion_results:
            completion_results = magic_completion_results
        else:
            try:
                completion_results = (
                    await self.mwi_comm_helper.send_completion_request_to_matlab(
                        code, cursor_pos
                    )
                )
            except (
                MATLABConnectionError,
                aiohttp.client_exceptions.ClientResponseError,
            ) as e:
                self.log.error(
                    f"Exception occurred while sending completion request to MATLAB:\n{e}"
                )

            self.log.debug(
                f"Received completion results from MATLAB:\n{completion_results}"
            )

        return {
            "status": "ok",
            "matches": completion_results["matches"],
            "cursor_start": completion_results["start"],
            "cursor_end": completion_results["end"],
            "metadata": {
                "_jupyter_types_experimental": completion_results["completions"]
            },
        }

    async def do_is_complete(self, code):
        # TODO: Seems like indentation rules. https://jupyter-client.readthedocs.io/en/stable/messaging.html#code-completeness
        return super().do_is_complete(code)

    async def do_inspect(self, code, cursor_pos, detail_level=0, omit_sections=...):
        # TODO: Implement Shift+Tab functionality. Can be used to provide any contextual information.
        return super().do_inspect(code, cursor_pos, detail_level, omit_sections)

    async def do_history(
        self,
        hist_access_type,
        output,
        raw,
        session=None,
        start=None,
        stop=None,
        n=None,
        pattern=None,
        unique=False,
    ):
        # TODO: Implement accessing history in Notebook. Usually this history is related to the code typed in notebook.
        # However, we may also choose to associate with MATLAB History stored on disk.
        return super().do_history(
            hist_access_type, output, raw, session, start, stop, n, pattern, unique
        )

    async def do_shutdown(self, restart):
        self.log.debug("Received shutdown request from Jupyter")
        try:
            await self.mwi_comm_helper.send_shutdown_request_to_matlab()
            await self.mwi_comm_helper.disconnect()
        except (
            MATLABConnectionError,
            aiohttp.client_exceptions.ClientResponseError,
        ) as e:
            self.log.error(
                f"Exception occurred while sending shutdown request to MATLAB:\n{e}"
            )

        return super().do_shutdown(restart)

    # Helper functions

    async def perform_startup_checks(self):
        """
        One time checks triggered during the first execution request. Displays
        login window if matlab is not licensed using matlab-proxy.

        Raises:
            ClientError, MATLABConnectionError: Occurs when matlab-proxy is not started or kernel cannot
                                              communicate with MATLAB.
        """
        self.log.debug("Performing startup checks")
        # Incase an error occurred while kernel initialization, display it to the user.
        if self.startup_error is not None:
            self.log.error(f"Found a startup error: {self.startup_error}")
            raise self.startup_error

        (
            is_matlab_licensed,
            matlab_status,
            matlab_proxy_has_error,
        ) = await self.mwi_comm_helper.fetch_matlab_proxy_status()

        # Display iframe containing matlab-proxy to show login window if MATLAB
        # is not licensed using matlab-proxy. The iframe is removed after MATLAB
        # has finished startup.
        #
        # This approach does not work when using the kernel in VS Code. We are using relative path
        # as src for iframe to avoid hardcoding any hostname/domain information. This is done to
        # ensure the kernel works in Jupyter deployments. VS Code however does not work the same way
        # as other browser based Jupyter clients.
        #
        # TODO: Find a workaround for users to be able to use our Jupyter kernel in VS Code.
        if not is_matlab_licensed:
            self.log.debug(
                "MATLAB is not licensed. Displaying HTML output to enable licensing."
            )
            self.display_output(
                {
                    "type": "display_data",
                    "content": {
                        "data": {
                            "text/html": f'<iframe src={self.server_base_url + "matlab"} width=700 height=600"></iframe>'
                        },
                        "metadata": {},
                    },
                }
            )

        # Wait until MATLAB is started before sending requests.
        self.log.debug("Waiting until MATLAB is started")
        timeout = 0
        while (
            matlab_status != "up"
            and timeout != _MATLAB_STARTUP_TIMEOUT
            and not matlab_proxy_has_error
        ):
            if is_matlab_licensed:
                if timeout == 0:
                    self.log.debug("Licensing completed. Clearing output area")
                    self.display_output(
                        {"type": "clear_output", "content": {"wait": False}}
                    )
                    self.display_output(
                        {
                            "type": "stream",
                            "content": {
                                "name": "stdout",
                                "text": "Starting MATLAB ...\n",
                            },
                        }
                    )
                timeout += 1
            time.sleep(1)
            (
                is_matlab_licensed,
                matlab_status,
                matlab_proxy_has_error,
            ) = await self.mwi_comm_helper.fetch_matlab_proxy_status()

        # If MATLAB is not available after 15 seconds of licensing information
        # being available either through user input or through matlab-proxy cache,
        # then display connection error to the user.
        if timeout == _MATLAB_STARTUP_TIMEOUT:
            self.log.error(
                f"MATLAB has not started after {_MATLAB_STARTUP_TIMEOUT} seconds."
            )
            raise MATLABConnectionError

        if matlab_proxy_has_error:
            self.log.error("matlab-proxy encountered error.")
            raise MATLABConnectionError

        self.log.debug("MATLAB is running, startup checks completed.")

    def display_output(self, out):
        """
        Common function to send execution outputs to Jupyter UI.
        For more information, look at https://jupyter-client.readthedocs.io/en/stable/messaging.html#messages-on-the-iopub-pub-sub-channel

        Input Example:
        1.  Execution Output:
            out = {
                "type": "execute_result",
                "mimetype": ["text/plain","text/html"],
                "value": ["Hello","<html><body>Hello</body></html>"]
            }
        2.  For all other message types:
            out = {
                "type": "stream",
                "content": {
                    "name": "stderr",
                    "text": "An error occurred"
                }
            }

        Args:
            out (dict): A dictionary containing the type of output and the content of the output.
        """
        msg_type = out["type"]
        if msg_type == "execute_result":
            assert len(out["mimetype"]) == len(out["value"])
            response = {
                # Use zip to create a tuple of KV pair of mimetype and value.
                "data": dict(zip(out["mimetype"], out["value"])),
                "metadata": {},
                "execution_count": self.execution_count,
            }
        else:
            response = out["content"]
        self.send_response(self.iopub_socket, msg_type, response)
